# When One Bit Is Enough

## Probabilistic Neutrino–Electromagnetic Trigger Channels for Latency-Sensitive Markets

**Author:** AnimaFoundry
**Research cutoff:** 2026-08-26
**Status:** `CONCEPT` · `RESEARCH_ONLY` · `L0` · `NOT PEER REVIEWED` · `NO CURRENT FEASIBILITY CLAIM`

> A decision-theoretic feasibility framework for using a probabilistic neutrino pulse as an early one-bit trigger while retaining a conventional electromagnetic channel as the reliable fallback.

This project asks whether a particle-counting channel that is inadequate for ordinary networking could nevertheless have positive *incremental* decision value before a hard deadline. It does not claim that a practical neutrino trading network exists. It contains literature synthesis and deterministic `SIMULATION_ONLY` calculations; it grants neither particle-beam operating authority nor live-market access.

The architecture is deliberately asymmetric:

```text
source event
   +-- conventional electromagnetic message --> reliable full state and fallback
   +-- probabilistic neutrino pulse ----------> optional early positive trigger
```

A missed neutrino pulse forfeits only the possible latency advantage because the conventional message still arrives. A false authenticated trigger can create a loss, so false-alarm probability, authentication overhead, end-to-end actuation and detection latency, and the best plausible electromagnetic baseline are first-class variables.

## Present verdict

| Question | Current assessment |
| --- | --- |
| Physical possibility | **Established in principle** for low-rate neutrino communication by Stancil et al. (2012), not for this proposed end-to-end use case. |
| Present engineering feasibility | **Unsupported by verified evidence.** No cited system establishes the required source-command latency, qualifying-event yield per joule, compact detector performance, or authenticated decision latency. |
| Present HFT feasibility | **Negative under the directly verified 2012 experimental anchor; otherwise indeterminate where required inputs remain `UNKNOWN`.** |
| Dominant bottleneck | Qualifying reconstructed interactions delivered before the electromagnetic deadline, including source actuation and receiver decision time. |
| Break-even trigger | Positive annual incremental value after false-trigger losses, pulse cost, operating cost, and annualized fixed cost. |
| Falsification condition | If the best achievable distribution of authenticated decision times cannot put sufficient evidence before the best electromagnetic route at tolerable false-alarm and cost levels, the commercial hypothesis fails. |

The point of the package is to identify the inequality that would have to change, not to make an illustrative parameter set look like measured performance.

## Repository map

- [`paper/main.pdf`](paper/main.pdf): compiled human-readable concept paper.
- [`paper/main.tex`](paper/main.tex): auditable LaTeX source and derivations.
- [`research-targets.md`](research-targets.md): subsystem baselines, break-even targets, gaps, uncertainty, levers, and falsifiers.
- [`assumptions.md`](assumptions.md): strict separation of measured, inferred, unknown, and synthetic inputs.
- [`docs/source-audit.md`](docs/source-audit.md): page-level audit of load-bearing sources.
- [`results/parameter_provenance.csv`](results/parameter_provenance.csv): machine-readable provenance ledger.
- [`results/figure_parameters.csv`](results/figure_parameters.csv): exact evidence status and inputs for every plotted scenario.
- [`results/relay_model_summary.csv`](results/relay_model_summary.csv): ideal, synthetic-divergence, and fail-closed literature-informed relay runs.
- [`src/neutrino_trigger/`](src/neutrino_trigger/): deterministic offline models.
- [`scripts/reproduce_2012_channel.py`](scripts/reproduce_2012_channel.py): reproduction of the 2012 Poisson-channel quantities.
- [`scripts/build_figures.py`](scripts/build_figures.py) and [`scripts/build_tables.py`](scripts/build_tables.py): reproducible synthetic outputs.
- [`AGENTS.md`](AGENTS.md), [`SAFETY.md`](SAFETY.md), and [`agent-manifest.json`](agent-manifest.json): authority and evidence boundaries.

## Reproduction

Python 3.11 or newer is required.

```bash
make install
make test
make figures
make paper
make all
```

`make install` installs the exact versions in `requirements-lock.txt`; `make paper` requires Tectonic 0.17.0. Equivalent Python and compiler commands are documented in Appendix C of the paper. The scripts use deterministic seeds and public, explicit inputs. After dependencies, Tectonic's TeX bundle, and source files are obtained, no network, private dataset, proprietary feed, accelerator interface, exchange connection, broker credential, or order-entry system is required.

Every synthetic figure visibly states:

> SIMULATION_ONLY — Illustrative assumptions; not measured system performance

## Experimental anchor

The code first reproduces quantities reported in D. D. Stancil et al., “Demonstration of Communication using Neutrinos,” *Modern Physics Letters A* 27(12), 1250077 (2012), doi:10.1142/S0217732312500770, arXiv:1203.2847. The paper used the NuMI beam and MINERvA detector over 1.035 km, including 240 m of rock, and modeled count records as a Poisson channel. Reproducing that result does not establish a latency-sensitive trans-Earth trigger.

## AI-assistance disclosure

OpenAI Codex assisted with literature organization, software implementation, and drafting. All claims, citations, calculations, and interpretations require human review.

## License

Original repository content is released under the root repository's [CC0 1.0 Universal dedication](../../LICENSE). Third-party sources retain their original rights.
