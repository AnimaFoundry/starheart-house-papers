# Safety and authority boundary

**Status:** `CONCEPT` / `RESEARCH_ONLY` / `L0` / `NOT PEER REVIEWED`
**Evidence:** literature synthesis and `SIMULATION_ONLY` calculations
**Authority:** no physical operation; no live trading; no deployment authorization

This document is a hazard and misuse boundary, not a radiation safety case, accelerator operating procedure, market-compliance opinion, engineering design approval, or deployment manual.

## Non-negotiable boundaries

1. **No particle-beam operation.** The package contains no accelerator controls, source settings, operating sequences, radiation procedures, or machine interfaces.
2. **No live-market operation.** The package contains no broker/exchange connectivity, credentials, order protocol, deployable trading bot, or real-order path.
3. **Simulation is not capability.** Numerical outputs are illustrative unless a row in the provenance ledger identifies a measured source and scope.
4. **No automatic promotion.** Publication, a passing test, or a merged pull request does not authorize physical construction, excavation, beam generation, detector operation, or financial deployment.
5. **Fail closed on evidence.** Unknown actuation latency, yield, detector response, background, cost, siting, or market value remains unknown.

## Physical hazards

Real accelerator and detector systems can involve ionizing radiation, high voltage, strong magnetic fields, activated material, stored beam energy, pressure systems, vacuum equipment, cryogens, oxygen-deficiency hazards, heavy structures, underground access, fire, and hazardous energy. Underground siting additionally raises excavation, ground stability, water ingress, ventilation, emergency egress, land-rights, and environmental risks. Detector concepts may involve large liquid volumes, flammable or toxic materials, photodetector high voltage, or cryogenic media. These risks require qualified institutions, permits, formal hazard analysis, independent safety systems, and jurisdiction-specific controls. Nothing here supplies them.

The simulator may compare abstract source energy, detector mass, baseline, or relay count. It must not be used as an accelerator design or operating prescription. Energy and material footprints, construction emissions, heat rejection, land use, and end-of-life waste belong in any later life-cycle assessment.

## Market-integrity and financial hazards

A false authenticated trigger can create direct loss, market impact, fees, and cascading control responses. A correct but stale trigger can also be harmful. Latency-sensitive strategies may intensify arms races, shift rents without creating social surplus, disadvantage slower participants, and become invalid after exchange redesign, speed bumps, batch auctions, regulation, or competitive diffusion.

Any later market research would require independent legal, compliance, model-risk, exchange-rule, cybersecurity, kill-switch, capital-limit, and human-authorization review. This repository grants none of those permissions.

## Security boundary

A one-bit pulse is not inherently authentic or secret. Background coincidences, source spoofing, replay-like timing patterns, codebook compromise, clock faults, gate errors, detector faults, denial of service, and conventional-channel mismatch must be modeled. Authentication adds particles and latency. The safe conceptual response to ambiguity is to wait for conventional confirmation, abort, or reconcile under a separately approved policy.

## Stop conditions for interpretation

Stop and request human review if a proposed change:

- adds a physical device or live external-service interface;
- removes `SIMULATION_ONLY` labeling;
- supplies an unverified quantitative capability claim;
- treats non-detection as an authenticated zero without an availability proof;
- ignores the best plausible electromagnetic competitor;
- suppresses a false-trigger or externality term;
- converts academic equations into operational beam or trading instructions.
