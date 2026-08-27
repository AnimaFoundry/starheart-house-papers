"""Deterministic offline experiment compositions used by scripts and CLI."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Any

from .detection import detection_probability, false_alarm_probability
from .economics import annual_incremental_value_fixed_gain
from .first_arrival import arrival_cdf
from .geometry import SPEED_OF_LIGHT_M_S, earth_arc_length_m, earth_chord_length_m
from .parameters import SyntheticScenario, positive
from .probability import (
    exact_at_least_one,
    ook_capacity_bits_per_pulse,
    on_off_keying_ber,
    poisson_limit_at_least_one,
)


DEFAULT_RANDOM_SEED = 20260826


@dataclass(frozen=True, slots=True)
class StancilReproductionRow:
    """A directly reproducible zero-background OOK calculation."""

    combined_frames: int
    effective_signal_mean: float
    threshold_one_detection_probability: float
    theoretical_uncoded_ber: float


def reproduce_stancil_2012_channel() -> dict[str, Any]:
    """Reproduce core Poisson-channel quantities from arXiv:1203.2847v2.

    The primary paper estimates ``lambda = 0.81`` qualifying events per on pulse,
    uses threshold-one on-off keying with nearly zero background, and gives an OOK
    capacity expression in its Eq. (2).  Combining frames adds their event counts.
    """

    signal_mean = 0.81
    incident_protons_per_pulse = 2.25e13
    incident_proton_kinetic_energy_gev = 120.0
    joule_per_electronvolt = 1.602_176_634e-19
    incident_proton_energy_per_pulse_j = (
        incident_protons_per_pulse
        * incident_proton_kinetic_energy_gev
        * 1.0e9
        * joule_per_electronvolt
    )
    qualifying_events_per_incident_proton_beam_joule = (
        signal_mean / incident_proton_energy_per_pulse_j
    )
    rows = tuple(
        StancilReproductionRow(
            combined_frames=frames,
            effective_signal_mean=frames * signal_mean,
            threshold_one_detection_probability=detection_probability(
                frames * signal_mean, 0.0, 1
            ),
            theoretical_uncoded_ber=on_off_keying_ber(
                frames * signal_mean, 0.0, 0.5
            ),
        )
        for frames in (1, 2, 3, 5, 9, 15)
    )
    capacity = ook_capacity_bits_per_pulse(signal_mean)
    return {
        "source": "Stancil et al. (2012), arXiv:1203.2847v2",
        "evidence_status": "primary-paper reproduction",
        "signal_mean_events_per_on_pulse": signal_mean,
        "background_assumption_events_per_gate": 0.0,
        "incident_protons_per_pulse": incident_protons_per_pulse,
        "incident_proton_kinetic_energy_gev": incident_proton_kinetic_energy_gev,
        "incident_proton_kinetic_energy_per_pulse_j": incident_proton_energy_per_pulse_j,
        "qualifying_events_per_incident_proton_beam_joule": (
            qualifying_events_per_incident_proton_beam_joule
        ),
        "capacity_bits_per_pulse": capacity,
        "capacity_at_nominal_2_2_s_spacing_bits_per_s": capacity / 2.2,
        "paper_experimental_information_rate_bits_per_pulse": 40.0 / 184.0,
        "paper_experimental_information_rate_bits_per_s": (40.0 / 184.0) / 2.2,
        "rows": [asdict(row) for row in rows],
        "limitations": (
            "The derived incident-proton-beam energy is not wall-plug energy or "
            "emitted-neutrino yield. The nearly-zero-background synchronized OOK "
            "model does not include "
            "source-command latency, beam actuation, authentication, relay regeneration, "
            "or a market decision deadline."
        ),
    }


def one_over_e_limit_snapshot() -> dict[str, float | str]:
    """Numerically expose the bounded ``1 - 1/e`` threshold-one result."""

    particles = 10_000_000
    p_eff = 1.0 / particles
    return {
        "emitted_particles": float(particles),
        "p_eff": p_eff,
        "lambda_s": particles * p_eff,
        "exact_binomial_probability": exact_at_least_one(particles, p_eff),
        "poisson_probability": poisson_limit_at_least_one(particles, p_eff),
        "limiting_probability": 1.0 - math.exp(-1.0),
        "assumptions": (
            "threshold one; independent constant-p particles; small p_eff; zero background"
        ),
    }


def default_summary_rows() -> list[dict[str, Any]]:
    """Return compact measured/reproduced and synthetic audit rows."""

    reproduction = reproduce_stancil_2012_channel()
    limit = one_over_e_limit_snapshot()
    angle = math.radians(90.0)
    scenario = SyntheticScenario()
    synthetic_pd = arrival_cdf(1_000.0, scenario.em_deadline_s, 1)
    synthetic_pfa = false_alarm_probability(1.0e-6, 1)
    synthetic_value = annual_incremental_value_fixed_gain(
        scenario.valid_windows_per_year,
        scenario.null_windows_per_year,
        synthetic_pd,
        synthetic_pfa,
        scenario.gross_value_per_early_success,
        scenario.false_trigger_loss,
        25.0,
        scenario.annual_fixed_cost,
        scenario.annual_operating_cost,
    )
    return [
        {
            "metric": "stancil_2012_signal_mean",
            "value": reproduction["signal_mean_events_per_on_pulse"],
            "unit": "event/pulse",
            "evidence_status": "estimated in primary paper",
            "notes": "Reproduction anchor; not a present market-link parameter.",
        },
        {
            "metric": "stancil_2012_ook_capacity",
            "value": reproduction["capacity_bits_per_pulse"],
            "unit": "bit/pulse",
            "evidence_status": "reproduced from primary-paper equation",
            "notes": "Zero-background OOK capacity at lambda=0.81.",
        },
        {
            "metric": "one_over_e_threshold_one_limit",
            "value": limit["limiting_probability"],
            "unit": "probability",
            "evidence_status": "analytic",
            "notes": limit["assumptions"],
        },
        {
            "metric": "ideal_90_degree_arc_minus_chord_time",
            "value": (
                earth_arc_length_m(angle) - earth_chord_length_m(angle)
            )
            / SPEED_OF_LIGHT_M_S,
            "unit": "s",
            "evidence_status": "analytic geometry",
            "notes": "Geometry only; excludes all source, detector, routing, and decision latency.",
        },
        {
            "metric": "illustrative_annual_incremental_value",
            "value": synthetic_value,
            "unit": "arbitrary currency/year",
            "evidence_status": "SYNTHETIC",
            "notes": "SIMULATION_ONLY; illustrative assumptions; not measured system performance.",
        },
    ]


def evaluate_trigger_snapshot(
    signal_mean: float,
    background_mean: float,
    threshold: int,
    decision_window_s: float,
) -> dict[str, float | int | str]:
    """Evaluate a non-operational count-gate scenario for the CLI."""

    decision_window = positive(decision_window_s, "decision_window_s")
    pd = detection_probability(signal_mean, background_mean, threshold)
    pfa = false_alarm_probability(background_mean, threshold)
    effective_total_rate = (signal_mean + background_mean) / decision_window
    return {
        "signal_mean": signal_mean,
        "background_mean": background_mean,
        "threshold": threshold,
        "decision_window_s": decision_window,
        "detection_probability": pd,
        "false_alarm_probability": pfa,
        "effective_h1_event_rate_hz": effective_total_rate,
        "status": "SIMULATION_ONLY",
        "warning": "Illustrative count model; not measured system performance or deployment authority.",
    }
