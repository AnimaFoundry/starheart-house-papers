import math

import pytest

from neutrino_trigger.economics import (
    AnnualValueInputs,
    annual_incremental_value,
    annual_incremental_value_fixed_gain,
    break_even_capex,
    break_even_detection_probability,
    expected_exponential_incremental_gain,
    expected_incremental_gain,
    exponential_opportunity_value,
    maximum_compatible_false_alarm_probability,
    net_present_value,
)


def test_exponential_value_decays_with_latency() -> None:
    assert exponential_opportunity_value(0.0, 100.0, 0.01) == 100.0
    assert exponential_opportunity_value(0.01, 100.0, 0.01) == pytest.approx(100.0 / math.e)


def test_closed_form_incremental_gain_matches_quadrature() -> None:
    rate = 2_000.0
    deadline = 0.001
    initial = 500.0
    decay = 0.004
    for threshold in (1, 2, 3):
        numeric = expected_incremental_gain(
            lambda time_s: exponential_opportunity_value(time_s, initial, decay),
            rate,
            deadline,
            threshold,
        )
        analytic = expected_exponential_incremental_gain(
            rate, deadline, initial, decay, threshold
        )
        assert analytic == pytest.approx(numeric, rel=2e-10, abs=1e-10)
        assert analytic >= 0.0


def test_fixed_latency_shift_matches_quadrature_and_reduces_gain() -> None:
    rate = 2_000.0
    deadline = 0.001
    fixed = 0.0002
    initial = 500.0
    decay = 0.004
    for threshold in (1, 2, 3):
        numeric = expected_incremental_gain(
            lambda time_s: exponential_opportunity_value(time_s, initial, decay),
            rate,
            deadline,
            threshold,
            fixed_neutrino_latency_s=fixed,
        )
        analytic = expected_exponential_incremental_gain(
            rate,
            deadline,
            initial,
            decay,
            threshold,
            fixed_neutrino_latency_s=fixed,
        )
        unshifted = expected_exponential_incremental_gain(
            rate, deadline, initial, decay, threshold
        )
        assert analytic == pytest.approx(numeric, rel=2e-10, abs=1e-10)
        assert 0.0 <= analytic < unshifted
    assert expected_exponential_incremental_gain(
        rate, deadline, initial, decay, fixed_neutrino_latency_s=deadline
    ) == 0.0


def test_annual_incremental_value_composition() -> None:
    inputs = AnnualValueInputs(
        valid_windows_per_year=100.0,
        null_windows_per_year=1_000.0,
        expected_incremental_gain_per_valid_window=20.0,
        false_alarm_probability_per_null_window=0.001,
        false_trigger_loss=500.0,
        pulse_cost_per_valid_window=2.0,
        annual_fixed_cost=100.0,
        annual_operating_cost=200.0,
    )
    expected = 100.0 * (20.0 - 2.0) - 1_000.0 * 0.001 * 500.0 - 100.0 - 200.0
    assert annual_incremental_value(inputs) == pytest.approx(expected)


def test_value_monotonicity_in_pd_pfa_and_pulse_cost() -> None:
    common = dict(
        valid_windows_per_year=100.0,
        null_windows_per_year=10_000.0,
        early_success_incremental_gain=50.0,
        false_trigger_loss=100.0,
        annual_fixed_cost=0.0,
        annual_operating_cost=0.0,
    )
    base = annual_incremental_value_fixed_gain(
        **common,
        detection_probability_before_deadline=0.5,
        false_alarm_probability_per_null_window=1e-4,
        pulse_cost_per_valid_window=1.0,
    )
    higher_pd = annual_incremental_value_fixed_gain(
        **common,
        detection_probability_before_deadline=0.6,
        false_alarm_probability_per_null_window=1e-4,
        pulse_cost_per_valid_window=1.0,
    )
    higher_pfa = annual_incremental_value_fixed_gain(
        **common,
        detection_probability_before_deadline=0.5,
        false_alarm_probability_per_null_window=2e-4,
        pulse_cost_per_valid_window=1.0,
    )
    higher_pulse = annual_incremental_value_fixed_gain(
        **common,
        detection_probability_before_deadline=0.5,
        false_alarm_probability_per_null_window=1e-4,
        pulse_cost_per_valid_window=2.0,
    )
    assert higher_pd > base
    assert higher_pfa < base
    assert higher_pulse < base


def test_npv_and_break_even_capex() -> None:
    assert net_present_value(100.0, 250.0, 3, 0.0) == pytest.approx(50.0)
    capex = break_even_capex(100.0, 3, 0.0)
    assert capex == pytest.approx(300.0)
    assert capex is not None
    assert net_present_value(100.0, capex, 3, 0.0) == pytest.approx(0.0)
    discounted = break_even_capex(100.0, 3, 0.10)
    assert discounted is not None
    assert 0.0 < discounted < 300.0


def test_break_even_capex_reports_infeasible_zero_price_case() -> None:
    assert break_even_capex(-1.0, 5, 0.1) is None
    assert break_even_capex(0.0, 5, 0.1) == 0.0


def test_break_even_probability_and_false_alarm_inverse() -> None:
    required_pd = break_even_detection_probability(
        valid_windows_per_year=1_000.0,
        null_windows_per_year=10_000.0,
        false_alarm_probability_per_null_window=1e-4,
        early_success_incremental_gain=100.0,
        false_trigger_loss=500.0,
        pulse_cost_per_valid_window=5.0,
        annual_fixed_cost=1_000.0,
        annual_operating_cost=1_000.0,
    )
    value = annual_incremental_value_fixed_gain(
        1_000.0,
        10_000.0,
        required_pd,
        1e-4,
        100.0,
        500.0,
        5.0,
        1_000.0,
        1_000.0,
    )
    assert value == pytest.approx(0.0, abs=1e-10)
    max_pfa = maximum_compatible_false_alarm_probability(
        1_000.0,
        10_000.0,
        required_pd,
        100.0,
        500.0,
        5.0,
        1_000.0,
        1_000.0,
    )
    assert max_pfa == pytest.approx(1e-4)


def test_false_alarm_bound_reports_infeasible_zero_pfa_case() -> None:
    assert (
        maximum_compatible_false_alarm_probability(
            valid_windows_per_year=100.0,
            null_windows_per_year=1_000.0,
            detection_probability_before_deadline=0.1,
            early_success_incremental_gain=1.0,
            false_trigger_loss=100.0,
            pulse_cost_per_valid_window=2.0,
            annual_fixed_cost=1.0,
        )
        is None
    )
    assert maximum_compatible_false_alarm_probability(100, 1_000, 0.5, 2, 10, 1) == 0.0


@pytest.mark.parametrize(
    "call",
    [
        lambda: exponential_opportunity_value(-1.0, 1.0, 1.0),
        lambda: expected_exponential_incremental_gain(1.0, 1.0, 1.0, 0.0),
        lambda: expected_incremental_gain(lambda _: 1.0, 1.0, 1.0, fixed_neutrino_latency_s=-1.0),
        lambda: expected_exponential_incremental_gain(1.0, 1.0, 1.0, 1.0, fixed_neutrino_latency_s=-1.0),
        lambda: AnnualValueInputs(1, 1, 1, 1.1, 1, 1, 1, 1),
        lambda: net_present_value(1.0, -1.0, 1, 0.1),
        lambda: net_present_value(1.0, 1.0, 0, 0.1),
        lambda: break_even_detection_probability(0, 1, 0, 1, 1, 1),
        lambda: maximum_compatible_false_alarm_probability(1, 0, 0.5, 1, 1, 1),
    ],
)
def test_invalid_economic_inputs(call) -> None:
    with pytest.raises((TypeError, ValueError)):
        call()
