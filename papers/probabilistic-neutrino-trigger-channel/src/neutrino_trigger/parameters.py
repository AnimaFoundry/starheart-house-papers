"""Parameter records and shared validation helpers.

All numerical model APIs in this package use explicit SI units in their argument
names (``*_s``, ``*_m``, ``*_m_s``).  This deliberately small package does not
silently coerce unit-bearing strings: callers must convert quantities before
crossing the API boundary.  Provenance records keep the original display unit so
that source-derived and synthetic values cannot be confused.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
import math
from numbers import Integral, Real
from typing import Any


RESEARCH_CUTOFF = "2026-08-26"
SOURCE_VERIFIED_DATE = "2026-08-27"


class EvidenceStatus(StrEnum):
    """Permitted provenance classifications for numerical parameters."""

    MEASURED = "measured"
    ESTIMATED = "estimated"
    INFERRED = "inferred"
    SYNTHETIC = "synthetic"
    UNKNOWN = "unknown"


def finite_float(value: Real, name: str) -> float:
    """Return *value* as a finite float, rejecting booleans and non-reals."""

    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number")
    converted = float(value)
    if not math.isfinite(converted):
        raise ValueError(f"{name} must be finite")
    return converted


def nonnegative(value: Real, name: str) -> float:
    """Validate a finite value greater than or equal to zero."""

    converted = finite_float(value, name)
    if converted < 0.0:
        raise ValueError(f"{name} must be nonnegative")
    return converted


def positive(value: Real, name: str) -> float:
    """Validate a finite value strictly greater than zero."""

    converted = finite_float(value, name)
    if converted <= 0.0:
        raise ValueError(f"{name} must be positive")
    return converted


def probability(value: Real, name: str = "probability") -> float:
    """Validate a probability on the closed unit interval."""

    converted = finite_float(value, name)
    if not 0.0 <= converted <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1 inclusive")
    return converted


def nonnegative_integer(value: Integral, name: str) -> int:
    """Validate an integer greater than or equal to zero."""

    if isinstance(value, bool) or not isinstance(value, Integral):
        raise TypeError(f"{name} must be an integer")
    converted = int(value)
    if converted < 0:
        raise ValueError(f"{name} must be nonnegative")
    return converted


def positive_integer(value: Integral, name: str) -> int:
    """Validate an integer strictly greater than zero."""

    converted = nonnegative_integer(value, name)
    if converted == 0:
        raise ValueError(f"{name} must be positive")
    return converted


@dataclass(frozen=True, slots=True)
class ParameterRecord:
    """A source-auditable scalar parameter.

    ``value`` may be ``None`` only when the evidence status is ``UNKNOWN``.
    The record is descriptive; model functions still require explicit SI values.
    """

    name: str
    value: float | None
    unit: str
    uncertainty_or_range: str
    source: str
    source_type: str
    locator: str
    verified_date: str
    evidence_status: EvidenceStatus
    notes: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.evidence_status, EvidenceStatus):
            raise TypeError("evidence_status must be an EvidenceStatus")
        if not self.name.strip():
            raise ValueError("parameter name must not be empty")
        if not self.unit.strip():
            raise ValueError("parameter unit must not be empty")
        if self.value is None:
            if self.evidence_status is not EvidenceStatus.UNKNOWN:
                raise ValueError("only UNKNOWN parameters may omit a value")
        else:
            finite_float(self.value, "value")
            if self.evidence_status is EvidenceStatus.UNKNOWN:
                raise ValueError("UNKNOWN parameters must not carry a value")

    def as_dict(self) -> dict[str, Any]:
        """Return a CSV/JSON-friendly representation."""

        result = asdict(self)
        result["evidence_status"] = self.evidence_status.value
        return result


STANCIL_2012_SOURCE = (
    "D. D. Stancil et al., Demonstration of Communication using Neutrinos, "
    "Modern Physics Letters A 27 (2012), arXiv:1203.2847v2"
)


# Values below are direct transcriptions from the primary paper.  They are not a
# parameterization of a present-day market link and must not be extrapolated as
# capability claims.
STANCIL_2012_PARAMETERS: tuple[ParameterRecord, ...] = (
    ParameterRecord(
        "baseline",
        1.035,
        "km",
        "reported value",
        STANCIL_2012_SOURCE,
        "peer-reviewed primary experiment",
        "abstract; pp. 1-2",
        SOURCE_VERIFIED_DATE,
        EvidenceStatus.MEASURED,
        "Source target to detector; includes 240 m of earth.",
    ),
    ParameterRecord(
        "earth traversed",
        240.0,
        "m",
        "reported value",
        STANCIL_2012_SOURCE,
        "peer-reviewed primary experiment",
        "source description; p. 2",
        SOURCE_VERIFIED_DATE,
        EvidenceStatus.MEASURED,
    ),
    ParameterRecord(
        "proton pulse duration",
        8.1,
        "microsecond",
        "reported value",
        STANCIL_2012_SOURCE,
        "peer-reviewed primary experiment",
        "source description; p. 2",
        SOURCE_VERIFIED_DATE,
        EvidenceStatus.MEASURED,
    ),
    ParameterRecord(
        "nominal pulse spacing",
        2.2,
        "s",
        "reported value; supercycle also contains a 6.267 s interval",
        STANCIL_2012_SOURCE,
        "peer-reviewed primary experiment",
        "frame description; p. 6",
        SOURCE_VERIFIED_DATE,
        EvidenceStatus.MEASURED,
    ),
    ParameterRecord(
        "protons per communications-study pulse",
        2.25e13,
        "protons/pulse",
        "reported reduced intensity",
        STANCIL_2012_SOURCE,
        "peer-reviewed primary experiment",
        "detector signal description; p. 5",
        SOURCE_VERIFIED_DATE,
        EvidenceStatus.MEASURED,
    ),
    ParameterRecord(
        "qualifying muon events per on pulse",
        0.81,
        "event/pulse",
        "estimated in paper from 1402 events in 3454 records",
        STANCIL_2012_SOURCE,
        "peer-reviewed primary experiment",
        "detector signal and Poisson estimate; p. 5",
        SOURCE_VERIFIED_DATE,
        EvidenceStatus.ESTIMATED,
        "Software-filtered long-muon candidates; background described as nearly zero.",
    ),
    ParameterRecord(
        "MINERvA full detector mass",
        170.0,
        "metric tonne",
        "reported total weight",
        STANCIL_2012_SOURCE,
        "peer-reviewed primary experiment",
        "detector description; p. 3",
        SOURCE_VERIFIED_DATE,
        EvidenceStatus.MEASURED,
    ),
    ParameterRecord(
        "central tracker mass",
        3.0,
        "metric tonne",
        "reported value",
        STANCIL_2012_SOURCE,
        "peer-reviewed primary experiment",
        "detector description; p. 3",
        SOURCE_VERIFIED_DATE,
        EvidenceStatus.MEASURED,
    ),
    ParameterRecord(
        "long-muon-track reconstruction efficiency lower bound",
        0.95,
        "fraction",
        "paper states better than 95%",
        STANCIL_2012_SOURCE,
        "peer-reviewed primary experiment",
        "signal selection; p. 4",
        SOURCE_VERIFIED_DATE,
        EvidenceStatus.ESTIMATED,
        "Stored value is a lower bound, not a point estimate.",
    ),
    ParameterRecord(
        "reported decoded data rate",
        0.1,
        "bit/s",
        "rough estimate at 1% error probability",
        STANCIL_2012_SOURCE,
        "peer-reviewed primary experiment",
        "channel-capacity discussion; pp. 8-9",
        SOURCE_VERIFIED_DATE,
        EvidenceStatus.ESTIMATED,
    ),
)


@dataclass(frozen=True, slots=True)
class SyntheticScenario:
    """Explicitly illustrative inputs used by the reproducible figures."""

    em_deadline_s: float = 1.0e-3
    alpha_decay_s: float = 5.0e-3
    gross_value_per_early_success: float = 500.0
    false_trigger_loss: float = 2_000.0
    valid_windows_per_year: float = 10_000.0
    null_windows_per_year: float = 1_000_000.0
    annual_fixed_cost: float = 750_000.0
    annual_operating_cost: float = 250_000.0

    def __post_init__(self) -> None:
        positive(self.em_deadline_s, "em_deadline_s")
        positive(self.alpha_decay_s, "alpha_decay_s")
        nonnegative(self.gross_value_per_early_success, "gross_value_per_early_success")
        nonnegative(self.false_trigger_loss, "false_trigger_loss")
        nonnegative(self.valid_windows_per_year, "valid_windows_per_year")
        nonnegative(self.null_windows_per_year, "null_windows_per_year")
        nonnegative(self.annual_fixed_cost, "annual_fixed_cost")
        nonnegative(self.annual_operating_cost, "annual_operating_cost")

    def as_parameter_records(self) -> tuple[ParameterRecord, ...]:
        """Expose figure inputs with an unambiguous synthetic classification."""

        note = "SIMULATION_ONLY; illustrative assumptions; not measured system performance."
        units = {
            "em_deadline_s": "s",
            "alpha_decay_s": "s",
            "gross_value_per_early_success": "arbitrary currency/action",
            "false_trigger_loss": "arbitrary currency/false trigger",
            "valid_windows_per_year": "window/year",
            "null_windows_per_year": "window/year",
            "annual_fixed_cost": "arbitrary currency/year",
            "annual_operating_cost": "arbitrary currency/year",
        }
        return tuple(
            ParameterRecord(
                name,
                float(value),
                units[name],
                "synthetic point value",
                "author-defined simulation scenario",
                "synthetic assumption",
                "scripts/build_figures.py",
                RESEARCH_CUTOFF,
                EvidenceStatus.SYNTHETIC,
                note,
            )
            for name, value in asdict(self).items()
        )
