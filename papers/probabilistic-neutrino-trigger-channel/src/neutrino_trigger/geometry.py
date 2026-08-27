"""Spherical-Earth path geometry and subluminal neutrino time of flight."""

from __future__ import annotations

import math
from numbers import Real

from .parameters import finite_float, nonnegative, positive


SPEED_OF_LIGHT_M_S = 299_792_458.0
"""Exact SI speed of light in vacuum, in metres per second."""

MEAN_EARTH_RADIUS_M = 6_371_000.0
"""PREM reference radius used for the paper's illustrative spherical geometry."""


def _central_angle(value: Real) -> float:
    angle = finite_float(value, "central_angle_rad")
    if not 0.0 <= angle <= math.pi:
        raise ValueError("central_angle_rad must be between 0 and pi")
    return angle


def earth_arc_length_m(
    central_angle_rad: Real,
    earth_radius_m: Real = MEAN_EARTH_RADIUS_M,
) -> float:
    """Great-circle surface arc length ``R * theta``."""

    angle = _central_angle(central_angle_rad)
    radius = positive(earth_radius_m, "earth_radius_m")
    return radius * angle


def earth_chord_length_m(
    central_angle_rad: Real,
    earth_radius_m: Real = MEAN_EARTH_RADIUS_M,
) -> float:
    """Straight Earth chord length ``2 R sin(theta / 2)``."""

    angle = _central_angle(central_angle_rad)
    radius = positive(earth_radius_m, "earth_radius_m")
    return 2.0 * radius * math.sin(angle / 2.0)


def propagation_time_s(path_length_m: Real, speed_m_s: Real) -> float:
    """Propagation time for an explicit path length and speed."""

    length = nonnegative(path_length_m, "path_length_m")
    speed = positive(speed_m_s, "speed_m_s")
    return length / speed


def relativistic_speed_m_s(rest_energy_ev: Real, total_energy_ev: Real) -> float:
    """Relativistic particle speed from rest and total energies.

    ``rest_energy_ev`` means ``m c^2`` expressed in eV, not a bare mass.  The
    returned speed never exceeds ``c``.  For extreme ratios floating-point
    rounding may make the returned value numerically equal to ``c``; use
    :func:`time_delay_from_light_s` for a stable small-delay calculation.
    """

    rest = nonnegative(rest_energy_ev, "rest_energy_ev")
    energy = positive(total_energy_ev, "total_energy_ev")
    if rest > energy:
        raise ValueError("total_energy_ev must be at least the rest energy")
    ratio = rest / energy
    return SPEED_OF_LIGHT_M_S * math.sqrt(max(0.0, 1.0 - ratio * ratio))


def time_delay_from_light_s(
    path_length_m: Real,
    rest_energy_ev: Real,
    total_energy_ev: Real,
) -> float:
    """Stable positive time-of-flight delay relative to light in vacuum."""

    length = nonnegative(path_length_m, "path_length_m")
    rest = nonnegative(rest_energy_ev, "rest_energy_ev")
    energy = positive(total_energy_ev, "total_energy_ev")
    if rest > energy:
        raise ValueError("total_energy_ev must be at least the rest energy")
    if length == 0.0 or rest == 0.0:
        return 0.0
    ratio_squared = (rest / energy) ** 2
    if ratio_squared < 1.0e-8:
        inverse_beta_minus_one = (
            0.5 * ratio_squared
            + 0.375 * ratio_squared**2
            + 0.3125 * ratio_squared**3
        )
    elif ratio_squared < 1.0:
        inverse_beta_minus_one = 1.0 / math.sqrt(1.0 - ratio_squared) - 1.0
    else:
        return math.inf
    return (length / SPEED_OF_LIGHT_M_S) * inverse_beta_minus_one


def neutrino_time_of_flight_s(
    path_length_m: Real,
    rest_energy_ev: Real,
    total_energy_ev: Real,
) -> float:
    """Subluminal time of flight using a stable high-energy correction."""

    length = nonnegative(path_length_m, "path_length_m")
    return length / SPEED_OF_LIGHT_M_S + time_delay_from_light_s(
        length, rest_energy_ev, total_energy_ev
    )


def ideal_arc_chord_advantage_s(
    central_angle_rad: Real,
    surface_speed_m_s: Real = SPEED_OF_LIGHT_M_S,
    chord_speed_m_s: Real = SPEED_OF_LIGHT_M_S,
    earth_radius_m: Real = MEAN_EARTH_RADIUS_M,
) -> float:
    """Ideal surface-arc propagation time minus direct-chord time.

    This geometry-only quantity excludes routing stretch, source and detector
    siting, actuation, evidence accumulation, and network processing.
    """

    arc = earth_arc_length_m(central_angle_rad, earth_radius_m)
    chord = earth_chord_length_m(central_angle_rad, earth_radius_m)
    return propagation_time_s(arc, surface_speed_m_s) - propagation_time_s(
        chord, chord_speed_m_s
    )
