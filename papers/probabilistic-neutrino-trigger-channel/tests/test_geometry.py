import math

import pytest

from neutrino_trigger.geometry import (
    MEAN_EARTH_RADIUS_M,
    SPEED_OF_LIGHT_M_S,
    earth_arc_length_m,
    earth_chord_length_m,
    ideal_arc_chord_advantage_s,
    neutrino_time_of_flight_s,
    propagation_time_s,
    relativistic_speed_m_s,
    time_delay_from_light_s,
)
from neutrino_trigger.latency import (
    AuthenticationSequenceBudget,
    EMLatencyBudget,
    NeutrinoLatencyBudget,
    authenticated_sequence_decision_latency_s,
    latency_advantage_s,
    particle_channel_beats_fallback,
)


def test_arc_and_chord_formulas() -> None:
    assert earth_arc_length_m(0.0) == 0.0
    assert earth_chord_length_m(0.0) == 0.0
    assert earth_arc_length_m(math.pi) == pytest.approx(math.pi * MEAN_EARTH_RADIUS_M)
    assert earth_chord_length_m(math.pi) == pytest.approx(2.0 * MEAN_EARTH_RADIUS_M)
    for degrees in range(0, 181, 10):
        angle = math.radians(degrees)
        assert earth_chord_length_m(angle) <= earth_arc_length_m(angle) + 1e-9


def test_geometry_advantage_is_zero_at_zero_and_positive_elsewhere() -> None:
    assert ideal_arc_chord_advantage_s(0.0) == 0.0
    assert ideal_arc_chord_advantage_s(math.pi / 2.0) > 0.0


def test_neutrino_velocity_is_subluminal_and_delay_is_stable() -> None:
    path = 1.0e7
    assert relativistic_speed_m_s(0.0, 1.0e9) == SPEED_OF_LIGHT_M_S
    speed = relativistic_speed_m_s(1.0, 10.0)
    assert 0.0 < speed < SPEED_OF_LIGHT_M_S
    delay = time_delay_from_light_s(path, 0.1, 1.0e9)
    approximation = path / SPEED_OF_LIGHT_M_S * 0.5 * (0.1 / 1.0e9) ** 2
    assert delay == pytest.approx(approximation, rel=1e-15)
    assert neutrino_time_of_flight_s(path, 0.1, 1.0e9) >= path / SPEED_OF_LIGHT_M_S


def test_si_propagation_unit_consistency() -> None:
    # 300 km at 200,000 km/s is 1.5 ms.
    assert propagation_time_s(300_000.0, 200_000_000.0) == pytest.approx(0.0015)


def test_complete_latency_composition_and_advantage() -> None:
    neutrino = NeutrinoLatencyBudget(
        feed_s=1e-5,
        event_classification_s=2e-5,
        beam_command_s=3e-5,
        source_actuation_s=4e-5,
        particle_production_s=5e-5,
        path_length_m=300_000.0,
        first_sufficient_evidence_s=6e-5,
        daq_s=7e-5,
        authentication_decode_s=10e-5,
        decision_s=8e-5,
        local_order_route_s=9e-5,
        clock_sync_margin_s=1e-5,
    )
    em = EMLatencyBudget(
        feed_s=1e-5,
        encode_s=2e-5,
        route_length_m=400_000.0,
        medium_speed_m_s=200_000_000.0,
        network_s=2e-4,
        decode_s=3e-5,
        local_order_route_s=9e-5,
    )
    expected_neutrino = sum((1, 2, 3, 4, 5, 6, 7, 10, 8, 9, 1)) * 1e-5 + 300_000.0 / SPEED_OF_LIGHT_M_S
    assert neutrino.total_s == pytest.approx(expected_neutrino)
    assert latency_advantage_s(em, neutrino) == pytest.approx(em.total_s - neutrino.total_s)
    assert particle_channel_beats_fallback(em, neutrino) == (em.total_s > neutrino.total_s)


def test_authentication_sequence_overhead_is_explicit() -> None:
    sequence = AuthenticationSequenceBudget(
        total_slot_count=5,
        positive_pulse_count=3,
        slot_duration_s=2e-3,
        emitted_particles_per_positive_pulse=100,
        variable_cost_per_positive_pulse=5.0,
        decode_latency_s=8e-6,
    )
    assert sequence.duration_s == pytest.approx(0.010)
    assert sequence.decision_overhead_s == pytest.approx(0.010008)
    assert sequence.emitted_particles == 300
    assert sequence.variable_cost == 15.0


def test_authenticated_sequence_decision_latency() -> None:
    latency = authenticated_sequence_decision_latency_s(
        positive_slot_indices=[1, 3, 5],
        trigger_times_within_slot_s=[0.001, 0.002, 0.003],
        slot_duration_s=0.010,
        decode_latency_s=0.004,
        guard_slot_indices=[2, 6],
    )
    assert latency == pytest.approx(6 * 0.010 + 0.004)
    assert authenticated_sequence_decision_latency_s([1], [0.0], 0.01) == 0.0


def test_trailing_guard_slot_must_finish_before_action() -> None:
    assert authenticated_sequence_decision_latency_s(
        [1], [0.001], 0.01, guard_slot_indices=[2, 3]
    ) == pytest.approx(0.03)


@pytest.mark.parametrize(
    "call",
    [
        lambda: earth_arc_length_m(-0.1),
        lambda: earth_chord_length_m(math.pi + 0.1),
        lambda: propagation_time_s(-1.0, 1.0),
        lambda: propagation_time_s(1.0, 0.0),
        lambda: relativistic_speed_m_s(2.0, 1.0),
        lambda: NeutrinoLatencyBudget(-1.0, 0, 0, 0, 0, 1.0),
        lambda: EMLatencyBudget(0, 0, 1.0, SPEED_OF_LIGHT_M_S + 1.0),
        lambda: authenticated_sequence_decision_latency_s([], [], 0.01),
        lambda: authenticated_sequence_decision_latency_s([1], [], 0.01),
        lambda: authenticated_sequence_decision_latency_s([2, 2], [0.0, 0.0], 0.01),
        lambda: authenticated_sequence_decision_latency_s([1], [0.02], 0.01),
        lambda: authenticated_sequence_decision_latency_s([1], [0.0], 0.01, guard_slot_indices=[1]),
        lambda: authenticated_sequence_decision_latency_s([1], [0.0], 0.01, guard_slot_indices=[3, 2]),
        lambda: AuthenticationSequenceBudget(1, 2, 0.01, 1, 1.0),
    ],
)
def test_invalid_geometry_and_latency_inputs(call) -> None:
    with pytest.raises((TypeError, ValueError)):
        call()
