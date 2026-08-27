"""Deadline-constrained first- and m-th-arrival distributions."""

from __future__ import annotations

import math
from numbers import Integral, Real

from scipy.special import gammainc, gammaincinv, gammaln

from .parameters import (
    nonnegative,
    nonnegative_integer,
    positive,
    positive_integer,
    probability,
)


def arrival_cdf(rate_hz: Real, time_s: Real, threshold: Integral = 1) -> float:
    """Return ``P(T_m <= time_s)`` for a homogeneous Poisson event process."""

    rate = nonnegative(rate_hz, "rate_hz")
    time = nonnegative(time_s, "time_s")
    m = positive_integer(threshold, "threshold")
    if rate == 0.0 or time == 0.0:
        return 0.0
    return float(gammainc(m, rate * time))


def arrival_survival(rate_hz: Real, time_s: Real, threshold: Integral = 1) -> float:
    """Return ``P(T_m > time_s)``."""

    return 1.0 - arrival_cdf(rate_hz, time_s, threshold)


def arrival_pdf(rate_hz: Real, time_s: Real, threshold: Integral = 1) -> float:
    """Density of the m-th arrival time (an Erlang distribution)."""

    rate = nonnegative(rate_hz, "rate_hz")
    time = nonnegative(time_s, "time_s")
    m = positive_integer(threshold, "threshold")
    if rate == 0.0:
        return 0.0
    if time == 0.0:
        return rate if m == 1 else 0.0
    log_density = m * math.log(rate) + (m - 1) * math.log(time) - rate * time
    log_density -= float(gammaln(m))
    return math.exp(log_density)


def required_total_rate_hz(
    target_probability: Real,
    deadline_s: Real,
    threshold: Integral = 1,
) -> float:
    """Minimum total event rate for a target m-th arrival probability.

    For threshold one this reduces exactly to ``-log(1-q) / deadline_s``.
    A target of one requires an unbounded homogeneous Poisson rate and therefore
    returns positive infinity.
    """

    q = probability(target_probability, "target_probability")
    deadline = positive(deadline_s, "deadline_s")
    m = positive_integer(threshold, "threshold")
    if q == 0.0:
        return 0.0
    if q == 1.0:
        return math.inf
    if m == 1:
        return -math.log1p(-q) / deadline
    return float(gammaincinv(m, q) / deadline)


def required_signal_rate_hz(
    target_probability: Real,
    deadline_s: Real,
    background_rate_hz: Real = 0.0,
    threshold: Integral = 1,
) -> float:
    """Minimum nonnegative signal rate with a specified background rate.

    This calculation constrains H1 detection probability only.  Threshold and
    background must separately satisfy the false-trigger requirement under H0.
    """

    background = nonnegative(background_rate_hz, "background_rate_hz")
    total_required = required_total_rate_hz(target_probability, deadline_s, threshold)
    return max(0.0, total_required - background)


def expected_capped_arrival_time_s(
    rate_hz: Real,
    deadline_s: Real,
    threshold: Integral = 1,
) -> float:
    """Return ``E[min(T_m, deadline_s)]``.

    This is useful for a hybrid system that waits for the electromagnetic
    fallback when the particle trigger does not arrive by the deadline.
    """

    rate = nonnegative(rate_hz, "rate_hz")
    deadline = nonnegative(deadline_s, "deadline_s")
    m = positive_integer(threshold, "threshold")
    if rate == 0.0 or deadline == 0.0:
        return deadline
    x = rate * deadline
    return float(sum(gammainc(j + 1, x) for j in range(m)) / rate)


def conditional_mean_arrival_time_s(
    rate_hz: Real,
    deadline_s: Real,
    threshold: Integral = 1,
) -> float:
    """Return ``E[T_m | T_m <= deadline_s]``.

    Raises ``ValueError`` if arrival before the deadline has zero probability.
    """

    rate = nonnegative(rate_hz, "rate_hz")
    deadline = nonnegative(deadline_s, "deadline_s")
    m = positive_integer(threshold, "threshold")
    detected = arrival_cdf(rate, deadline, m)
    if detected == 0.0:
        raise ValueError("conditional mean is undefined when deadline detection probability is zero")
    truncated_first_moment = m * gammainc(m + 1, rate * deadline) / rate
    return float(truncated_first_moment / detected)


def sample_arrival_times_s(
    rate_hz: Real,
    threshold: Integral,
    size: Integral,
    seed: Integral = 20260826,
):
    """Draw deterministic Erlang samples for validation or Monte Carlo studies."""

    import numpy as np

    rate = positive(rate_hz, "rate_hz")
    m = positive_integer(threshold, "threshold")
    sample_size = positive_integer(size, "size")
    random_seed = nonnegative_integer(seed, "seed")
    rng = np.random.default_rng(random_seed)
    return rng.gamma(shape=m, scale=1.0 / rate, size=sample_size)
