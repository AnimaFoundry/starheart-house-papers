"""Poisson count detection, ROC, Bayesian, and sequential decision tools."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
import math
from numbers import Integral, Real

import numpy as np
from scipy.special import gammaln
from scipy.stats import poisson

from .parameters import (
    nonnegative,
    nonnegative_integer,
    positive,
    probability,
)


def poisson_tail(mean: Real, threshold: Integral) -> float:
    """Return ``P(K >= threshold)`` for ``K ~ Poisson(mean)``."""

    lam = nonnegative(mean, "mean")
    m = nonnegative_integer(threshold, "threshold")
    if m == 0:
        return 1.0
    return float(poisson.sf(m - 1, lam))


def detection_probability(
    signal_mean: Real,
    background_mean: Real = 0.0,
    threshold: Integral = 1,
) -> float:
    """Probability of a count trigger under ``H1``."""

    signal = nonnegative(signal_mean, "signal_mean")
    background = nonnegative(background_mean, "background_mean")
    return poisson_tail(signal + background, threshold)


def false_alarm_probability(background_mean: Real, threshold: Integral = 1) -> float:
    """Probability of a count trigger under ``H0``."""

    return poisson_tail(background_mean, threshold)


def all_symbols_sequence_success_probability(
    per_symbol_detection_probability: Real,
    required_symbols: Integral,
) -> float:
    """Success probability when every authenticated symbol must be detected.

    The power law assumes conditionally independent symbol decisions.  Real
    codebooks, correlated detector failures, and replay defenses require a more
    detailed model; callers must not treat this as universal authentication.
    """

    per_symbol = probability(
        per_symbol_detection_probability,
        "per_symbol_detection_probability",
    )
    symbols = nonnegative_integer(required_symbols, "required_symbols")
    return per_symbol**symbols


@dataclass(frozen=True, slots=True)
class AuthenticatedSequenceProbabilities:
    """Sequence-level actionable probabilities under an independence model."""

    detection_probability: float
    false_alarm_probability: float


def authenticated_sequence_actionable_probabilities(
    availability_probability: Real,
    positive_slot_detection_probabilities: Sequence[Real],
    positive_slot_false_alarm_probabilities: Sequence[Real],
    guard_slot_false_alarm_probabilities: Sequence[Real] = (),
) -> AuthenticatedSequenceProbabilities:
    """Compute actionable authentication PD and PFA for prescribed slots.

    Under conditional independence,

    ``PD_A = P_avail * prod(d_r) * prod(1-u_guard)`` and
    ``PFA_A = P_avail * prod(u_r) * prod(1-u_guard)``.

    At least one prescribed positive slot is required; guard slots may be empty.
    The model does not cover correlated faults, replay, or timing-gate mismatch.
    """

    availability = probability(availability_probability, "availability_probability")
    detections = tuple(positive_slot_detection_probabilities)
    positive_false_alarms = tuple(positive_slot_false_alarm_probabilities)
    guards = tuple(guard_slot_false_alarm_probabilities)
    if not detections:
        raise ValueError("at least one prescribed positive slot is required")
    if len(detections) != len(positive_false_alarms):
        raise ValueError("positive-slot detection and false-alarm shapes must match")
    validated_detections = tuple(
        probability(value, f"positive_slot_detection_probabilities[{index}]")
        for index, value in enumerate(detections)
    )
    validated_positive_false_alarms = tuple(
        probability(value, f"positive_slot_false_alarm_probabilities[{index}]")
        for index, value in enumerate(positive_false_alarms)
    )
    validated_guards = tuple(
        probability(value, f"guard_slot_false_alarm_probabilities[{index}]")
        for index, value in enumerate(guards)
    )
    guard_survival = math.prod(1.0 - value for value in validated_guards)
    return AuthenticatedSequenceProbabilities(
        availability * math.prod(validated_detections) * guard_survival,
        availability * math.prod(validated_positive_false_alarms) * guard_survival,
    )


@dataclass(frozen=True, slots=True)
class ROCCurve:
    """Discrete ROC points indexed by integer count thresholds."""

    thresholds: np.ndarray
    detection_probability: np.ndarray
    false_alarm_probability: np.ndarray


def roc_curve(
    signal_mean: Real,
    background_mean: Real,
    max_threshold: Integral | None = None,
) -> ROCCurve:
    """Compute the complete useful discrete-threshold ROC sequence.

    Threshold zero (always trigger) is included.  If ``max_threshold`` is not
    supplied, a conservative tail cutoff is selected from the H1 mean.
    """

    signal = nonnegative(signal_mean, "signal_mean")
    background = nonnegative(background_mean, "background_mean")
    total = signal + background
    if max_threshold is None:
        maximum = max(10, int(math.ceil(total + 10.0 * math.sqrt(total + 1.0) + 5.0)))
    else:
        maximum = nonnegative_integer(max_threshold, "max_threshold")
    thresholds = np.arange(maximum + 1, dtype=int)
    pd = np.asarray([detection_probability(signal, background, int(m)) for m in thresholds])
    pfa = np.asarray([false_alarm_probability(background, int(m)) for m in thresholds])
    return ROCCurve(thresholds, pd, pfa)


def _poisson_log_pmf(count: int, mean: float) -> float:
    if mean == 0.0:
        return 0.0 if count == 0 else -math.inf
    return count * math.log(mean) - mean - float(gammaln(count + 1.0))


def posterior_signal_probability(
    count: Integral,
    signal_mean: Real,
    background_mean: Real,
    prior_signal: Real,
) -> float:
    """Return ``P(H1 | K=count)`` for two Poisson hypotheses."""

    k = nonnegative_integer(count, "count")
    signal = nonnegative(signal_mean, "signal_mean")
    background = nonnegative(background_mean, "background_mean")
    prior = probability(prior_signal, "prior_signal")
    if prior == 0.0:
        return 0.0
    if prior == 1.0:
        return 1.0
    log_h1 = math.log(prior) + _poisson_log_pmf(k, signal + background)
    log_h0 = math.log1p(-prior) + _poisson_log_pmf(k, background)
    if math.isinf(log_h1) and math.isinf(log_h0):
        raise ValueError("observed count has zero probability under both hypotheses")
    denominator = float(np.logaddexp(log_h1, log_h0))
    return float(math.exp(log_h1 - denominator))


def conditional_incremental_utility(
    posterior_signal: Real,
    success_gain: Real,
    false_trigger_loss: Real,
    execution_cost: Real = 0.0,
) -> float:
    """Conditional utility of triggering now rather than waiting."""

    posterior = probability(posterior_signal, "posterior_signal")
    gain = nonnegative(success_gain, "success_gain")
    loss = nonnegative(false_trigger_loss, "false_trigger_loss")
    cost = nonnegative(execution_cost, "execution_cost")
    return posterior * gain - (1.0 - posterior) * loss - cost


def should_trigger(
    posterior_signal: Real,
    success_gain: Real,
    false_trigger_loss: Real,
    execution_cost: Real = 0.0,
) -> bool:
    """Return true only when conditional incremental utility is positive."""

    return (
        conditional_incremental_utility(
            posterior_signal, success_gain, false_trigger_loss, execution_cost
        )
        > 0.0
    )


def poisson_log_likelihood_ratio(
    count: Integral,
    exposure_s: Real,
    signal_rate_hz: Real,
    background_rate_hz: Real,
) -> float:
    """Log likelihood ratio for a homogeneous Poisson process observation.

    Under H0 the rate is ``background_rate_hz`` and under H1 it is the sum of
    signal and background.  Arrival times add no further information when both
    hypotheses specify homogeneous rates over the same observation interval.
    """

    k = nonnegative_integer(count, "count")
    exposure = nonnegative(exposure_s, "exposure_s")
    signal = nonnegative(signal_rate_hz, "signal_rate_hz")
    background = nonnegative(background_rate_hz, "background_rate_hz")
    if signal == 0.0:
        return 0.0
    if background == 0.0:
        return math.inf if k > 0 else -signal * exposure
    return k * math.log1p(signal / background) - signal * exposure


@dataclass(frozen=True, slots=True)
class SPRTDecision:
    """A snapshot decision for Wald likelihood-ratio boundaries."""

    decision: str
    log_likelihood_ratio: float
    lower_boundary: float
    upper_boundary: float


def sprt_decision(
    log_likelihood_ratio: Real,
    false_accept_probability: Real,
    false_reject_probability: Real,
) -> SPRTDecision:
    """Classify an LLR using conventional Wald approximate boundaries."""

    if isinstance(log_likelihood_ratio, bool) or not isinstance(log_likelihood_ratio, Real):
        raise TypeError("log_likelihood_ratio must be a real number")
    llr = float(log_likelihood_ratio)
    if math.isnan(llr):
        raise ValueError("log_likelihood_ratio must not be NaN")
    alpha = probability(false_accept_probability, "false_accept_probability")
    beta = probability(false_reject_probability, "false_reject_probability")
    if alpha in (0.0, 1.0) or beta in (0.0, 1.0):
        raise ValueError("SPRT error probabilities must be strictly between 0 and 1")
    lower = math.log(beta / (1.0 - alpha))
    upper = math.log((1.0 - beta) / alpha)
    if lower >= upper:
        raise ValueError("SPRT boundaries are not ordered for the requested errors")
    if llr >= upper:
        decision = "H1"
    elif llr <= lower:
        decision = "H0"
    else:
        decision = "continue"
    return SPRTDecision(decision, llr, lower, upper)
