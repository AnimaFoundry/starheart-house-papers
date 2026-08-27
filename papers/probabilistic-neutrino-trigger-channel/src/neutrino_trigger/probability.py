"""Independent-particle and Poisson-limit probability calculations."""

from __future__ import annotations

import math
from numbers import Integral, Real

from .parameters import nonnegative, nonnegative_integer, probability


def exact_at_least_one(emitted_particles: Integral, p_eff: Real) -> float:
    """Return ``1 - (1 - p_eff)**emitted_particles`` stably.

    The result assumes independent particles with a constant per-particle
    probability of producing a qualifying reconstructed event in the gate.
    """

    particles = nonnegative_integer(emitted_particles, "emitted_particles")
    p = probability(p_eff, "p_eff")
    if particles == 0 or p == 0.0:
        return 0.0
    if p == 1.0:
        return 1.0
    try:
        exponent = particles * math.log1p(-p)
    except OverflowError:
        return 1.0
    if math.isinf(exponent):
        return 1.0
    return -math.expm1(exponent)


def poisson_at_least_one(expected_events: Real) -> float:
    """Return the threshold-one Poisson probability ``1 - exp(-lambda)``."""

    mean = nonnegative(expected_events, "expected_events")
    return -math.expm1(-mean)


def poisson_limit_at_least_one(emitted_particles: Integral, p_eff: Real) -> float:
    """Approximate independent trials by a Poisson mean ``N * p_eff``."""

    particles = nonnegative_integer(emitted_particles, "emitted_particles")
    p = probability(p_eff, "p_eff")
    try:
        expected = particles * p
    except OverflowError:
        return 1.0
    if math.isinf(expected):
        return 1.0
    return poisson_at_least_one(expected)


def poisson_approximation_error(emitted_particles: Integral, p_eff: Real) -> float:
    """Return Poisson approximation minus the exact binomial result."""

    return poisson_limit_at_least_one(emitted_particles, p_eff) - exact_at_least_one(
        emitted_particles, p_eff
    )


def on_off_keying_ber(
    signal_mean: Real,
    background_mean: Real = 0.0,
    prior_one: Real = 0.5,
) -> float:
    """Uncoded threshold-one on-off-keying bit error probability.

    A count triggers a decoded one.  Consequently, errors comprise a missed one
    and a background-triggered zero.  This is a per-symbol communication metric,
    not an economic decision objective.
    """

    signal = nonnegative(signal_mean, "signal_mean")
    background = nonnegative(background_mean, "background_mean")
    p_one = probability(prior_one, "prior_one")
    miss_one = math.exp(-(signal + background))
    false_one = -math.expm1(-background)
    return p_one * miss_one + (1.0 - p_one) * false_one


def ook_capacity_bits_per_pulse(signal_mean: Real) -> float:
    """Zero-background OOK Poisson capacity used by Stancil et al. (2012).

    This reproduces Eq. (2) of arXiv:1203.2847v2.  It is not a capacity formula
    for the deadline-constrained hybrid trigger with background or authentication.
    """

    mean = nonnegative(signal_mean, "signal_mean")
    if mean == 0.0:
        return 0.0
    detection = -math.expm1(-mean)
    if mean > 700.0:
        exponent = 0.0
    else:
        exponent = -mean / math.expm1(mean)
    return math.log2(1.0 + detection * math.exp(exponent))
