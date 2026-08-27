import csv
import importlib.util
import json
from pathlib import Path
from types import ModuleType

import pytest

from neutrino_trigger.cli import run as run_cli
from neutrino_trigger.parameters import (
    RESEARCH_CUTOFF,
    SOURCE_VERIFIED_DATE,
    STANCIL_2012_PARAMETERS,
    EvidenceStatus,
    ParameterRecord,
)
from neutrino_trigger.simulation import default_summary_rows, evaluate_trigger_snapshot


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _load_script(name: str) -> ModuleType:
    path = PROJECT_ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"test_{name}_module", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_decision_window_fails_closed_before_json_serialization() -> None:
    for invalid in (0.0, -1e-3):
        with pytest.raises(ValueError, match="decision_window_s must be positive"):
            evaluate_trigger_snapshot(1.0, 0.0, 1, invalid)
        with pytest.raises(ValueError, match="decision_window_s must be positive"):
            run_cli(
                [
                    "detect",
                    "--signal-mean",
                    "1",
                    "--decision-window-s",
                    str(invalid),
                ]
            )


def test_default_summary_and_cli_payloads_are_strict_json() -> None:
    json.dumps(default_summary_rows(), allow_nan=False)
    payload = run_cli(
        ["detect", "--signal-mean", "1", "--decision-window-s", "0.001"]
    )
    json.dumps(payload, allow_nan=False)
    assert payload["effective_h1_event_rate_hz"] == pytest.approx(1_000.0)


def test_parameter_record_rejects_untyped_evidence_status() -> None:
    with pytest.raises(TypeError, match="evidence_status must be an EvidenceStatus"):
        ParameterRecord(
            name="invalid",
            value=1.0,
            unit="1",
            uncertainty_or_range="none",
            source="synthetic",
            source_type="test",
            locator="test",
            verified_date="2026-08-26",
            evidence_status="synthetic",  # type: ignore[arg-type]
        )
    valid = ParameterRecord(
        name="valid",
        value=1.0,
        unit="1",
        uncertainty_or_range="none",
        source="synthetic",
        source_type="test",
        locator="test",
        verified_date="2026-08-26",
        evidence_status=EvidenceStatus.SYNTHETIC,
    )
    assert valid.evidence_status is EvidenceStatus.SYNTHETIC


def test_source_verification_date_and_cutoff_are_distinct_and_locators_are_audited() -> None:
    assert RESEARCH_CUTOFF == "2026-08-26"
    assert SOURCE_VERIFIED_DATE == "2026-08-27"
    by_name = {record.name: record for record in STANCIL_2012_PARAMETERS}
    assert by_name["protons per communications-study pulse"].locator.endswith("p. 5")
    assert by_name["qualifying muon events per on pulse"].locator.endswith("p. 5")
    assert all(record.verified_date == SOURCE_VERIFIED_DATE for record in STANCIL_2012_PARAMETERS)


def test_table_artifacts_preserve_ledger_and_report_all_relay_models(tmp_path: Path) -> None:
    module = _load_script("build_tables")
    ledger = tmp_path / "parameter_provenance.csv"
    ledger.write_text("human-reviewed-sentinel\n", encoding="utf-8")
    paths = module.build(tmp_path)
    assert ledger.read_text(encoding="utf-8") == "human-reviewed-sentinel\n"
    assert (tmp_path / "relay_model_summary.csv") in paths
    assert (tmp_path / "figure_parameters.csv") in paths

    relay_rows = _read_csv(tmp_path / "relay_model_summary.csv")
    assert len(relay_rows) == 24
    assert {row["model"] for row in relay_rows} == {
        "ideal_no_distance_penalty",
        "synthetic_geometric",
        "literature_informed_supplied",
    }
    unavailable = [
        row
        for row in relay_rows
        if row["model"] == "literature_informed_supplied" and int(row["hop_count"]) > 1
    ]
    assert len(unavailable) == 7
    assert all(row["availability"] == "UNAVAILABLE_EVIDENCE_GAP" for row in unavailable)
    assert all(row["end_to_end_detection_probability"] == "UNKNOWN" for row in unavailable)
    synthetic = [row for row in relay_rows if row["evidence_status"] == "SYNTHETIC"]
    assert len(synthetic) == 16
    assert all("SIMULATION_ONLY" in row["notes"] for row in synthetic)
    assert all("false origin only at hop 1" in row["notes"] for row in synthetic)
    assert all("Pulse cost charges all hops" in row["notes"] for row in synthetic)
    geometric_h2 = next(
        row
        for row in relay_rows
        if row["model"] == "synthetic_geometric" and row["hop_count"] == "2"
    )
    assert float(geometric_h2["supplied_end_to_end_false_alarm_probability"]) > 1e-8

    gap_rows = _read_csv(tmp_path / "engineering_gap_template.csv")
    assert len(gap_rows) >= 21
    pulse_width = next(row for row in gap_rows if row["variable"] == "Pulse width")
    assert "8.1 microseconds" in pulse_width["verified_present_baseline"]
    assert "Required gate cannot be shortened" in pulse_width["falsifier"]
    authentication = next(
        row for row in gap_rows if row["variable"] == "Authentication sequence overhead"
    )
    assert "NOT ESTABLISHED" in authentication["verified_present_baseline"]
    assert "Minimum secure sequence time" in authentication["falsifier"]

    figure_rows = _read_csv(tmp_path / "figure_parameters.csv")
    assert {row["figure"] for row in figure_rows} == {
        "01_binomial_vs_poisson",
        "02_deadline_detection",
        "03_roc_curves",
        "04_arc_chord_advantage",
        "05_incremental_value",
        "06_relay_phase_diagram",
        "07_events_per_joule_break_even",
        "08_hybrid_channel_comparison",
    }
    anchor = next(
        row
        for row in figure_rows
        if row["parameter"] == "stancil_anchor_signal_mean_event_per_gate"
    )
    anchor_background = next(
        row
        for row in figure_rows
        if row["parameter"]
        == "anchor_regime_synthetic_background_mean_event_per_gate"
    )
    assert anchor["value"] == "0.81"
    assert anchor["evidence_status"] == "PRIMARY_PAPER_ANCHOR"
    assert anchor_background["evidence_status"] == "SYNTHETIC"
    relay_parameters = {
        row["parameter"]: row
        for row in figure_rows
        if row["figure"] == "06_relay_phase_diagram"
    }
    assert "pulse_cost_convention" in relay_parameters
    assert "false_trigger_relay_pulse_cost_convention" in relay_parameters
    hybrid_parameters = {
        row["parameter"]: row
        for row in figure_rows
        if row["figure"] == "08_hybrid_channel_comparison"
    }
    assert hybrid_parameters["fixed_neutrino_latency_s"]["value"] == "0.0002"
    for figure in {row["figure"] for row in figure_rows}:
        assert len([row for row in figure_rows if row["figure"] == figure]) >= 3


def test_every_generated_figure_has_stable_name_and_machine_readable_label(
    tmp_path: Path,
) -> None:
    module = _load_script("build_figures")
    paths = module.build(tmp_path)
    assert tuple(path.name for path in paths) == module.FIGURE_NAMES
    for path in paths:
        data = path.read_bytes()
        assert len(data) > 10_000
        assert b"SIMULATION_ONLY" in data
        assert b"not measured system performance" in data
