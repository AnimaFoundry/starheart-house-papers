import math

import pytest

from neutrino_trigger.geometry import SPEED_OF_LIGHT_M_S
from neutrino_trigger.relay import (
    AnnualRelayValueInputs,
    DistanceModel,
    annual_relay_incremental_value,
    end_to_end_detection_probability,
    equal_hop_signal_means,
    evaluate_equal_hop_architecture,
    latency_decayed_architecture_utility,
    relay_cost,
    relay_latency_s,
    regenerative_false_origin_upper_bound,
    select_best_architecture,
)


def test_independent_hop_success_probability() -> None:
    assert end_to_end_detection_probability([0.9, 0.8, 0.7]) == pytest.approx(0.504)
    assert end_to_end_detection_probability([1.0]) == 1.0


def test_relay_latency_includes_complete_regeneration_delays() -> None:
    latency = relay_latency_s(
        [100_000.0, 200_000.0, 300_000.0],
        200_000_000.0,
        [0.002, 0.003],
        endpoint_delay_s=0.001,
    )
    assert latency == pytest.approx(600_000.0 / 200_000_000.0 + 0.006)


def test_relay_cost_separates_pulses_and_infrastructure() -> None:
    assert relay_cost([1.0, 1.0, 1.0], [10.0, 20.0]) == 33.0


def test_regenerative_false_origin_bound_is_not_pfa_product() -> None:
    bound = regenerative_false_origin_upper_bound(
        [0.01, 0.02, 0.03],
        [0.8, 0.7, 0.6],
    )
    assert bound == pytest.approx(0.01 * 0.7 * 0.6 + 0.02 * 0.6 + 0.03)
    first_hop_only = regenerative_false_origin_upper_bound(
        [0.01, 0.0, 0.0],
        [0.8, 0.7, 0.6],
    )
    assert first_hop_only == pytest.approx(0.01 * 0.7 * 0.6)


def test_declared_distance_models() -> None:
    assert equal_hop_signal_means(
        0.1, 3, DistanceModel.IDEAL_NO_DISTANCE_PENALTY
    ) == (0.1, 0.1, 0.1)
    assert equal_hop_signal_means(
        0.1, 3, DistanceModel.SYNTHETIC_GEOMETRIC
    ) == pytest.approx((0.9, 0.9, 0.9))
    assert equal_hop_signal_means(
        0.1,
        3,
        DistanceModel.SUPPLIED_HOP_MEANS,
        supplied_hop_means=(0.2, 0.3, 0.4),
    ) == (0.2, 0.3, 0.4)


def test_architecture_evaluation_boundary_and_monotonicity() -> None:
    direct = evaluate_equal_hop_architecture(
        total_distance_m=1_000_000.0,
        hop_count=1,
        direct_signal_mean=0.5,
        background_mean_per_hop=0.0,
        threshold=1,
        propagation_speed_m_s=SPEED_OF_LIGHT_M_S,
        relay_regeneration_delay_s=0.001,
        endpoint_delay_s=0.0001,
        pulse_cost_per_hop=2.0,
        relay_infrastructure_cost=100.0,
        distance_model=DistanceModel.SYNTHETIC_GEOMETRIC,
    )
    assert direct.per_hop_signal_means == (0.5,)
    assert direct.end_to_end_detection_probability == pytest.approx(1.0 - math.exp(-0.5))
    assert direct.latency_s == pytest.approx(1_000_000.0 / SPEED_OF_LIGHT_M_S + 0.0001)
    assert direct.cost == 2.0

    stronger = evaluate_equal_hop_architecture(
        total_distance_m=1_000_000.0,
        hop_count=1,
        direct_signal_mean=1.0,
        background_mean_per_hop=0.0,
        threshold=1,
        propagation_speed_m_s=SPEED_OF_LIGHT_M_S,
        relay_regeneration_delay_s=0.001,
        endpoint_delay_s=0.0001,
        pulse_cost_per_hop=2.0,
        relay_infrastructure_cost=100.0,
        distance_model=DistanceModel.SYNTHETIC_GEOMETRIC,
    )
    assert stronger.end_to_end_detection_probability > direct.end_to_end_detection_probability


def test_architecture_selection_uses_objective_and_prefers_fewer_hops_on_tie() -> None:
    evaluations = [
        evaluate_equal_hop_architecture(
            100_000.0,
            hops,
            0.2,
            0.0,
            1,
            SPEED_OF_LIGHT_M_S,
            1e-4,
            0.0,
            0.0,
            0.0,
            DistanceModel.SYNTHETIC_GEOMETRIC,
        )
        for hops in (1, 2, 3)
    ]
    selected = select_best_architecture(evaluations, lambda evaluation: 1.0)
    assert selected.hop_count == 1
    utility_selected = select_best_architecture(
        evaluations,
        lambda evaluation: latency_decayed_architecture_utility(evaluation, 1.0, 0.01),
    )
    assert utility_selected in evaluations


def test_currency_consistent_annual_relay_value() -> None:
    evaluation = evaluate_equal_hop_architecture(
        total_distance_m=100_000.0,
        hop_count=2,
        direct_signal_mean=0.5,
        background_mean_per_hop=0.0,
        threshold=1,
        propagation_speed_m_s=SPEED_OF_LIGHT_M_S,
        relay_regeneration_delay_s=1e-4,
        endpoint_delay_s=0.0,
        pulse_cost_per_hop=0.0,
        relay_infrastructure_cost=0.0,
        distance_model=DistanceModel.SYNTHETIC_GEOMETRIC,
    )
    inputs = AnnualRelayValueInputs(
        valid_windows_per_year=100.0,
        null_windows_per_year=1_000.0,
        end_to_end_false_alarm_probability=1e-4,
        fallback_relative_gain_per_success=50.0,
        false_trigger_loss=500.0,
        pulse_variable_cost_per_valid_window=2.0,
        annual_fixed_cost=100.0,
        annual_operating_cost=50.0,
    )
    expected = (
        100.0 * (evaluation.end_to_end_detection_probability * 50.0 - 2.0)
        - 1_000.0 * 1e-4 * 500.0
        - 100.0
        - 50.0
    )
    assert annual_relay_incremental_value(evaluation, inputs) == pytest.approx(expected)


def test_annual_relay_value_uses_supplied_end_to_end_pfa() -> None:
    evaluation = evaluate_equal_hop_architecture(
        100_000.0,
        1,
        1.0,
        0.0,
        1,
        SPEED_OF_LIGHT_M_S,
        0.0,
        0.0,
        0.0,
        0.0,
        DistanceModel.IDEAL_NO_DISTANCE_PENALTY,
    )
    common = dict(
        valid_windows_per_year=100.0,
        null_windows_per_year=1_000.0,
        fallback_relative_gain_per_success=50.0,
        false_trigger_loss=500.0,
        pulse_variable_cost_per_valid_window=2.0,
        annual_fixed_cost=100.0,
        annual_operating_cost=50.0,
    )
    low = annual_relay_incremental_value(
        evaluation,
        AnnualRelayValueInputs(**common, end_to_end_false_alarm_probability=1e-5),
    )
    high = annual_relay_incremental_value(
        evaluation,
        AnnualRelayValueInputs(**common, end_to_end_false_alarm_probability=1e-3),
    )
    assert high < low


@pytest.mark.parametrize(
    "call",
    [
        lambda: end_to_end_detection_probability([]),
        lambda: end_to_end_detection_probability([1.1]),
        lambda: relay_latency_s([], 1.0, []),
        lambda: relay_latency_s([1.0, 1.0], 1.0, []),
        lambda: relay_cost([1.0, 1.0], []),
        lambda: equal_hop_signal_means(1.0, 0, DistanceModel.SYNTHETIC_GEOMETRIC),
        lambda: equal_hop_signal_means(1.0, 2, DistanceModel.SUPPLIED_HOP_MEANS, supplied_hop_means=[1.0]),
        lambda: select_best_architecture([], lambda evaluation: 0.0),
        lambda: AnnualRelayValueInputs(1, 1, 1.1, 1, 1, 1, 1, 1),
        lambda: regenerative_false_origin_upper_bound([0.1], [0.9, 0.8]),
    ],
)
def test_invalid_relay_inputs(call) -> None:
    with pytest.raises((TypeError, ValueError)):
        call()
