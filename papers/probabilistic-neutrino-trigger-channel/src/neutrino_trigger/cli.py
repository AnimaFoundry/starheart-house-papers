"""Command-line interface for deterministic offline feasibility calculations."""

from __future__ import annotations

import argparse
import json
import math
from typing import Any

from .detection import detection_probability, false_alarm_probability
from .first_arrival import required_signal_rate_hz
from .probability import exact_at_least_one, poisson_limit_at_least_one
from .simulation import evaluate_trigger_snapshot, reproduce_stancil_2012_channel


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="neutrino-trigger",
        description="Offline probabilistic trigger feasibility calculations (RESEARCH_ONLY).",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    exact = subparsers.add_parser("particle-limit", help="compare exact and Poisson probabilities")
    exact.add_argument("--particles", type=int, required=True)
    exact.add_argument("--p-eff", type=float, required=True)

    detect = subparsers.add_parser("detect", help="evaluate an illustrative Poisson gate")
    detect.add_argument("--signal-mean", type=float, required=True)
    detect.add_argument("--background-mean", type=float, default=0.0)
    detect.add_argument("--threshold", type=int, default=1)
    detect.add_argument("--decision-window-s", type=float, required=True)

    deadline = subparsers.add_parser("required-rate", help="solve rate required before a deadline")
    deadline.add_argument("--target-probability", type=float, required=True)
    deadline.add_argument("--deadline-s", type=float, required=True)
    deadline.add_argument("--background-rate-hz", type=float, default=0.0)
    deadline.add_argument("--threshold", type=int, default=1)

    subparsers.add_parser("reproduce-2012", help="reproduce Stancil et al. Poisson quantities")
    return parser


def run(arguments: list[str] | None = None) -> dict[str, Any]:
    """Parse arguments and return a JSON-serializable result."""

    args = _parser().parse_args(arguments)
    if args.command == "particle-limit":
        exact = exact_at_least_one(args.particles, args.p_eff)
        approximate = poisson_limit_at_least_one(args.particles, args.p_eff)
        return {
            "exact_binomial": exact,
            "poisson_approximation": approximate,
            "approximation_minus_exact": approximate - exact,
            "status": "analytic calculation",
        }
    if args.command == "detect":
        return evaluate_trigger_snapshot(
            args.signal_mean,
            args.background_mean,
            args.threshold,
            args.decision_window_s,
        )
    if args.command == "required-rate":
        rate = required_signal_rate_hz(
            args.target_probability,
            args.deadline_s,
            args.background_rate_hz,
            args.threshold,
        )
        if math.isinf(rate):
            verification = 1.0
            display_rate: float | str = "INFINITE"
        else:
            verification = detection_probability(
                rate * args.deadline_s,
                args.background_rate_hz * args.deadline_s,
                args.threshold,
            )
            display_rate = rate
        return {
            "required_signal_rate_hz": display_rate,
            "target_probability": args.target_probability,
            "deadline_s": args.deadline_s,
            "threshold": args.threshold,
            "background_rate_hz": args.background_rate_hz,
            "false_alarm_probability_by_deadline": false_alarm_probability(
                args.background_rate_hz * args.deadline_s,
                args.threshold,
            ),
            "verification_detection_probability": verification,
            "status": "analytic Poisson model; RESEARCH_ONLY",
        }
    return reproduce_stancil_2012_channel()


def main() -> None:
    """Console-script entry point."""

    print(json.dumps(run(), indent=2, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    main()
