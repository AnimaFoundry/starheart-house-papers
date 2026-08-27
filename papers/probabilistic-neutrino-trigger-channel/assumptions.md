# Assumptions and evidence classes

**Status:** `CONCEPT` · `RESEARCH_ONLY` · `L0` · `SIMULATION_ONLY` where noted
**Research cutoff:** 2026-08-26

The project uses four input classes. Code and prose must not silently move a value between them.

| Class | Meaning | Permitted use |
| --- | --- | --- |
| `MEASURED` | Directly reported by a primary or official source for a defined system. | Reproduce or bound only within the source's scope. |
| `ESTIMATED` / `INFERRED` | Derived from cited measurements or geometry with the derivation shown. | Sensitivity analysis with uncertainty and caveats. |
| `SYNTHETIC PARAMETER` | Chosen to explore model behavior; not observed system performance. | `SIMULATION_ONLY` charts and unit tests. |
| `UNKNOWN` / `LITERATURE GAP` | Not established by the reviewed evidence. | Remain symbolic or define a measurement target. |

## Directly verified 2012 anchor

The following values are transcribed from Stancil et al. (2012) and apply only to that demonstration. Page locators and qualifications are recorded in [`docs/source-audit.md`](docs/source-audit.md).

| Parameter | Value | Evidence class | Scope warning |
| --- | ---: | --- | --- |
| Baseline | 1.035 km | `MEASURED` as reported | Fermilab NuMI target to MINERvA configuration. |
| Rock traversed | 240 m, mostly shale | `MEASURED` as reported | Not a trans-Earth attenuation test. |
| Proton pulse duration | 8.1 microseconds | `MEASURED` as reported | Beam pulse width is not source-command latency. |
| Nominal pulse spacing | 2.2 s | `MEASURED` as reported | Limited by acceleration cycle in that facility. |
| Study intensity | 2.25e13 protons per pulse | `MEASURED` as reported | Proton count is not emitted-neutrino count or energy efficiency. |
| Registered qualifying signal mean | 0.81 events per on pulse | `MEASURED` as reported | Most signal came from upstream-rock interactions producing entering muons. |
| Full detector mass | 170 metric tons | `MEASURED` as reported | Not an effective target mass for the communication selection. |
| Central tracker mass | 3 metric tons | `MEASURED` as reported | Most communication signal was not confined to this mass. |
| Long-muon reconstruction efficiency | greater than 95% | `MEASURED` as reported | Specific selection, detector, and energy spectrum. |
| Decoded rate | about 0.1 bit/s at about 1% BER | `ESTIMATED` by source | Source calls it a rough estimate; it pooled repeated frames. |

## Synthetic scenario family

Every figure generated from these values is labeled `SIMULATION_ONLY — Illustrative assumptions; not measured system performance`. Values are selected for numerical coverage, not plausibility claims.

| Parameter | Illustrative values or range | Purpose |
| --- | --- | --- |
| Signal mean per decision gate, `lambda_s` | 0.01 to 10 | Exercise missed-trigger and saturation regimes. |
| Background mean per gate, `lambda_b` | 1e-6 to 1 | Exercise false-alarm thresholds and ROC shape. |
| Count threshold, `m` | 1 to 5 | Compare speed and false-trigger suppression. |
| Decision deadline | 1 microsecond to 100 milliseconds | Expose accumulation-rate requirements without asserting source actuation. |
| Endpoint central angle | 0 to pi radians | Compare spherical arc and chord geometry. |
| Fiber speed | 2.0e8 m/s | Simplified scenario; route, equipment, and last mile are separate. |
| Free-space speed | exact `c` | Propagation-only upper bound, not an end-to-end network latency. |
| Opportunity value curve | exponential decay | Illustrative non-linear alpha decay; not a profit estimate. |
| Signal opportunity rate, false-trigger loss, pulse cost, CAPEX | dimensioned synthetic grids | Test break-even algebra, not market performance. |
| Relay spot-size exponent and regeneration delay | synthetic grids | Explore phase boundaries; not a beam-physics claim. |

## Values intentionally not supplied

The reviewed evidence does not establish a present, integrated value for the proposed system's source-command-to-beam latency, emitted neutrinos per joule, usable long-baseline beam divergence, qualifying interactions per joule per deadline, compact-detector decision latency, authenticated false-trigger probability, pulse variable cost, fixed infrastructure cost, or incremental value per successful trigger. These remain `UNKNOWN` until a traceable source or measurement is added.

## Modeling approximations

- Independent particles give a binomial interaction model; the Poisson approximation is tested rather than assumed exact.
- Poisson signal and background counts are an explicit model, not a guarantee about correlated detector faults or burst backgrounds.
- Hop detections are independent in the first relay model; common-mode source, timing, environment, and codebook failures violate that approximation.
- A spherical Earth with a stated radius is a geometry model; real routes and density profiles require geodesy and tomography inputs.
- A synthetic inverse-square or power-law beam-spread scenario is not a universal neutrino-beam law.
- Economic inputs are conditional scenarios. No proprietary feed or trading record is used.
