#!/usr/bin/env python3
"""Build deterministic CSV tables for the concept paper."""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
import sys
from typing import Any, Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from neutrino_trigger.parameters import (  # noqa: E402
    STANCIL_2012_PARAMETERS,
    SyntheticScenario,
)
from neutrino_trigger.detection import false_alarm_probability  # noqa: E402
from neutrino_trigger.geometry import SPEED_OF_LIGHT_M_S  # noqa: E402
from neutrino_trigger.figure_inputs import figure_parameter_rows  # noqa: E402
from neutrino_trigger.relay import (  # noqa: E402
    AnnualRelayValueInputs,
    DistanceModel,
    annual_relay_incremental_value,
    evaluate_equal_hop_architecture,
    regenerative_false_origin_upper_bound,
)
from neutrino_trigger.simulation import default_summary_rows  # noqa: E402


SYNTHETIC_NOTICE = "SIMULATION_ONLY; illustrative assumptions; not measured system performance."


def _write_rows(path: Path, fieldnames: Iterable[str], rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(fieldnames), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _provenance_rows() -> list[dict[str, Any]]:
    return [record.as_dict() for record in STANCIL_2012_PARAMETERS]


def _synthetic_rows() -> list[dict[str, Any]]:
    return [record.as_dict() for record in SyntheticScenario().as_parameter_records()]


def _break_even_rows() -> list[dict[str, str]]:
    return [
        {
            "quantity": "threshold-one deadline rate",
            "inequality": "mu_s >= -ln(1-q)/t_d",
            "interpretation": "Zero-background signal rate needed for one qualifying arrival by deadline t_d.",
            "scope": "analytic; threshold one; homogeneous independent Poisson events",
        },
        {
            "quantity": "latency advantage",
            "inequality": "tau_EM - tau_nu > 0",
            "interpretation": "Complete neutrino decision path must beat the best EM fallback, not merely its propagation term.",
            "scope": "full end-to-end accounting",
        },
        {
            "quantity": "annual incremental value",
            "inequality": "rho1(E[Delta G]-C_pulse) - rho0 P_FA L_FA - C_fixed - C_operate > 0",
            "interpretation": "Early-trigger gains must exceed pulse, false-trigger, fixed, and operating costs.",
            "scope": "incremental versus conventional fallback",
        },
        {
            "quantity": "relay selection",
            "inequality": "h* = argmax_h Delta V_h",
            "interpretation": "A relay is justified only if flux/detector gains exceed compounded misses, regeneration delay, and cost.",
            "scope": "independent-hop reliability is an explicit approximation",
        },
        {
            "quantity": "events per joule",
            "inequality": "eta_q >= -ln(1-q)/E_pulse",
            "interpretation": "Threshold-one, zero-background qualifying-event yield required per pulse joule.",
            "scope": SYNTHETIC_NOTICE,
        },
    ]


def _engineering_gap_rows() -> list[dict[str, str]]:
    """Read the reviewed subsystem rows from ``research-targets.md``.

    The Markdown target sheet is the human-reviewed source of truth.  Parsing it
    avoids replacing its specific baselines and falsifiers with generic UNKNOWN
    placeholders while preserving deterministic row order and exact wording.
    """

    source_path = PROJECT_ROOT / "research-targets.md"
    expected_header = (
        "Variable",
        "Meaning",
        "Verified present baseline",
        "Required break-even target",
        "Gap",
        "Uncertainty",
        "Possible research lever",
        "Falsifier",
    )
    lines = source_path.read_text(encoding="utf-8").splitlines()
    header_index = next(
        (
            index
            for index, line in enumerate(lines)
            if tuple(cell.strip() for cell in line.strip().strip("|").split("|"))
            == expected_header
        ),
        None,
    )
    if header_index is None:
        raise ValueError("research-targets.md does not contain the expected engineering table")
    keys = (
        "variable",
        "meaning",
        "verified_present_baseline",
        "required_break_even_target",
        "gap",
        "uncertainty",
        "possible_research_lever",
        "falsifier",
    )
    rows: list[dict[str, str]] = []
    for line in lines[header_index + 2 :]:
        if not line.startswith("|"):
            break
        cells = tuple(cell.strip() for cell in line.strip().strip("|").split("|"))
        if len(cells) != len(keys):
            raise ValueError("malformed engineering target row")
        rows.append(dict(zip(keys, cells, strict=True)))
    required_variables = {
        "Source-command-to-beam latency",
        "Pulse width",
        "Authentication sequence overhead",
        "Neutrino yield per joule",
        "Usable beam divergence",
        "Qualifying interactions per emitted neutrino",
        "Qualifying interactions per joule",
        "Detector target mass",
        "Detector effective area",
        "Background rate per decision gate",
        "Reconstruction efficiency",
        "Time to first sufficient evidence",
        "DAQ and classification latency",
        "False-trigger probability",
        "Endpoint last-mile latency",
        "Classical-route latency",
        "Incremental market value per successful early trigger",
        "Annual opportunity rate",
        "Pulse variable cost",
        "Fixed infrastructure cost",
        "Relay regeneration delay",
    }
    actual_variables = {row["variable"] for row in rows}
    missing = sorted(required_variables - actual_variables)
    if missing:
        raise ValueError(
            "research-targets.md is missing required engineering targets: "
            + ", ".join(missing)
        )
    return rows


def _relay_model_rows() -> list[dict[str, Any]]:
    """Run two explicit synthetic models and audit literature-data availability.

    The Stancil experiment supplies one direct-link signal mean but no regenerative
    hop measurements.  Consequently, literature-informed h>1 cells are emitted as
    literal ``UNKNOWN`` values instead of receiving synthetic stand-ins.
    """

    total_distance_m = 5.0e6
    direct_signal_mean = 0.10
    background_mean_per_hop = 1.0e-6
    threshold = 1
    relay_delay_s = 1.0e-4
    endpoint_delay_s = 2.0e-4
    pulse_cost_per_hop_currency = 2.0
    valid_windows_per_year = 10_000.0
    null_windows_per_year = 1_000_000.0
    false_trigger_loss_currency = 2_000.0
    initial_value_currency = 500.0
    value_decay_s = 5.0e-2
    em_fallback_deadline_s = 2.5e-2
    base_annual_fixed_cost_currency = 150_000.0
    base_annual_operating_cost_currency = 100_000.0
    annual_fixed_cost_per_relay_currency = 40_000.0
    annual_operating_cost_per_relay_currency = 10_000.0
    per_hop_pfa = false_alarm_probability(background_mean_per_hop, threshold)
    rows: list[dict[str, Any]] = []

    for model in (
        DistanceModel.IDEAL_NO_DISTANCE_PENALTY,
        DistanceModel.SYNTHETIC_GEOMETRIC,
    ):
        for hops in range(1, 9):
            evaluation = evaluate_equal_hop_architecture(
                total_distance_m=total_distance_m,
                hop_count=hops,
                direct_signal_mean=direct_signal_mean,
                background_mean_per_hop=background_mean_per_hop,
                threshold=threshold,
                propagation_speed_m_s=SPEED_OF_LIGHT_M_S,
                relay_regeneration_delay_s=relay_delay_s,
                endpoint_delay_s=endpoint_delay_s,
                pulse_cost_per_hop=pulse_cost_per_hop_currency,
                relay_infrastructure_cost=0.0,
                distance_model=model,
            )
            end_to_end_pfa = regenerative_false_origin_upper_bound(
                (per_hop_pfa,) + (0.0,) * (hops - 1),
                evaluation.per_hop_detection_probabilities,
            )
            fallback_relative_gain = initial_value_currency * max(
                0.0,
                math.exp(-evaluation.latency_s / value_decay_s)
                - math.exp(-em_fallback_deadline_s / value_decay_s),
            )
            annual_fixed_cost = (
                base_annual_fixed_cost_currency
                + (hops - 1) * annual_fixed_cost_per_relay_currency
            )
            annual_operating_cost = (
                base_annual_operating_cost_currency
                + (hops - 1) * annual_operating_cost_per_relay_currency
            )
            pulse_cost = hops * pulse_cost_per_hop_currency
            annual_value = annual_relay_incremental_value(
                evaluation,
                AnnualRelayValueInputs(
                    valid_windows_per_year=valid_windows_per_year,
                    null_windows_per_year=null_windows_per_year,
                    end_to_end_false_alarm_probability=end_to_end_pfa,
                    fallback_relative_gain_per_success=fallback_relative_gain,
                    false_trigger_loss=false_trigger_loss_currency,
                    pulse_variable_cost_per_valid_window=pulse_cost,
                    annual_fixed_cost=annual_fixed_cost,
                    annual_operating_cost=annual_operating_cost,
                ),
            )
            rows.append(
                {
                    "model": model.value,
                    "hop_count": hops,
                    "evidence_status": "SYNTHETIC",
                    "availability": "AVAILABLE_AS_SIMULATION_ONLY",
                    "per_hop_signal_means_event_per_gate": ";".join(
                        f"{mean:.12g}" for mean in evaluation.per_hop_signal_means
                    ),
                    "end_to_end_detection_probability": evaluation.end_to_end_detection_probability,
                    "supplied_end_to_end_false_alarm_probability": end_to_end_pfa,
                    "modeled_latency_s": evaluation.latency_s,
                    "known_propagation_only_s": total_distance_m / SPEED_OF_LIGHT_M_S,
                    "valid_windows_per_year": valid_windows_per_year,
                    "null_windows_per_year": null_windows_per_year,
                    "fallback_relative_gain_per_success_currency": fallback_relative_gain,
                    "false_trigger_loss_currency": false_trigger_loss_currency,
                    "pulse_variable_cost_per_valid_window_currency": pulse_cost,
                    "annual_fixed_cost_currency": annual_fixed_cost,
                    "annual_operating_cost_currency": annual_operating_cost,
                    "annual_incremental_value_currency_per_year": annual_value,
                    "notes": (
                        f"{SYNTHETIC_NOTICE} Named causal PFA example permits a false "
                        "origin only at hop 1 and requires all downstream PD events. "
                        "Pulse cost charges all hops on every valid window; relay pulses "
                        "caused by false origins are excluded and would reduce value further."
                    ),
                }
            )

    direct_literature = evaluate_equal_hop_architecture(
        total_distance_m=1_035.0,
        hop_count=1,
        direct_signal_mean=0.81,
        background_mean_per_hop=0.0,
        threshold=1,
        propagation_speed_m_s=SPEED_OF_LIGHT_M_S,
        relay_regeneration_delay_s=0.0,
        endpoint_delay_s=0.0,
        pulse_cost_per_hop=0.0,
        relay_infrastructure_cost=0.0,
        distance_model=DistanceModel.SUPPLIED_HOP_MEANS,
        supplied_hop_means=(0.81,),
    )
    for hops in range(1, 9):
        direct_available = hops == 1
        rows.append(
            {
                "model": "literature_informed_supplied",
                "hop_count": hops,
                "evidence_status": (
                    "PRIMARY_PAPER_REPRODUCTION" if direct_available else "LITERATURE_GAP"
                ),
                "availability": (
                    "DIRECT_ANCHOR_ONLY" if direct_available else "UNAVAILABLE_EVIDENCE_GAP"
                ),
                "per_hop_signal_means_event_per_gate": "0.81" if direct_available else "UNKNOWN",
                "end_to_end_detection_probability": (
                    direct_literature.end_to_end_detection_probability
                    if direct_available
                    else "UNKNOWN"
                ),
                "supplied_end_to_end_false_alarm_probability": "UNKNOWN",
                "modeled_latency_s": "UNKNOWN",
                "known_propagation_only_s": (
                    1_035.0 / SPEED_OF_LIGHT_M_S if direct_available else "UNKNOWN"
                ),
                "valid_windows_per_year": "UNKNOWN",
                "null_windows_per_year": "UNKNOWN",
                "fallback_relative_gain_per_success_currency": "UNKNOWN",
                "false_trigger_loss_currency": "UNKNOWN",
                "pulse_variable_cost_per_valid_window_currency": "UNKNOWN",
                "annual_fixed_cost_currency": "UNKNOWN",
                "annual_operating_cost_currency": "UNKNOWN",
                "annual_incremental_value_currency_per_year": "UNKNOWN",
                "notes": (
                    "Stancil et al. (2012) direct-link lambda=0.81 reproduction; full "
                    "request-to-decision latency and numeric background bound are unavailable."
                    if direct_available
                    else "UNKNOWN: no source-audited regenerative-hop signal mean or delay."
                ),
            }
        )
    return rows


def build(output_dir: Path) -> tuple[Path, ...]:
    """Write all generated tables and return their paths."""

    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = output_dir / "summary.csv"
    # The curated evidence ledger at ``parameter_provenance.csv`` is maintained
    # by human/source-audit review and is intentionally never overwritten here.
    reproduction_parameters_path = output_dir / "stancil_2012_reproduction_parameters.csv"
    synthetic_path = output_dir / "synthetic_scenario_parameters.csv"
    inequalities_path = output_dir / "break_even_inequalities.csv"
    gaps_path = output_dir / "engineering_gap_template.csv"
    relay_models_path = output_dir / "relay_model_summary.csv"
    figure_parameters_path = output_dir / "figure_parameters.csv"
    summary_rows = default_summary_rows()
    _write_rows(summary_path, summary_rows[0].keys(), summary_rows)
    provenance_rows = _provenance_rows()
    _write_rows(
        reproduction_parameters_path,
        provenance_rows[0].keys(),
        provenance_rows,
    )
    synthetic_rows = _synthetic_rows()
    _write_rows(synthetic_path, synthetic_rows[0].keys(), synthetic_rows)
    break_even_rows = _break_even_rows()
    _write_rows(inequalities_path, break_even_rows[0].keys(), break_even_rows)
    gap_rows = _engineering_gap_rows()
    _write_rows(gaps_path, gap_rows[0].keys(), gap_rows)
    relay_rows = _relay_model_rows()
    _write_rows(relay_models_path, relay_rows[0].keys(), relay_rows)
    figure_rows = figure_parameter_rows()
    _write_rows(figure_parameters_path, figure_rows[0].keys(), figure_rows)
    return (
        summary_path,
        reproduction_parameters_path,
        synthetic_path,
        inequalities_path,
        gaps_path,
        relay_models_path,
        figure_parameters_path,
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "results",
        help="output directory (default: results)",
    )
    return parser


def main() -> None:
    args = _parser().parse_args()
    for path in build(args.output_dir):
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
