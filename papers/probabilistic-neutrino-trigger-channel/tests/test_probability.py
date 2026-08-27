import math

import pytest

from neutrino_trigger.probability import (
    exact_at_least_one,
    ook_capacity_bits_per_pulse,
    on_off_keying_ber,
    poisson_approximation_error,
    poisson_at_least_one,
    poisson_limit_at_least_one,
)
from neutrino_trigger.simulation import reproduce_stancil_2012_channel


def test_exact_binomial_boundaries() -> None:
    assert exact_at_least_one(0, 0.5) == 0.0
    assert exact_at_least_one(10, 0.0) == 0.0
    assert exact_at_least_one(1, 1.0) == 1.0
    assert exact_at_least_one(10, 1.0) == 1.0


def test_poisson_approximation_converges_in_rare_event_limit() -> None:
    particles = 10_000_000
    p_eff = 1.0 / particles
    exact = exact_at_least_one(particles, p_eff)
    approximate = poisson_limit_at_least_one(particles, p_eff)
    assert approximate == pytest.approx(1.0 - math.exp(-1.0), rel=1e-15)
    assert exact == pytest.approx(approximate, abs=2e-8)


def test_exact_probability_exceeds_poisson_approximation_for_finite_p() -> None:
    assert poisson_approximation_error(2, 0.5) < 0.0
    assert exact_at_least_one(2, 0.5) == pytest.approx(0.75)
    assert poisson_limit_at_least_one(2, 0.5) == pytest.approx(1.0 - math.exp(-1.0))


def test_poisson_threshold_one_is_stable() -> None:
    assert poisson_at_least_one(0.0) == 0.0
    assert poisson_at_least_one(1.0e-16) == pytest.approx(1.0e-16)
    assert poisson_at_least_one(1_000.0) == 1.0


def test_arbitrarily_large_particle_count_saturates_without_overflow() -> None:
    particles = 10**400
    assert exact_at_least_one(particles, 0.1) == 1.0
    assert poisson_limit_at_least_one(particles, 0.1) == 1.0


def test_zero_background_ook_reproduces_stancil_formula() -> None:
    mean = 0.81
    assert on_off_keying_ber(mean) == pytest.approx(math.exp(-mean) / 2.0)
    assert ook_capacity_bits_per_pulse(mean) == pytest.approx(0.37, abs=0.01)


def test_2012_reproduction_has_paper_rate_scale() -> None:
    result = reproduce_stancil_2012_channel()
    assert result["paper_experimental_information_rate_bits_per_s"] == pytest.approx(0.1, abs=0.002)
    assert result["incident_proton_kinetic_energy_per_pulse_j"] == pytest.approx(
        432_587.69118
    )
    assert result["qualifying_events_per_incident_proton_beam_joule"] == pytest.approx(
        0.81 / 432_587.69118
    )
    five_frames = next(row for row in result["rows"] if row["combined_frames"] == 5)
    assert five_frames["theoretical_uncoded_ber"] < 0.01


@pytest.mark.parametrize(
    ("particles", "p_eff", "error"),
    [(-1, 0.1, ValueError), (1.5, 0.1, TypeError), (1, -0.1, ValueError), (1, 1.1, ValueError)],
)
def test_invalid_particle_inputs(particles, p_eff, error) -> None:
    with pytest.raises(error):
        exact_at_least_one(particles, p_eff)
