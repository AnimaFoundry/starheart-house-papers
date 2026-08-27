#!/usr/bin/env python3
"""Reproduce the core Stancil et al. (2012) Poisson-channel calculation."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from neutrino_trigger.simulation import reproduce_stancil_2012_channel  # noqa: E402


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "results" / "reproduction_2012_channel.csv",
        help="CSV output path (default: results/reproduction_2012_channel.csv)",
    )
    return parser


def main() -> None:
    args = _parser().parse_args()
    result = reproduce_stancil_2012_channel()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = (
        "combined_frames",
        "effective_signal_mean",
        "threshold_one_detection_probability",
        "theoretical_uncoded_ber",
        "incident_proton_kinetic_energy_per_pulse_j",
        "qualifying_events_per_incident_proton_beam_joule",
        "source",
        "evidence_status",
    )
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in result["rows"]:
            writer.writerow(
                {
                    **row,
                    "incident_proton_kinetic_energy_per_pulse_j": result[
                        "incident_proton_kinetic_energy_per_pulse_j"
                    ],
                    "qualifying_events_per_incident_proton_beam_joule": result[
                        "qualifying_events_per_incident_proton_beam_joule"
                    ],
                    "source": result["source"],
                    "evidence_status": result["evidence_status"],
                }
            )
    print(json.dumps(result, indent=2, sort_keys=True))
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
