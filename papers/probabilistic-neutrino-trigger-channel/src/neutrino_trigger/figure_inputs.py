"""Single source of truth for every load-bearing generated-figure input."""

from __future__ import annotations

from typing import Any

from .geometry import MEAN_EARTH_RADIUS_M, SPEED_OF_LIGHT_M_S


FIGURE_INPUTS: dict[str, dict[str, Any]] = {
    "01_binomial_vs_poisson": {
        "p_eff": 1.0e-3,
        "particle_count_min": 0,
        "particle_count_max": 10_000,
    },
    "02_deadline_detection": {
        "deadline_min_s": 0.0,
        "deadline_max_s": 0.020,
        "sample_count": 500,
        "effective_rates_hz": (100.0, 300.0, 1_000.0),
    },
    "03_roc_curves": {
        "stancil_anchor_signal_mean_event_per_gate": 0.81,
        "anchor_regime_synthetic_background_mean_event_per_gate": 0.01,
        "synthetic_signal_means_event_per_gate": (0.5, 2.0, 5.0),
        "synthetic_background_means_event_per_gate": (0.01, 0.10, 1.00),
        "maximum_count_threshold": 18,
    },
    "04_arc_chord_advantage": {
        "mean_spherical_earth_radius_m": MEAN_EARTH_RADIUS_M,
        "central_angle_min_degree": 0.0,
        "central_angle_max_degree": 180.0,
        "sample_count": 721,
        "surface_path_speed_m_s": SPEED_OF_LIGHT_M_S,
        "chord_path_speed_m_s": SPEED_OF_LIGHT_M_S,
    },
    "05_incremental_value": {
        "detection_probability_min": 0.0,
        "detection_probability_max": 1.0,
        "detection_probability_sample_count": 161,
        "false_alarm_probability_min": 1.0e-9,
        "false_alarm_probability_max": 1.0e-3,
        "false_alarm_probability_sample_count": 181,
        "pulse_costs_currency_per_valid_window": (0.0, 50.0, 200.0),
        "valid_windows_per_year": 10_000.0,
        "null_windows_per_year": 1_000_000.0,
        "fallback_relative_gain_currency_per_success": 500.0,
        "false_trigger_loss_currency": 2_000.0,
        "annual_fixed_cost_currency": 750_000.0,
        "annual_operating_cost_currency": 250_000.0,
    },
    "06_relay_phase_diagram": {
        "direct_signal_mean_min_event_per_gate": 1.0e-3,
        "direct_signal_mean_max_event_per_gate": 10.0,
        "direct_signal_mean_sample_count": 121,
        "relay_regeneration_delay_min_s": 1.0e-6,
        "relay_regeneration_delay_max_s": 1.0e-2,
        "relay_regeneration_delay_sample_count": 101,
        "total_distance_m": 5.0e6,
        "endpoint_delay_s": 2.0e-4,
        "em_fallback_deadline_s": 2.5e-2,
        "value_decay_s": 5.0e-2,
        "initial_gross_value_currency": 500.0,
        "valid_windows_per_year": 10_000.0,
        "null_windows_per_year": 1_000_000.0,
        "false_trigger_loss_currency": 2_000.0,
        "first_hop_false_origin_probability": 1.0e-6,
        "pulse_cost_per_hop_currency": 2.0,
        "base_annual_fixed_cost_currency": 150_000.0,
        "base_annual_operating_cost_currency": 100_000.0,
        "annual_fixed_cost_per_relay_currency": 40_000.0,
        "annual_operating_cost_per_relay_currency": 10_000.0,
        "minimum_hop_count": 1,
        "maximum_hop_count": 8,
        "synthetic_geometric_exponent": 2.0,
        "pulse_cost_convention": "all-hop conservative cost on every valid window",
        "false_trigger_relay_pulse_cost_convention": (
            "excluded separately; include in false-trigger loss if material"
        ),
    },
    "07_events_per_joule_break_even": {
        "target_probability_min": 0.50,
        "target_probability_max": 0.999,
        "target_probability_sample_count": 220,
        "pulse_energy_min_j": 1.0e3,
        "pulse_energy_max_j": 1.0e15,
        "pulse_energy_sample_count": 260,
        "count_threshold": 1,
        "background_mean_event_per_gate": 0.0,
    },
    "08_hybrid_channel_comparison": {
        "em_fallback_deadline_s": 1.0e-3,
        "fixed_neutrino_latency_s": 2.0e-4,
        "trigger_rate_min_hz": 1.0,
        "trigger_rate_max_hz": 1.0e5,
        "trigger_rate_sample_count": 400,
        "count_threshold": 1,
        "background_rate_hz": 0.0,
    },
}


_UNITS: dict[str, str] = {
    "p_eff": "qualifying event/emitted particle",
    "particle_count_min": "emitted particle",
    "particle_count_max": "emitted particle",
    "deadline_min_s": "s",
    "deadline_max_s": "s",
    "sample_count": "sample",
    "effective_rates_hz": "qualifying event/s",
    "stancil_anchor_signal_mean_event_per_gate": "qualifying event/gate",
    "anchor_regime_synthetic_background_mean_event_per_gate": "qualifying event/gate",
    "synthetic_signal_means_event_per_gate": "qualifying event/gate",
    "synthetic_background_means_event_per_gate": "qualifying event/gate",
    "maximum_count_threshold": "count",
    "mean_spherical_earth_radius_m": "m",
    "central_angle_min_degree": "degree",
    "central_angle_max_degree": "degree",
    "surface_path_speed_m_s": "m/s",
    "chord_path_speed_m_s": "m/s",
    "detection_probability_min": "probability",
    "detection_probability_max": "probability",
    "detection_probability_sample_count": "sample",
    "false_alarm_probability_min": "probability/null window",
    "false_alarm_probability_max": "probability/null window",
    "false_alarm_probability_sample_count": "sample",
    "pulse_costs_currency_per_valid_window": "synthetic currency/valid window",
    "valid_windows_per_year": "valid window/year",
    "null_windows_per_year": "null window/year",
    "fallback_relative_gain_currency_per_success": "synthetic currency/success",
    "false_trigger_loss_currency": "synthetic currency/false trigger",
    "annual_fixed_cost_currency": "synthetic currency/year",
    "annual_operating_cost_currency": "synthetic currency/year",
    "direct_signal_mean_min_event_per_gate": "qualifying event/gate",
    "direct_signal_mean_max_event_per_gate": "qualifying event/gate",
    "direct_signal_mean_sample_count": "sample",
    "relay_regeneration_delay_min_s": "s/relay",
    "relay_regeneration_delay_max_s": "s/relay",
    "relay_regeneration_delay_sample_count": "sample",
    "total_distance_m": "m",
    "endpoint_delay_s": "s",
    "em_fallback_deadline_s": "s",
    "fixed_neutrino_latency_s": "s",
    "value_decay_s": "s",
    "initial_gross_value_currency": "synthetic currency",
    "first_hop_false_origin_probability": "probability/null gate",
    "pulse_cost_per_hop_currency": "synthetic currency/valid window/hop",
    "base_annual_fixed_cost_currency": "synthetic currency/year",
    "base_annual_operating_cost_currency": "synthetic currency/year",
    "annual_fixed_cost_per_relay_currency": "synthetic currency/year/relay",
    "annual_operating_cost_per_relay_currency": "synthetic currency/year/relay",
    "minimum_hop_count": "hop",
    "maximum_hop_count": "hop",
    "synthetic_geometric_exponent": "dimensionless exponent",
    "pulse_cost_convention": "text",
    "false_trigger_relay_pulse_cost_convention": "text",
    "target_probability_min": "probability",
    "target_probability_max": "probability",
    "target_probability_sample_count": "sample",
    "pulse_energy_min_j": "J",
    "pulse_energy_max_j": "J",
    "pulse_energy_sample_count": "sample",
    "count_threshold": "count",
    "background_mean_event_per_gate": "qualifying event/gate",
    "trigger_rate_min_hz": "qualifying event/s",
    "trigger_rate_max_hz": "qualifying event/s",
    "trigger_rate_sample_count": "sample",
    "background_rate_hz": "qualifying event/s",
}


def figure_parameter_rows() -> list[dict[str, str]]:
    """Return stable CSV-ready figure parameters with evidence labels."""

    rows: list[dict[str, str]] = []
    for figure, parameters in FIGURE_INPUTS.items():
        for parameter, value in parameters.items():
            if isinstance(value, tuple):
                display_value = ";".join(f"{item:.12g}" for item in value)
            else:
                display_value = f"{value:.12g}" if isinstance(value, float) else str(value)
            if parameter == "stancil_anchor_signal_mean_event_per_gate":
                evidence_status = "PRIMARY_PAPER_ANCHOR"
                notes = (
                    "Lambda_s=0.81 is anchored to Stancil et al. (2012); this does not "
                    "make the paired background or ROC regime empirical."
                )
            elif parameter in {
                "mean_spherical_earth_radius_m",
                "surface_path_speed_m_s",
                "chord_path_speed_m_s",
            }:
                evidence_status = "MODEL_CONSTANT"
                notes = "Geometry-model input; the plotted comparison remains idealized."
            else:
                evidence_status = "SYNTHETIC"
                notes = "SIMULATION_ONLY; illustrative assumption; not measured system performance."
            rows.append(
                {
                    "figure": figure,
                    "parameter": parameter,
                    "value": display_value,
                    "unit": _UNITS.get(parameter, "dimensionless"),
                    "evidence_status": evidence_status,
                    "notes": notes,
                }
            )
    return rows
