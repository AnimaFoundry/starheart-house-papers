#!/usr/bin/env python3
"""Build all deterministic SIMULATION_ONLY figures for the concept paper."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(PROJECT_ROOT / ".matplotlib-cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import BoundaryNorm  # noqa: E402
import numpy as np  # noqa: E402


SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from neutrino_trigger.detection import roc_curve  # noqa: E402
from neutrino_trigger.figure_inputs import FIGURE_INPUTS  # noqa: E402
from neutrino_trigger.geometry import (  # noqa: E402
    SPEED_OF_LIGHT_M_S,
)


NOTICE = "SIMULATION_ONLY · Illustrative assumptions; not measured system performance"
FIGURE_NAMES = (
    "01_binomial_vs_poisson.png",
    "02_deadline_detection.png",
    "03_roc_curves.png",
    "04_arc_chord_advantage.png",
    "05_incremental_value.png",
    "06_relay_phase_diagram.png",
    "07_events_per_joule_break_even.png",
    "08_hybrid_channel_comparison.png",
)


def _configure() -> None:
    plt.rcParams.update(
        {
            "figure.figsize": (8.0, 5.0),
            "figure.dpi": 120,
            "savefig.dpi": 180,
            "font.size": 10,
            "axes.grid": True,
            "grid.alpha": 0.25,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "legend.frameon": False,
        }
    )


def _save(
    fig: plt.Figure,
    output_dir: Path,
    filename: str,
    *,
    right_margin: float = 0.94,
) -> Path:
    fig.text(
        0.5,
        0.012,
        NOTICE,
        ha="center",
        va="bottom",
        color="#9b1c31",
        fontsize=9,
        fontweight="bold",
        bbox={"facecolor": "white", "edgecolor": "#9b1c31", "alpha": 0.94, "pad": 3},
    )
    # A fixed margin works for standard, twin-axis, and colorbar figures without
    # the incompatible-Axes warning emitted by ``tight_layout``.
    fig.subplots_adjust(
        left=0.10,
        right=right_margin,
        bottom=0.17,
        top=0.90,
        wspace=0.30,
        hspace=0.30,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / filename
    fig.savefig(
        path,
        bbox_inches="tight",
        metadata={
            "Software": "neutrino-trigger deterministic simulator",
            "Title": filename,
            "Description": NOTICE,
        },
    )
    plt.close(fig)
    return path


def _binomial_vs_poisson(output_dir: Path) -> Path:
    inputs = FIGURE_INPUTS["01_binomial_vs_poisson"]
    p_eff = float(inputs["p_eff"])
    particles = np.arange(
        int(inputs["particle_count_min"]),
        int(inputs["particle_count_max"]) + 1,
        dtype=float,
    )
    exact = -np.expm1(particles * np.log1p(-p_eff))
    poisson = -np.expm1(-particles * p_eff)
    fig, axes = plt.subplots(2, 1, figsize=(8.0, 6.4), sharex=True, height_ratios=(3, 1))
    axes[0].plot(particles * p_eff, exact, label="Exact binomial", linewidth=2)
    axes[0].plot(particles * p_eff, poisson, "--", label="Poisson approximation", linewidth=2)
    axes[0].set_ylabel("P(at least one qualifying event)")
    axes[0].set_title(r"Independent-particle detection ($p_{eff}=10^{-3}$)")
    axes[0].legend()
    axes[1].plot(particles * p_eff, exact - poisson, color="#a23b72")
    axes[1].set_xlabel(r"Expected qualifying events $N_\nu p_{eff}$")
    axes[1].set_ylabel("Exact − Poisson")
    return _save(fig, output_dir, FIGURE_NAMES[0])


def _deadline_detection(output_dir: Path) -> Path:
    inputs = FIGURE_INPUTS["02_deadline_detection"]
    time_s = np.linspace(
        float(inputs["deadline_min_s"]),
        float(inputs["deadline_max_s"]),
        int(inputs["sample_count"]),
    )
    rates = tuple(float(rate) for rate in inputs["effective_rates_hz"])
    fig, ax = plt.subplots()
    for rate in rates:
        ax.plot(time_s * 1e3, -np.expm1(-rate * time_s), label=f"{rate:g} events/s")
    ax.set_xlabel("Decision deadline (ms)")
    ax.set_ylabel("Threshold-one detection probability")
    ax.set_ylim(0.0, 1.01)
    ax.set_title("Qualifying-event arrival before a hard deadline")
    ax.legend(title="Synthetic effective rate")
    return _save(fig, output_dir, FIGURE_NAMES[1])


def _roc_curves(output_dir: Path) -> Path:
    inputs = FIGURE_INPUTS["03_roc_curves"]
    regimes = [
        (
            float(inputs["stancil_anchor_signal_mean_event_per_gate"]),
            float(inputs["anchor_regime_synthetic_background_mean_event_per_gate"]),
            "λs=0.81 (2012 anchor), λb=0.01 (synthetic)",
            {"color": "black", "linestyle": "--", "linewidth": 2.4, "marker": "D"},
        )
    ]
    regimes.extend(
        (
            float(signal),
            float(background),
            f"λs={signal:g}, λb={background:g} (synthetic)",
            {"linewidth": 1.8, "marker": "o"},
        )
        for signal, background in zip(
            inputs["synthetic_signal_means_event_per_gate"],
            inputs["synthetic_background_means_event_per_gate"],
            strict=True,
        )
    )
    fig, ax = plt.subplots()
    for signal, background, label, style in regimes:
        roc = roc_curve(
            signal,
            background,
            max_threshold=int(inputs["maximum_count_threshold"]),
        )
        ax.step(
            roc.false_alarm_probability,
            roc.detection_probability,
            where="post",
            markersize=3,
            label=label,
            **style,
        )
    ax.set_xscale("symlog", linthresh=1e-8)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.01)
    ax.set_xlabel("False-trigger probability per gate")
    ax.set_ylabel("Detection probability per signal gate")
    ax.set_title("Poisson ROC curves with an anchor-derived signal mean")
    ax.legend(title="Signal/background gate means", fontsize=8)
    ax.text(
        0.98,
        0.04,
        "Only λs=0.81 is anchor-derived; every plotted λb is synthetic.",
        transform=ax.transAxes,
        ha="right",
        fontsize=8.5,
    )
    return _save(fig, output_dir, FIGURE_NAMES[2])


def _arc_chord_advantage(output_dir: Path) -> Path:
    inputs = FIGURE_INPUTS["04_arc_chord_advantage"]
    degrees = np.linspace(
        float(inputs["central_angle_min_degree"]),
        float(inputs["central_angle_max_degree"]),
        int(inputs["sample_count"]),
    )
    radians = np.deg2rad(degrees)
    radius_m = float(inputs["mean_spherical_earth_radius_m"])
    arc = radius_m * radians
    chord = 2.0 * radius_m * np.sin(radians / 2.0)
    advantage_ms = (
        arc / float(inputs["surface_path_speed_m_s"])
        - chord / float(inputs["chord_path_speed_m_s"])
    ) * 1e3
    fig, ax = plt.subplots()
    ax.plot(degrees, advantage_ms, linewidth=2)
    ax.set_xlabel("Endpoint central-angle separation (degrees)")
    ax.set_ylabel("Ideal arc minus chord propagation time (ms)")
    ax.set_title("Geometry-only upper bound on direct-chord propagation advantage")
    ax.text(
        0.02,
        0.95,
        "Both paths evaluated at c;\nno source, detector, route, or decision latency",
        transform=ax.transAxes,
        va="top",
        fontsize=9,
    )
    return _save(fig, output_dir, FIGURE_NAMES[3])


def _incremental_value(output_dir: Path) -> Path:
    inputs = FIGURE_INPUTS["05_incremental_value"]
    detection = np.linspace(
        float(inputs["detection_probability_min"]),
        float(inputs["detection_probability_max"]),
        int(inputs["detection_probability_sample_count"]),
    )
    false_alarm = np.logspace(
        np.log10(float(inputs["false_alarm_probability_min"])),
        np.log10(float(inputs["false_alarm_probability_max"])),
        int(inputs["false_alarm_probability_sample_count"]),
    )
    pd_grid, pfa_grid = np.meshgrid(detection, false_alarm)
    pulse_costs = tuple(float(cost) for cost in inputs["pulse_costs_currency_per_valid_window"])
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.6), sharey=True)
    extrema = []
    values = []
    for pulse_cost in pulse_costs:
        annual = (
            float(inputs["valid_windows_per_year"])
            * (
                pd_grid * float(inputs["fallback_relative_gain_currency_per_success"])
                - pulse_cost
            )
            - float(inputs["null_windows_per_year"])
            * pfa_grid
            * float(inputs["false_trigger_loss_currency"])
            - float(inputs["annual_fixed_cost_currency"])
            - float(inputs["annual_operating_cost_currency"])
        ) / 1e6
        values.append(annual)
        extrema.extend([float(np.nanmin(annual)), float(np.nanmax(annual))])
    bound = max(abs(min(extrema)), abs(max(extrema)))
    levels = np.linspace(-bound, bound, 31)
    image = None
    for ax, pulse_cost, annual in zip(axes, pulse_costs, values, strict=True):
        image = ax.contourf(pd_grid, pfa_grid, annual, levels=levels, cmap="RdBu", extend="both")
        ax.contour(pd_grid, pfa_grid, annual, levels=[0.0], colors="black", linewidths=1.5)
        ax.set_yscale("log")
        ax.set_xlabel(r"$P_D$ before EM deadline")
        ax.set_title(f"Pulse cost = {pulse_cost:g}")
    axes[0].set_ylabel(r"$P_{FA}$ per null window")
    assert image is not None
    colorbar_axis = fig.add_axes((0.90, 0.20, 0.015, 0.62))
    colorbar = fig.colorbar(image, cax=colorbar_axis)
    colorbar.set_label("Annual incremental value (million arbitrary currency)")
    fig.suptitle("Incremental value sensitivity versus fallback baseline", y=1.01)
    return _save(fig, output_dir, FIGURE_NAMES[4], right_margin=0.87)


def _relay_phase_diagram(output_dir: Path) -> Path:
    inputs = FIGURE_INPUTS["06_relay_phase_diagram"]
    direct_means = np.logspace(
        np.log10(float(inputs["direct_signal_mean_min_event_per_gate"])),
        np.log10(float(inputs["direct_signal_mean_max_event_per_gate"])),
        int(inputs["direct_signal_mean_sample_count"]),
    )
    relay_delays = np.logspace(
        np.log10(float(inputs["relay_regeneration_delay_min_s"])),
        np.log10(float(inputs["relay_regeneration_delay_max_s"])),
        int(inputs["relay_regeneration_delay_sample_count"]),
    )
    mean_grid, delay_grid = np.meshgrid(direct_means, relay_delays)
    total_distance_m = float(inputs["total_distance_m"])
    endpoint_delay_s = float(inputs["endpoint_delay_s"])
    em_fallback_deadline_s = float(inputs["em_fallback_deadline_s"])
    value_decay_s = float(inputs["value_decay_s"])
    initial_gross_value_currency = float(inputs["initial_gross_value_currency"])
    valid_windows_per_year = float(inputs["valid_windows_per_year"])
    null_windows_per_year = float(inputs["null_windows_per_year"])
    false_trigger_loss_currency = float(inputs["false_trigger_loss_currency"])
    first_hop_false_origin_probability = float(
        inputs["first_hop_false_origin_probability"]
    )
    pulse_cost_per_hop_currency = float(inputs["pulse_cost_per_hop_currency"])
    base_annual_fixed_cost_currency = float(inputs["base_annual_fixed_cost_currency"])
    base_annual_operating_cost_currency = float(inputs["base_annual_operating_cost_currency"])
    annual_fixed_cost_per_relay_currency = float(
        inputs["annual_fixed_cost_per_relay_currency"]
    )
    annual_operating_cost_per_relay_currency = float(
        inputs["annual_operating_cost_per_relay_currency"]
    )
    annual_values = []
    for hops in range(
        int(inputs["minimum_hop_count"]),
        int(inputs["maximum_hop_count"]) + 1,
    ):
        hop_mean = mean_grid * hops ** float(inputs["synthetic_geometric_exponent"])
        per_hop_pd = -np.expm1(-hop_mean)
        end_pd = per_hop_pd**hops
        latency = (
            total_distance_m / SPEED_OF_LIGHT_M_S
            + (hops - 1) * delay_grid
            + endpoint_delay_s
        )
        fallback_relative_gain = initial_gross_value_currency * np.maximum(
            0.0,
            np.exp(-latency / value_decay_s)
            - np.exp(-em_fallback_deadline_s / value_decay_s),
        )
        # Named causal example: a false origin can occur only at the first hop;
        # every downstream site must then detect the regenerated signal.
        supplied_end_to_end_pfa = (
            first_hop_false_origin_probability * per_hop_pd ** (hops - 1)
        )
        pulse_cost_per_valid_window = hops * pulse_cost_per_hop_currency
        annual_fixed_cost = (
            base_annual_fixed_cost_currency
            + (hops - 1) * annual_fixed_cost_per_relay_currency
        )
        annual_operating_cost = (
            base_annual_operating_cost_currency
            + (hops - 1) * annual_operating_cost_per_relay_currency
        )
        annual_value = (
            valid_windows_per_year
            * (end_pd * fallback_relative_gain - pulse_cost_per_valid_window)
            - null_windows_per_year
            * supplied_end_to_end_pfa
            * false_trigger_loss_currency
            - annual_fixed_cost
            - annual_operating_cost
        )
        annual_values.append(annual_value)
    value_stack = np.stack(annual_values, axis=0)
    best_hops = np.argmax(value_stack, axis=0) + 1
    best_hops[np.max(value_stack, axis=0) < 0.0] = 0
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    maximum_hops = int(inputs["maximum_hop_count"])
    cmap = plt.get_cmap("viridis", maximum_hops + 1)
    norm = BoundaryNorm(np.arange(-0.5, maximum_hops + 1.5, 1.0), cmap.N)
    mesh = ax.pcolormesh(direct_means, relay_delays * 1e6, best_hops, cmap=cmap, norm=norm, shading="auto")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Direct-link signal mean per pulse")
    ax.set_ylabel("Complete regeneration delay per relay (µs)")
    ax.set_title("Annual-value-maximizing hop count under synthetic geometric scaling")
    colorbar = fig.colorbar(mesh, ax=ax, ticks=np.arange(0, maximum_hops + 1))
    colorbar.set_label("Optimal hop count (0 = no positive annual value; 1 = direct)")
    ax.text(
        0.02,
        0.03,
        (
            r"Equal hops; $\lambda_{hop}=\lambda_{direct}h^2$; independent-hop approximation"
            "\nFirst-hop-only false origin; all-hop valid-window pulse cost; false-origin relay pulse cost excluded"
            "\nAnnual objective: gains and costs in one consistent synthetic currency/year"
        ),
        transform=ax.transAxes,
        fontsize=8.0,
        color="white",
        bbox={"facecolor": "black", "alpha": 0.65, "edgecolor": "none"},
    )
    return _save(fig, output_dir, FIGURE_NAMES[5])


def _events_per_joule_break_even(output_dir: Path) -> Path:
    inputs = FIGURE_INPUTS["07_events_per_joule_break_even"]
    if int(inputs["count_threshold"]) != 1 or float(
        inputs["background_mean_event_per_gate"]
    ) != 0.0:
        raise ValueError("figure 7 derivation requires threshold one and zero background")
    target_probability = np.linspace(
        float(inputs["target_probability_min"]),
        float(inputs["target_probability_max"]),
        int(inputs["target_probability_sample_count"]),
    )
    pulse_energy_j = np.logspace(
        np.log10(float(inputs["pulse_energy_min_j"])),
        np.log10(float(inputs["pulse_energy_max_j"])),
        int(inputs["pulse_energy_sample_count"]),
    )
    q_grid, energy_grid = np.meshgrid(target_probability, pulse_energy_j)
    required_events_per_joule = -np.log1p(-q_grid) / energy_grid
    log_yield = np.log10(required_events_per_joule)
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    levels = np.arange(-16.0, -1.0, 1.0)
    filled = ax.contourf(q_grid, energy_grid, log_yield, levels=levels, cmap="magma", extend="both")
    contours = ax.contour(q_grid, energy_grid, log_yield, levels=levels[::2], colors="white", linewidths=0.6)
    ax.clabel(contours, fmt=lambda value: rf"$10^{{{value:.0f}}}$", fontsize=8)
    ax.set_yscale("log")
    ax.set_xlabel("Target threshold-one detection probability")
    ax.set_ylabel("Signaling-pulse energy (J)")
    ax.set_title("Required qualifying-event yield per joule per decision window")
    colorbar = fig.colorbar(filled, ax=ax)
    colorbar.set_label(r"$\log_{10}$ required qualifying events/J")
    ax.text(
        0.02,
        0.03,
        "Zero background; all qualifying events assigned to one decision gate",
        transform=ax.transAxes,
        fontsize=8.5,
        color="white",
        bbox={"facecolor": "black", "alpha": 0.65, "edgecolor": "none"},
    )
    return _save(fig, output_dir, FIGURE_NAMES[6])


def _hybrid_channel_comparison(output_dir: Path) -> Path:
    inputs = FIGURE_INPUTS["08_hybrid_channel_comparison"]
    if int(inputs["count_threshold"]) != 1 or float(inputs["background_rate_hz"]) != 0.0:
        raise ValueError("figure 8 closed form requires threshold one and zero background")
    em_deadline_s = float(inputs["em_fallback_deadline_s"])
    fixed_latency_s = float(inputs["fixed_neutrino_latency_s"])
    evidence_budget_s = em_deadline_s - fixed_latency_s
    if evidence_budget_s <= 0.0:
        raise ValueError("figure 8 fixed latency must be below the EM deadline")
    trigger_rates = np.logspace(
        np.log10(float(inputs["trigger_rate_min_hz"])),
        np.log10(float(inputs["trigger_rate_max_hz"])),
        int(inputs["trigger_rate_sample_count"]),
    )
    detection = -np.expm1(-trigger_rates * evidence_budget_s)
    hybrid_latency_s = fixed_latency_s + detection / trigger_rates
    conventional_latency_s = np.full_like(trigger_rates, em_deadline_s)
    fig, ax = plt.subplots()
    ax.plot(
        trigger_rates,
        conventional_latency_s * 1e3,
        label="Conventional-only action",
        linewidth=2,
    )
    ax.plot(
        trigger_rates,
        hybrid_latency_s * 1e3,
        label="Early trigger or EM fallback",
        linewidth=2,
    )
    ax.set_xscale("log")
    ax.set_xlabel("Synthetic qualifying-event rate under H1 (event/s)")
    ax.set_ylabel("Expected request-to-action latency (ms)")
    ax.set_title("Fallback caps latency after a synthetic fixed trigger overhead")
    ax.legend(loc="upper right")
    second = ax.twinx()
    second.plot(trigger_rates, detection, color="#777777", linestyle=":", label="P(early trigger)")
    second.set_ylabel("Probability actionable evidence arrives before 1 ms")
    second.set_ylim(0.0, 1.02)
    second.grid(False)
    ax.text(
        0.02,
        0.05,
        f"Fixed non-evidence neutrino-path latency = {fixed_latency_s * 1e3:.1f} ms",
        transform=ax.transAxes,
        fontsize=8.5,
    )
    return _save(fig, output_dir, FIGURE_NAMES[7])


def build(output_dir: Path) -> tuple[Path, ...]:
    """Build all figures in a stable order and return their paths."""

    _configure()
    builders = (
        _binomial_vs_poisson,
        _deadline_detection,
        _roc_curves,
        _arc_chord_advantage,
        _incremental_value,
        _relay_phase_diagram,
        _events_per_joule_break_even,
        _hybrid_channel_comparison,
    )
    return tuple(builder(output_dir) for builder in builders)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "figures",
        help="output directory (default: figures)",
    )
    return parser


def main() -> None:
    args = _parser().parse_args()
    for path in build(args.output_dir):
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
