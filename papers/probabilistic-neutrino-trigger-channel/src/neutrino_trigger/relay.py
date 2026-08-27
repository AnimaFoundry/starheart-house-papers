"""Direct and regenerative-relay reliability, latency, and cost models."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from enum import StrEnum
import math
from numbers import Integral, Real

from .detection import detection_probability
from .parameters import nonnegative, positive, positive_integer, probability


class DistanceModel(StrEnum):
    """Explicit signal-mean scaling choices for relay studies."""

    IDEAL_NO_DISTANCE_PENALTY = "ideal_no_distance_penalty"
    SYNTHETIC_GEOMETRIC = "synthetic_geometric"
    SUPPLIED_HOP_MEANS = "supplied_hop_means"


def end_to_end_detection_probability(per_hop_probabilities: Sequence[Real]) -> float:
    """Product reliability under the stated independent-hop approximation."""

    if not per_hop_probabilities:
        raise ValueError("at least one hop probability is required")
    result = 1.0
    for index, value in enumerate(per_hop_probabilities):
        result *= probability(value, f"per_hop_probabilities[{index}]")
    return result


def regenerative_false_origin_upper_bound(
    per_hop_false_origin_probabilities: Sequence[Real],
    per_hop_signal_detection_probabilities: Sequence[Real],
) -> float:
    """Union bound for actionable false origins in a regenerative chain.

    A false origin at hop ``i`` becomes actionable only if every downstream hop
    detects and regenerates it, giving ``sum_i PFA_i prod_{j>i} PD_j``.  This is
    not ``prod_i PFA_i``: once a false origin is regenerated, downstream sites
    receive a signal-like pulse.  The returned union bound is capped at one.
    """

    if not per_hop_false_origin_probabilities:
        raise ValueError("at least one hop probability is required")
    if len(per_hop_false_origin_probabilities) != len(
        per_hop_signal_detection_probabilities
    ):
        raise ValueError("false-origin and signal-detection sequences must have equal length")
    false_origins = tuple(
        probability(value, f"per_hop_false_origin_probabilities[{index}]")
        for index, value in enumerate(per_hop_false_origin_probabilities)
    )
    detections = tuple(
        probability(value, f"per_hop_signal_detection_probabilities[{index}]")
        for index, value in enumerate(per_hop_signal_detection_probabilities)
    )
    bound = sum(
        false_probability * math.prod(detections[index + 1 :])
        for index, false_probability in enumerate(false_origins)
    )
    return min(1.0, bound)


def relay_latency_s(
    hop_lengths_m: Sequence[Real],
    propagation_speed_m_s: Real,
    relay_regeneration_delays_s: Sequence[Real],
    endpoint_delay_s: Real = 0.0,
) -> float:
    """Propagation plus complete detect/reconstruct/regenerate relay delays."""

    if not hop_lengths_m:
        raise ValueError("at least one hop length is required")
    lengths = [nonnegative(v, f"hop_lengths_m[{i}]") for i, v in enumerate(hop_lengths_m)]
    speed = positive(propagation_speed_m_s, "propagation_speed_m_s")
    expected_relays = len(lengths) - 1
    if len(relay_regeneration_delays_s) != expected_relays:
        raise ValueError("relay delay count must equal hop count minus one")
    delays = [
        nonnegative(v, f"relay_regeneration_delays_s[{i}]")
        for i, v in enumerate(relay_regeneration_delays_s)
    ]
    endpoint = nonnegative(endpoint_delay_s, "endpoint_delay_s")
    return sum(lengths) / speed + sum(delays) + endpoint


def relay_cost(
    pulse_costs: Sequence[Real],
    relay_infrastructure_costs: Sequence[Real],
) -> float:
    """Sum pulse and relay-infrastructure costs in one consistent cost basis."""

    if not pulse_costs:
        raise ValueError("at least one pulse cost is required")
    if len(relay_infrastructure_costs) != len(pulse_costs) - 1:
        raise ValueError("infrastructure cost count must equal hop count minus one")
    pulses = [nonnegative(v, f"pulse_costs[{i}]") for i, v in enumerate(pulse_costs)]
    infrastructure = [
        nonnegative(v, f"relay_infrastructure_costs[{i}]")
        for i, v in enumerate(relay_infrastructure_costs)
    ]
    return sum(pulses) + sum(infrastructure)


def equal_hop_signal_means(
    direct_signal_mean: Real,
    hop_count: Integral,
    distance_model: DistanceModel,
    geometric_exponent: Real = 2.0,
    supplied_hop_means: Sequence[Real] | None = None,
) -> tuple[float, ...]:
    """Construct per-hop signal means for a declared distance model.

    ``SYNTHETIC_GEOMETRIC`` uses ``lambda_hop = lambda_direct * h**exponent``
    for equal hop lengths.  This is an illustrative flux-density scaling, not a
    universal law for an engineered neutrino beam.
    """

    direct = nonnegative(direct_signal_mean, "direct_signal_mean")
    hops = positive_integer(hop_count, "hop_count")
    try:
        model = DistanceModel(distance_model)
    except ValueError as error:
        raise ValueError(f"unsupported distance model: {distance_model}") from error
    if model is DistanceModel.IDEAL_NO_DISTANCE_PENALTY:
        return (direct,) * hops
    if model is DistanceModel.SYNTHETIC_GEOMETRIC:
        exponent = nonnegative(geometric_exponent, "geometric_exponent")
        return (direct * hops**exponent,) * hops
    if supplied_hop_means is None or len(supplied_hop_means) != hops:
        raise ValueError("supplied_hop_means must contain exactly one mean per hop")
    return tuple(
        nonnegative(value, f"supplied_hop_means[{index}]")
        for index, value in enumerate(supplied_hop_means)
    )


@dataclass(frozen=True, slots=True)
class RelayEvaluation:
    """Computed reliability, latency, cost, and per-hop audit values."""

    hop_count: int
    per_hop_signal_means: tuple[float, ...]
    per_hop_detection_probabilities: tuple[float, ...]
    end_to_end_detection_probability: float
    latency_s: float
    cost: float
    distance_model: DistanceModel


@dataclass(frozen=True, slots=True)
class AnnualRelayValueInputs:
    """Currency-consistent annual inputs for fallback-relative relay value.

    Every gain, loss, and cost must use the same currency.  The false-alarm
    probability is supplied end to end; it is not inferred from hop detection
    probabilities because null propagation depends on the authentication and
    regeneration protocol.
    """

    valid_windows_per_year: float
    null_windows_per_year: float
    end_to_end_false_alarm_probability: float
    fallback_relative_gain_per_success: float
    false_trigger_loss: float
    pulse_variable_cost_per_valid_window: float
    annual_fixed_cost: float
    annual_operating_cost: float

    def __post_init__(self) -> None:
        nonnegative(self.valid_windows_per_year, "valid_windows_per_year")
        nonnegative(self.null_windows_per_year, "null_windows_per_year")
        probability(
            self.end_to_end_false_alarm_probability,
            "end_to_end_false_alarm_probability",
        )
        nonnegative(
            self.fallback_relative_gain_per_success,
            "fallback_relative_gain_per_success",
        )
        nonnegative(self.false_trigger_loss, "false_trigger_loss")
        nonnegative(
            self.pulse_variable_cost_per_valid_window,
            "pulse_variable_cost_per_valid_window",
        )
        nonnegative(self.annual_fixed_cost, "annual_fixed_cost")
        nonnegative(self.annual_operating_cost, "annual_operating_cost")


def annual_relay_incremental_value(
    evaluation: RelayEvaluation,
    inputs: AnnualRelayValueInputs,
) -> float:
    """Annual relay value incremental to the electromagnetic fallback.

    ``fallback_relative_gain_per_success`` must already equal the gain from the
    evaluated arrival time relative to acting at the EM fallback, not gross
    strategy value.  Pulse cost is charged for every valid signaling window,
    including missed triggers.  Relay pulses caused by null-window false origins
    are not separately charged; include them in ``false_trigger_loss`` when they
    are material.  This convention must be stated in any reported scenario.
    """

    valid_value = inputs.valid_windows_per_year * (
        evaluation.end_to_end_detection_probability
        * inputs.fallback_relative_gain_per_success
        - inputs.pulse_variable_cost_per_valid_window
    )
    null_loss = (
        inputs.null_windows_per_year
        * inputs.end_to_end_false_alarm_probability
        * inputs.false_trigger_loss
    )
    return (
        valid_value
        - null_loss
        - inputs.annual_fixed_cost
        - inputs.annual_operating_cost
    )


def evaluate_equal_hop_architecture(
    total_distance_m: Real,
    hop_count: Integral,
    direct_signal_mean: Real,
    background_mean_per_hop: Real,
    threshold: Integral,
    propagation_speed_m_s: Real,
    relay_regeneration_delay_s: Real,
    endpoint_delay_s: Real,
    pulse_cost_per_hop: Real,
    relay_infrastructure_cost: Real,
    distance_model: DistanceModel = DistanceModel.SYNTHETIC_GEOMETRIC,
    geometric_exponent: Real = 2.0,
    supplied_hop_means: Sequence[Real] | None = None,
) -> RelayEvaluation:
    """Evaluate a direct (h=1) or equal-hop regenerative architecture."""

    distance = nonnegative(total_distance_m, "total_distance_m")
    hops = positive_integer(hop_count, "hop_count")
    background = nonnegative(background_mean_per_hop, "background_mean_per_hop")
    threshold_value = positive_integer(threshold, "threshold")
    speed = positive(propagation_speed_m_s, "propagation_speed_m_s")
    relay_delay = nonnegative(relay_regeneration_delay_s, "relay_regeneration_delay_s")
    endpoint = nonnegative(endpoint_delay_s, "endpoint_delay_s")
    pulse_cost = nonnegative(pulse_cost_per_hop, "pulse_cost_per_hop")
    infrastructure_cost = nonnegative(relay_infrastructure_cost, "relay_infrastructure_cost")
    means = equal_hop_signal_means(
        direct_signal_mean,
        hops,
        distance_model,
        geometric_exponent,
        supplied_hop_means,
    )
    probabilities = tuple(
        detection_probability(mean, background, threshold_value) for mean in means
    )
    success = end_to_end_detection_probability(probabilities)
    lengths = (distance / hops,) * hops
    delays = (relay_delay,) * (hops - 1)
    latency = relay_latency_s(lengths, speed, delays, endpoint)
    cost = relay_cost((pulse_cost,) * hops, (infrastructure_cost,) * (hops - 1))
    return RelayEvaluation(
        hops,
        means,
        probabilities,
        success,
        latency,
        cost,
        DistanceModel(distance_model),
    )


def latency_decayed_architecture_utility(
    evaluation: RelayEvaluation,
    gross_value_if_immediate: Real,
    value_decay_time_s: Real,
) -> float:
    """Normalized per-opportunity score for non-economic sensitivity checks.

    Use :func:`annual_relay_incremental_value` for currency-denominated claims;
    this compact score is retained only for backward-compatible normalized tests.
    """

    gross = nonnegative(gross_value_if_immediate, "gross_value_if_immediate")
    decay = positive(value_decay_time_s, "value_decay_time_s")
    discounted_gross = gross * math.exp(-evaluation.latency_s / decay)
    return evaluation.end_to_end_detection_probability * discounted_gross - evaluation.cost


def select_best_architecture(
    evaluations: Sequence[RelayEvaluation],
    objective: Callable[[RelayEvaluation], Real],
) -> RelayEvaluation:
    """Return the evaluation with maximum finite objective, preferring fewer hops."""

    if not evaluations:
        raise ValueError("at least one architecture evaluation is required")
    scored: list[tuple[float, int, RelayEvaluation]] = []
    for evaluation in evaluations:
        score = float(objective(evaluation))
        if not math.isfinite(score):
            raise ValueError("architecture objective must be finite")
        scored.append((score, -evaluation.hop_count, evaluation))
    return max(scored, key=lambda item: (item[0], item[1]))[2]
