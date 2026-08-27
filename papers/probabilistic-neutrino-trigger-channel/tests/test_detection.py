import math

import numpy as np
import pytest

from neutrino_trigger.detection import (
    authenticated_sequence_actionable_probabilities,
    all_symbols_sequence_success_probability,
    conditional_incremental_utility,
    detection_probability,
    false_alarm_probability,
    poisson_log_likelihood_ratio,
    poisson_tail,
    posterior_signal_probability,
    roc_curve,
    should_trigger,
    sprt_decision,
)
from neutrino_trigger.first_arrival import (
    arrival_cdf,
    arrival_pdf,
    conditional_mean_arrival_time_s,
    expected_capped_arrival_time_s,
    required_signal_rate_hz,
    required_total_rate_hz,
    sample_arrival_times_s,
)


def test_threshold_probabilities_match_closed_form() -> None:
    signal = 1.2
    background = 0.03
    assert detection_probability(signal, background, 1) == pytest.approx(
        1.0 - math.exp(-(signal + background))
    )
    assert false_alarm_probability(background, 1) == pytest.approx(1.0 - math.exp(-background))
    assert poisson_tail(100.0, 0) == 1.0


def test_higher_threshold_formula() -> None:
    mean = 2.0
    expected = 1.0 - math.exp(-mean) * (1.0 + mean)
    assert poisson_tail(mean, 2) == pytest.approx(expected)


def test_roc_is_monotone_with_threshold() -> None:
    curve = roc_curve(2.0, 0.1, max_threshold=12)
    assert curve.thresholds[0] == 0
    assert curve.detection_probability[0] == 1.0
    assert curve.false_alarm_probability[0] == 1.0
    assert np.all(np.diff(curve.detection_probability) <= 1e-15)
    assert np.all(np.diff(curve.false_alarm_probability) <= 1e-15)
    assert np.all(curve.detection_probability >= curve.false_alarm_probability)


def test_bayesian_posterior_and_utility_rule() -> None:
    posterior = posterior_signal_probability(0, 1.0, 0.1, 0.25)
    manual = 0.25 * math.exp(-1.1) / (
        0.25 * math.exp(-1.1) + 0.75 * math.exp(-0.1)
    )
    assert posterior == pytest.approx(manual)
    assert posterior_signal_probability(1, 1.0, 0.0, 0.1) == 1.0
    assert conditional_incremental_utility(0.9, 100.0, 500.0, 1.0) == pytest.approx(39.0)
    assert should_trigger(0.9, 100.0, 500.0, 1.0)
    assert not should_trigger(0.5, 100.0, 500.0, 1.0)


def test_authentication_sequence_compounds_symbol_misses() -> None:
    assert all_symbols_sequence_success_probability(0.9, 4) == pytest.approx(0.9**4)
    assert all_symbols_sequence_success_probability(0.9, 0) == 1.0


def test_authenticated_sequence_actionable_probabilities() -> None:
    result = authenticated_sequence_actionable_probabilities(
        availability_probability=0.95,
        positive_slot_detection_probabilities=[0.9, 0.8],
        positive_slot_false_alarm_probabilities=[0.01, 0.02],
        guard_slot_false_alarm_probabilities=[0.03, 0.04],
    )
    guard_survival = (1.0 - 0.03) * (1.0 - 0.04)
    assert result.detection_probability == pytest.approx(0.95 * 0.9 * 0.8 * guard_survival)
    assert result.false_alarm_probability == pytest.approx(
        0.95 * 0.01 * 0.02 * guard_survival
    )


def test_authenticated_sequence_empty_guards_and_probability_edges() -> None:
    no_guards = authenticated_sequence_actionable_probabilities(1.0, [1.0], [0.0])
    assert no_guards.detection_probability == 1.0
    assert no_guards.false_alarm_probability == 0.0
    unavailable = authenticated_sequence_actionable_probabilities(0.0, [1.0], [1.0])
    assert unavailable.detection_probability == 0.0
    assert unavailable.false_alarm_probability == 0.0
    blocked_by_guard = authenticated_sequence_actionable_probabilities(
        1.0, [1.0], [1.0], [1.0]
    )
    assert blocked_by_guard.detection_probability == 0.0
    assert blocked_by_guard.false_alarm_probability == 0.0


def test_posterior_undefined_for_impossible_observation() -> None:
    with pytest.raises(ValueError):
        posterior_signal_probability(1, 0.0, 0.0, 0.5)


def test_first_and_mth_arrival_distributions() -> None:
    rate = 20.0
    time = 0.1
    assert arrival_cdf(rate, time, 1) == pytest.approx(1.0 - math.exp(-2.0))
    assert arrival_cdf(rate, time, 2) == pytest.approx(1.0 - math.exp(-2.0) * 3.0)
    assert arrival_pdf(rate, 0.0, 1) == rate
    assert arrival_pdf(rate, 0.0, 2) == 0.0


def test_required_deadline_rate_and_background_generalization() -> None:
    q = 0.95
    deadline = 0.002
    required = required_total_rate_hz(q, deadline, 1)
    assert required == pytest.approx(-math.log(0.05) / deadline)
    assert arrival_cdf(required, deadline, 1) == pytest.approx(q)
    required_m3 = required_total_rate_hz(q, deadline, 3)
    assert arrival_cdf(required_m3, deadline, 3) == pytest.approx(q)
    signal = required_signal_rate_hz(q, deadline, 100.0, 3)
    assert arrival_cdf(signal + 100.0, deadline, 3) == pytest.approx(q)


def test_hybrid_capped_and_conditional_arrival_means() -> None:
    rate = 1_000.0
    deadline = 0.001
    expected_capped = (1.0 - math.exp(-rate * deadline)) / rate
    assert expected_capped_arrival_time_s(rate, deadline, 1) == pytest.approx(expected_capped)
    conditional = conditional_mean_arrival_time_s(rate, deadline, 1)
    assert 0.0 < conditional < deadline
    assert expected_capped_arrival_time_s(0.0, deadline, 4) == deadline


def test_seeded_arrival_samples_are_deterministic() -> None:
    first = sample_arrival_times_s(10.0, 2, 10, seed=42)
    second = sample_arrival_times_s(10.0, 2, 10, seed=42)
    assert np.array_equal(first, second)
    assert np.array_equal(
        sample_arrival_times_s(10.0, 2, 3, seed=0),
        sample_arrival_times_s(10.0, 2, 3, seed=0),
    )


def test_poisson_sprt_snapshot() -> None:
    llr = poisson_log_likelihood_ratio(4, 0.01, 100.0, 10.0)
    decision = sprt_decision(llr, 0.01, 0.05)
    assert decision.lower_boundary < decision.upper_boundary
    assert decision.decision in {"H0", "H1", "continue"}
    assert poisson_log_likelihood_ratio(0, 0.01, 100.0, 0.0) == pytest.approx(-1.0)
    assert sprt_decision(math.inf, 0.01, 0.05).decision == "H1"
    assert sprt_decision(-math.inf, 0.01, 0.05).decision == "H0"


@pytest.mark.parametrize(
    "call",
    [
        lambda: poisson_tail(-1.0, 1),
        lambda: poisson_tail(1.0, -1),
        lambda: arrival_cdf(1.0, 1.0, 0),
        lambda: required_total_rate_hz(1.1, 1.0, 1),
        lambda: required_total_rate_hz(0.5, 0.0, 1),
        lambda: conditional_mean_arrival_time_s(0.0, 1.0, 1),
        lambda: authenticated_sequence_actionable_probabilities(1.0, [], []),
        lambda: authenticated_sequence_actionable_probabilities(1.0, [0.9], []),
        lambda: authenticated_sequence_actionable_probabilities(1.0, [1.1], [0.1]),
    ],
)
def test_invalid_detection_inputs(call) -> None:
    with pytest.raises((TypeError, ValueError)):
        call()
