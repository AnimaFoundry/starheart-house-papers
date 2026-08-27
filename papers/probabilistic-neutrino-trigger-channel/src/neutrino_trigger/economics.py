"""Incremental utility, annual value, NPV, and break-even calculations."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import math
from numbers import Integral, Real

from scipy.integrate import quad
from scipy.special import gammainc

from .first_arrival import arrival_cdf, arrival_pdf
from .parameters import (
    finite_float,
    nonnegative,
    positive,
    positive_integer,
    probability,
)


def exponential_opportunity_value(latency_s: Real, initial_value: Real, decay_time_s: Real) -> float:
    """Illustrative exponential gross opportunity-value curve."""

    latency = nonnegative(latency_s, "latency_s")
    initial = nonnegative(initial_value, "initial_value")
    decay = positive(decay_time_s, "decay_time_s")
    return initial * math.exp(-latency / decay)


def expected_incremental_gain(
    value_function: Callable[[float], float],
    detection_rate_hz: Real,
    em_deadline_s: Real,
    threshold: Integral = 1,
    fixed_neutrino_latency_s: Real = 0.0,
) -> float:
    """Integrate fallback-relative gain over a shifted evidence-time density.

    ``fixed_neutrino_latency_s`` contains every non-accumulation term between the
    originating request and action.  If evidence time is ``u``, full action time
    is ``fixed + u`` and only ``u < em_deadline - fixed`` can add value.
    """

    rate = nonnegative(detection_rate_hz, "detection_rate_hz")
    deadline = nonnegative(em_deadline_s, "em_deadline_s")
    m = positive_integer(threshold, "threshold")
    fixed = nonnegative(fixed_neutrino_latency_s, "fixed_neutrino_latency_s")
    evidence_budget = deadline - fixed
    if rate == 0.0 or deadline == 0.0 or evidence_budget <= 0.0:
        return 0.0
    baseline_value = finite_float(value_function(deadline), "value_function(deadline)")

    def integrand(evidence_time_s: float) -> float:
        action_time_s = fixed + evidence_time_s
        value = finite_float(value_function(action_time_s), "value_function(time)")
        return (value - baseline_value) * arrival_pdf(rate, evidence_time_s, m)

    result, _ = quad(
        integrand,
        0.0,
        evidence_budget,
        epsabs=1e-11,
        epsrel=1e-10,
        limit=200,
    )
    return float(result)


def expected_exponential_incremental_gain(
    detection_rate_hz: Real,
    em_deadline_s: Real,
    initial_value: Real,
    decay_time_s: Real,
    threshold: Integral = 1,
    fixed_neutrino_latency_s: Real = 0.0,
) -> float:
    """Closed-form shifted m-th-arrival utility for an exponential alpha curve."""

    rate = nonnegative(detection_rate_hz, "detection_rate_hz")
    deadline = nonnegative(em_deadline_s, "em_deadline_s")
    initial = nonnegative(initial_value, "initial_value")
    decay = positive(decay_time_s, "decay_time_s")
    m = positive_integer(threshold, "threshold")
    fixed = nonnegative(fixed_neutrino_latency_s, "fixed_neutrino_latency_s")
    evidence_budget = deadline - fixed
    if (
        rate == 0.0
        or deadline == 0.0
        or initial == 0.0
        or evidence_budget <= 0.0
    ):
        return 0.0
    adjusted_rate = rate + 1.0 / decay
    discounted_arrival_term = math.exp(-fixed / decay) * (
        rate / adjusted_rate
    ) ** m * gammainc(
        m, adjusted_rate * evidence_budget
    )
    detection_by_deadline = arrival_cdf(rate, evidence_budget, m)
    baseline_term = math.exp(-deadline / decay) * detection_by_deadline
    return float(initial * (discounted_arrival_term - baseline_term))


@dataclass(frozen=True, slots=True)
class AnnualValueInputs:
    """Validated annualized incremental-value inputs.

    Monetary fields may use any single consistent currency.  No currency or
    opportunity-rate default is asserted to be empirical.
    """

    valid_windows_per_year: float
    null_windows_per_year: float
    expected_incremental_gain_per_valid_window: float
    false_alarm_probability_per_null_window: float
    false_trigger_loss: float
    pulse_cost_per_valid_window: float
    annual_fixed_cost: float
    annual_operating_cost: float

    def __post_init__(self) -> None:
        nonnegative(self.valid_windows_per_year, "valid_windows_per_year")
        nonnegative(self.null_windows_per_year, "null_windows_per_year")
        finite_float(
            self.expected_incremental_gain_per_valid_window,
            "expected_incremental_gain_per_valid_window",
        )
        probability(
            self.false_alarm_probability_per_null_window,
            "false_alarm_probability_per_null_window",
        )
        nonnegative(self.false_trigger_loss, "false_trigger_loss")
        nonnegative(self.pulse_cost_per_valid_window, "pulse_cost_per_valid_window")
        nonnegative(self.annual_fixed_cost, "annual_fixed_cost")
        nonnegative(self.annual_operating_cost, "annual_operating_cost")


def annual_incremental_value(inputs: AnnualValueInputs) -> float:
    """Annual incremental value versus the conventional fallback baseline."""

    valid_contribution = inputs.valid_windows_per_year * (
        inputs.expected_incremental_gain_per_valid_window
        - inputs.pulse_cost_per_valid_window
    )
    false_trigger_cost = (
        inputs.null_windows_per_year
        * inputs.false_alarm_probability_per_null_window
        * inputs.false_trigger_loss
    )
    return (
        valid_contribution
        - false_trigger_cost
        - inputs.annual_fixed_cost
        - inputs.annual_operating_cost
    )


def annual_incremental_value_fixed_gain(
    valid_windows_per_year: Real,
    null_windows_per_year: Real,
    detection_probability_before_deadline: Real,
    false_alarm_probability_per_null_window: Real,
    early_success_incremental_gain: Real,
    false_trigger_loss: Real,
    pulse_cost_per_valid_window: Real,
    annual_fixed_cost: Real = 0.0,
    annual_operating_cost: Real = 0.0,
) -> float:
    """Discrete-gain form useful for break-even and sensitivity grids."""

    pd = probability(detection_probability_before_deadline, "detection_probability")
    gain = nonnegative(early_success_incremental_gain, "early_success_incremental_gain")
    return annual_incremental_value(
        AnnualValueInputs(
            nonnegative(valid_windows_per_year, "valid_windows_per_year"),
            nonnegative(null_windows_per_year, "null_windows_per_year"),
            pd * gain,
            probability(false_alarm_probability_per_null_window, "false_alarm_probability"),
            nonnegative(false_trigger_loss, "false_trigger_loss"),
            nonnegative(pulse_cost_per_valid_window, "pulse_cost_per_valid_window"),
            nonnegative(annual_fixed_cost, "annual_fixed_cost"),
            nonnegative(annual_operating_cost, "annual_operating_cost"),
        )
    )


def net_present_value(
    annual_cash_flow: Real,
    upfront_capex: Real,
    years: Integral,
    annual_discount_rate: Real,
    terminal_value: Real = 0.0,
) -> float:
    """Finite-horizon NPV with end-of-year level cash flows."""

    cash_flow = finite_float(annual_cash_flow, "annual_cash_flow")
    capex = nonnegative(upfront_capex, "upfront_capex")
    horizon = positive_integer(years, "years")
    discount = nonnegative(annual_discount_rate, "annual_discount_rate")
    terminal = finite_float(terminal_value, "terminal_value")
    annuity_factor = sum((1.0 + discount) ** (-year) for year in range(1, horizon + 1))
    return -capex + cash_flow * annuity_factor + terminal * (1.0 + discount) ** (-horizon)


def break_even_capex(
    annual_cash_flow_before_capex: Real,
    years: Integral,
    annual_discount_rate: Real,
    terminal_value: Real = 0.0,
) -> float | None:
    """Maximum upfront CAPEX consistent with nonnegative NPV.

    Returns ``None`` when the discounted operating surplus is negative even at
    zero CAPEX.  Returning zero is reserved for a genuinely feasible boundary
    where zero CAPEX produces exactly zero NPV.
    """

    cash_flow = finite_float(annual_cash_flow_before_capex, "annual_cash_flow_before_capex")
    horizon = positive_integer(years, "years")
    discount = nonnegative(annual_discount_rate, "annual_discount_rate")
    terminal = finite_float(terminal_value, "terminal_value")
    present_value = sum(cash_flow / (1.0 + discount) ** year for year in range(1, horizon + 1))
    present_value += terminal / (1.0 + discount) ** horizon
    return None if present_value < 0.0 else present_value


def break_even_detection_probability(
    valid_windows_per_year: Real,
    null_windows_per_year: Real,
    false_alarm_probability_per_null_window: Real,
    early_success_incremental_gain: Real,
    false_trigger_loss: Real,
    pulse_cost_per_valid_window: Real,
    annual_fixed_cost: Real = 0.0,
    annual_operating_cost: Real = 0.0,
) -> float:
    """Detection probability required for zero annual incremental value.

    A return above one means no feasible probability can break even under the
    supplied assumptions.
    """

    rho1 = positive(valid_windows_per_year, "valid_windows_per_year")
    rho0 = nonnegative(null_windows_per_year, "null_windows_per_year")
    pfa = probability(false_alarm_probability_per_null_window, "false_alarm_probability")
    gain = positive(early_success_incremental_gain, "early_success_incremental_gain")
    loss = nonnegative(false_trigger_loss, "false_trigger_loss")
    pulse = nonnegative(pulse_cost_per_valid_window, "pulse_cost_per_valid_window")
    fixed = nonnegative(annual_fixed_cost, "annual_fixed_cost")
    operate = nonnegative(annual_operating_cost, "annual_operating_cost")
    required = (rho1 * pulse + rho0 * pfa * loss + fixed + operate) / (rho1 * gain)
    return required


def maximum_compatible_false_alarm_probability(
    valid_windows_per_year: Real,
    null_windows_per_year: Real,
    detection_probability_before_deadline: Real,
    early_success_incremental_gain: Real,
    false_trigger_loss: Real,
    pulse_cost_per_valid_window: Real,
    annual_fixed_cost: Real = 0.0,
    annual_operating_cost: Real = 0.0,
) -> float | None:
    """Largest P_FA compatible with nonnegative annual incremental value.

    Returns ``None`` when the proposal loses money even with ``P_FA = 0``.
    A numeric zero therefore means that zero false alarms is exactly the
    break-even boundary, not that an infeasible case was silently clamped.
    """

    rho1 = nonnegative(valid_windows_per_year, "valid_windows_per_year")
    rho0 = positive(null_windows_per_year, "null_windows_per_year")
    pd = probability(detection_probability_before_deadline, "detection_probability")
    gain = nonnegative(early_success_incremental_gain, "early_success_incremental_gain")
    loss = positive(false_trigger_loss, "false_trigger_loss")
    pulse = nonnegative(pulse_cost_per_valid_window, "pulse_cost_per_valid_window")
    fixed = nonnegative(annual_fixed_cost, "annual_fixed_cost")
    operate = nonnegative(annual_operating_cost, "annual_operating_cost")
    numerator = rho1 * (pd * gain - pulse) - fixed - operate
    if numerator < 0.0:
        return None
    return min(1.0, numerator / (rho0 * loss))


def maximum_false_alarm_probability(
    valid_windows_per_year: Real,
    null_windows_per_year: Real,
    detection_probability_before_deadline: Real,
    early_success_incremental_gain: Real,
    false_trigger_loss: Real,
    pulse_cost_per_valid_window: Real,
    annual_fixed_cost: Real = 0.0,
    annual_operating_cost: Real = 0.0,
) -> float | None:
    """Backward-compatible alias for :func:`maximum_compatible_false_alarm_probability`."""

    return maximum_compatible_false_alarm_probability(
        valid_windows_per_year,
        null_windows_per_year,
        detection_probability_before_deadline,
        early_success_incremental_gain,
        false_trigger_loss,
        pulse_cost_per_valid_window,
        annual_fixed_cost,
        annual_operating_cost,
    )
