"""Offline feasibility models for a probabilistic particle trigger channel.

CONCEPT · RESEARCH_ONLY · L0 · SIMULATION_ONLY where applicable.
This package neither controls particle sources nor connects to live markets.
"""

from .detection import detection_probability, false_alarm_probability
from .first_arrival import arrival_cdf, required_signal_rate_hz
from .probability import exact_at_least_one, poisson_limit_at_least_one

__all__ = [
    "arrival_cdf",
    "detection_probability",
    "exact_at_least_one",
    "false_alarm_probability",
    "poisson_limit_at_least_one",
    "required_signal_rate_hz",
]

__version__ = "0.1.0"
