# Contributing to Sanqing Fabricator

Sanqing Fabricator is presently a public concept and interface-design project. Contributions should make the idea more testable, modular, truthful, safe, and accessible—not imply that physical capability already exists.

## Useful contributions now

- architecture critiques and alternative modular designs;
- transport-neutral task, tool, observation, authorization, and audit schemas;
- synthetic fixtures, simulators, failure injection, and hostile tests;
- low-barrier teleoperation and accessibility interface proposals;
- comparisons of mobile bases, standard grippers, five-finger hands, and sensors;
- bounded parameterized fixtures and inspection workflows;
- full-cost, labor-transition, and demographic-resilience research designs;
- consent, privacy, provenance, retention, revocation, and dataset-card templates;
- threat models, hazard registers, safety-state machines, and independent red-team reviews;
- translations, diagrams, tutorials, and critical counterexamples.

## Evidence labels are mandatory

Every experiment, image, dataset, metric, and capability statement must use one primary label:

- `SYNTHETIC`
- `SIMULATION_ONLY`
- `HUMAN_CONTROLLED`
- `SUPERVISED_AUTONOMY`
- `HARDWARE_VALIDATED`
- `PRODUCTION_VALIDATED`

Do not upgrade a label because a result looks plausible. Higher labels require versioned evidence, configuration identity, test scope, known limitations, and reviewer/authorization records.

## Safety-impact declaration

Any proposal touching safety policy, authority, state transitions, motion limits, sensing used for protection, tool approval, fabrication, machine interfaces, firmware, cybersecurity, or workplace data must include:

```yaml
safety_impact:
  affected_invariants: []
  new_or_changed_hazards: []
  failure_modes: []
  hostile_tests: []
  evidence_class: "SYNTHETIC"
  evidence_refs: []
  data_rights_impact: []
  rollback_plan: ""
  independent_review_needed: true
```

A merge is not a physical deployment authorization. Protected safety-boundary changes require offline review, independent human reviewers, signed versioning, and rollback readiness.

## Data rules

- Public examples default to synthetic data and must set `synthetic: true` at artifact and record level.
- Do not upload real factory layouts, employee/bystander media, customer identifiers, recipes, control addresses, credentials, private research, or trade secrets.
- Real data requires documented collection purpose, consent/authority, access, retention, publication permission, de-identification review, provenance, license, and revocation behavior.
- Collection permission, model-training permission, cross-site use, and public release are separate.
- Emergency-stop, intervention, and near-miss episodes must not be silently relabeled as successful demonstrations.

## Schema rules

- Use UTF-8, stable English field names, ISO 8601 UTC timestamps, SI units, explicit coordinate frames, and SemVer.
- Safety-critical artifacts use SHA-256 content identity.
- Additive extensions belong under `extensions`; do not silently change the meaning of an existing field.
- A breaking change requires a schema major-version increment and migration note.
- Add or update synthetic conformance fixtures for every schema change.

## Please do not contribute

- instructions to bypass interlocks, guards, lockout, emergency stop, or authorization;
- direct Agent-to-actuator, Agent-to-printer, or Agent-to-machine-tool control paths;
- runtime self-promotion or self-modification of the protected safety boundary;
- weapon, injury, coercion, or non-consensual surveillance use cases;
- unlicensed third-party CAD, code, data, images, papers, or confidential materials;
- performance claims supported only by simulation, a demo video, or undisclosed data.

## Security and hazards

Report non-exploitable design hazards in a GitHub issue with a minimal reproducible synthetic case. Do not publicly post credentials, live control endpoints, private facility details, or actionable exploit steps against a deployed system. Use GitHub's private security-advisory channel if enabled; otherwise contact the repository owner privately before disclosure.

## License and rights

Unless a file states otherwise, contributions to this concept paper and its original schemas are dedicated under the repository's CC0 1.0 terms. By contributing, you confirm that you have the right to provide the material under those terms. Future code, hardware, datasets, models, trademarks, and patents may require separate, explicit licensing and are not automatically covered merely because this paper discusses them.

