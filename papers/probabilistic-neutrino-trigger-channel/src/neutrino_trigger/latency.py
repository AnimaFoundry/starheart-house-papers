"""Dimensionally explicit end-to-end latency budgets."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, fields
from numbers import Integral, Real

from .geometry import SPEED_OF_LIGHT_M_S, propagation_time_s
from .parameters import nonnegative, nonnegative_integer, positive, positive_integer


def _validate_nonnegative_fields(instance: object, excluded: frozenset[str] = frozenset()) -> None:
    for field in fields(instance):
        if field.name not in excluded:
            nonnegative(getattr(instance, field.name), field.name)


@dataclass(frozen=True, slots=True)
class NeutrinoLatencyBudget:
    """End-to-end trigger latency, with every value expressed in SI units."""

    feed_s: float
    event_classification_s: float
    beam_command_s: float
    source_actuation_s: float
    particle_production_s: float
    path_length_m: float
    particle_speed_m_s: float = SPEED_OF_LIGHT_M_S
    first_sufficient_evidence_s: float = 0.0
    daq_s: float = 0.0
    authentication_decode_s: float = 0.0
    decision_s: float = 0.0
    local_order_route_s: float = 0.0
    clock_sync_margin_s: float = 0.0

    def __post_init__(self) -> None:
        _validate_nonnegative_fields(self, frozenset({"particle_speed_m_s"}))
        positive(self.particle_speed_m_s, "particle_speed_m_s")
        if self.particle_speed_m_s > SPEED_OF_LIGHT_M_S:
            raise ValueError("particle_speed_m_s must not exceed the speed of light")

    @property
    def propagation_s(self) -> float:
        return propagation_time_s(self.path_length_m, self.particle_speed_m_s)

    @property
    def total_s(self) -> float:
        return (
            self.feed_s
            + self.event_classification_s
            + self.beam_command_s
            + self.source_actuation_s
            + self.particle_production_s
            + self.propagation_s
            + self.first_sufficient_evidence_s
            + self.daq_s
            + self.authentication_decode_s
            + self.decision_s
            + self.local_order_route_s
            + self.clock_sync_margin_s
        )


@dataclass(frozen=True, slots=True)
class EMLatencyBudget:
    """Best technically plausible electromagnetic comparison budget."""

    feed_s: float
    encode_s: float
    route_length_m: float
    medium_speed_m_s: float
    network_s: float = 0.0
    decode_s: float = 0.0
    local_order_route_s: float = 0.0
    clock_sync_margin_s: float = 0.0

    def __post_init__(self) -> None:
        _validate_nonnegative_fields(self, frozenset({"medium_speed_m_s"}))
        positive(self.medium_speed_m_s, "medium_speed_m_s")
        if self.medium_speed_m_s > SPEED_OF_LIGHT_M_S:
            raise ValueError("medium_speed_m_s must not exceed the speed of light")

    @property
    def propagation_s(self) -> float:
        return propagation_time_s(self.route_length_m, self.medium_speed_m_s)

    @property
    def total_s(self) -> float:
        return (
            self.feed_s
            + self.encode_s
            + self.propagation_s
            + self.network_s
            + self.decode_s
            + self.local_order_route_s
            + self.clock_sync_margin_s
        )


def latency_advantage_s(em_budget: EMLatencyBudget, neutrino_budget: NeutrinoLatencyBudget) -> float:
    """Return ``tau_EM - tau_neutrino``; positive is required for an early trigger."""

    return em_budget.total_s - neutrino_budget.total_s


def particle_channel_beats_fallback(
    em_budget: EMLatencyBudget,
    neutrino_budget: NeutrinoLatencyBudget,
) -> bool:
    """Return whether the complete trigger budget arrives strictly earlier."""

    return latency_advantage_s(em_budget, neutrino_budget) > 0.0


@dataclass(frozen=True, slots=True)
class AuthenticationSequenceBudget:
    """Explicit slot, pulse, particle, cost, and decode authentication overhead.

    This offline accounting object does not prescribe a physical codebook.  A
    positive-pulse slot consumes particles while a quiet guard slot consumes time
    but no signal particles.  The separate counts prevent a guard-heavy codebook
    from hiding its latency or inventing particle emissions in quiet slots.
    """

    total_slot_count: int
    positive_pulse_count: int
    slot_duration_s: float
    emitted_particles_per_positive_pulse: int
    variable_cost_per_positive_pulse: float
    decode_latency_s: float = 0.0

    def __post_init__(self) -> None:
        total = positive_integer(self.total_slot_count, "total_slot_count")
        positives = positive_integer(self.positive_pulse_count, "positive_pulse_count")
        if positives > total:
            raise ValueError("positive_pulse_count must not exceed total_slot_count")
        positive(self.slot_duration_s, "slot_duration_s")
        nonnegative_integer(
            self.emitted_particles_per_positive_pulse,
            "emitted_particles_per_positive_pulse",
        )
        nonnegative(
            self.variable_cost_per_positive_pulse,
            "variable_cost_per_positive_pulse",
        )
        nonnegative(self.decode_latency_s, "decode_latency_s")

    @property
    def duration_s(self) -> float:
        """Full codeword observation duration, excluding decode."""

        return self.total_slot_count * self.slot_duration_s

    @property
    def decision_overhead_s(self) -> float:
        """Conservative full-codeword observation plus decode latency."""

        return self.duration_s + self.decode_latency_s

    @property
    def emitted_particles(self) -> int:
        return self.positive_pulse_count * self.emitted_particles_per_positive_pulse

    @property
    def variable_cost(self) -> float:
        return self.positive_pulse_count * self.variable_cost_per_positive_pulse


def authenticated_sequence_decision_latency_s(
    positive_slot_indices: Sequence[Integral],
    trigger_times_within_slot_s: Sequence[Real],
    slot_duration_s: Real,
    decode_latency_s: Real = 0.0,
    guard_slot_indices: Sequence[Integral] = (),
) -> float:
    """Return decision latency for positive detections and quiet guard slots.

    Positive slots complete when their required trigger arrives.  A guard slot
    cannot be certified quiet until its end, so the implemented timing equation is
    ``max(max((r-1)*slot + trigger_r), max(g*slot for g in guards)) + decode``.
    Indices are one-based and strictly increasing within each set; the sets must be
    disjoint. Trigger times are relative to slot start and lie in ``[0, slot]``.
    """

    indices = tuple(positive_slot_indices)
    trigger_times = tuple(trigger_times_within_slot_s)
    if not indices:
        raise ValueError("at least one prescribed positive slot is required")
    if len(indices) != len(trigger_times):
        raise ValueError("slot-index and trigger-time shapes must match")
    slot_duration = positive(slot_duration_s, "slot_duration_s")
    decode = nonnegative(decode_latency_s, "decode_latency_s")
    validated_indices = tuple(
        positive_integer(index, f"positive_slot_indices[{position}]")
        for position, index in enumerate(indices)
    )
    if any(
        right <= left
        for left, right in zip(validated_indices, validated_indices[1:])
    ):
        raise ValueError("positive_slot_indices must be strictly increasing")
    guards = tuple(
        positive_integer(index, f"guard_slot_indices[{position}]")
        for position, index in enumerate(guard_slot_indices)
    )
    if any(right <= left for left, right in zip(guards, guards[1:])):
        raise ValueError("guard_slot_indices must be strictly increasing")
    if set(validated_indices).intersection(guards):
        raise ValueError("positive and guard slot indices must be disjoint")
    validated_times = tuple(
        nonnegative(value, f"trigger_times_within_slot_s[{position}]")
        for position, value in enumerate(trigger_times)
    )
    if any(value > slot_duration for value in validated_times):
        raise ValueError("trigger time must not exceed slot_duration_s")
    last_required_trigger = max(
        (index - 1) * slot_duration + trigger_time
        for index, trigger_time in zip(
            validated_indices,
            validated_times,
            strict=True,
        )
    )
    last_required_guard_end = max((index * slot_duration for index in guards), default=0.0)
    return max(last_required_trigger, last_required_guard_end) + decode
