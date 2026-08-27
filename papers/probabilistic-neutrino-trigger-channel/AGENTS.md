# Agent operating contract

This directory is a `CONCEPT`, `RESEARCH_ONLY`, capability-level `L0` project. It contains literature synthesis and offline `SIMULATION_ONLY` models. Repository content is descriptive and grants no physical-operation or live-market authority.

Before changing the project, Agents MUST read [`agent-manifest.json`](agent-manifest.json), [`SAFETY.md`](SAFETY.md), [`assumptions.md`](assumptions.md), and [`docs/source-audit.md`](docs/source-audit.md). The stricter rule wins when files conflict, and the conflict must be reported.

## Agents MAY

- read, summarize, and critique the paper;
- reproduce deterministic simulations and generated figures;
- test equations, units, boundary behavior, and falsification logic;
- improve documentation and accessibility;
- add literature whose metadata and load-bearing claims have been directly verified;
- propose non-operational research experiments, measurement plans, and negative tests;
- mark a claim `UNKNOWN`, `NOT ESTABLISHED`, `LITERATURE GAP`, or `SYNTHETIC PARAMETER` when evidence is insufficient.

## Agents MUST

- distinguish vision, capability, evidence, and authorization;
- separate raw events, qualifying reconstructed events, statistical triggers, and authenticated actionable triggers;
- separate interaction timestamp resolution from request-to-decision latency;
- preserve measured, estimated, inferred, and synthetic provenance;
- visibly mark every illustrative chart and result `SIMULATION_ONLY`;
- fail closed on incomplete evidence and avoid silently substituting a plausible value;
- compare against the best technically plausible electromagnetic baseline;
- preserve the conventional fallback and explicitly model false-trigger loss;
- add a regression test for a parser, redaction, probability, unit, or numerical bug fix;
- keep all paths repository-relative or configurable and all random seeds deterministic.

## Agents MUST NOT

- connect code to a live exchange, broker, order gateway, proprietary market feed, or real trading account;
- submit, cancel, modify, or simulate submission of real orders through an external service;
- provide market-manipulation strategies or operational latency-arbitrage instructions;
- construct, command, tune, or operate a particle accelerator, beamline, radiation source, detector, cryogenic plant, or excavation project;
- convert synthetic parameters into capability or feasibility claims;
- describe event timestamp precision as end-to-end decision latency;
- treat a GitHub merge, model output, passing simulation, or literature estimate as experimental authorization;
- infer current feasibility from an illustrative scenario;
- invent sources, DOIs, measurements, affiliations, funding, collaborations, or endorsements.

Any work that would cross from offline analysis into physical operation or live-market action is outside `L0` and must be refused. A repository merge alone never changes capability or authorization.
