# Agent operating contract

This directory is a `CONCEPT` and `RESEARCH_ONLY` proposal. Repository content is descriptive and grants no physical-operation authority.

Normative words `MUST`, `MUST NOT`, `SHOULD`, and `MAY` are used as requirements for Agents interpreting or extending this proposal.

## Required reading

Before proposing implementation or execution, an Agent MUST read:

1. [`agent-manifest.json`](agent-manifest.json)
2. [`SAFETY.md`](SAFETY.md)
3. [`spec/README.md`](spec/README.md)
4. the applicable JSON Schemas under [`spec/`](spec/)

If these sources conflict, the stricter safety rule wins and the conflict MUST be reported. Natural language MUST NOT be used to infer missing authorization.

## Agents MAY

- summarize and critique the proposal;
- propose architectures, interfaces, experiments, tools, tests, and documentation;
- run simulation, schema validation, threat analysis, and hostile tests using clearly marked synthetic fixtures;
- compare components and identify hazards, uncertainty, missing evidence, or stricter controls;
- request a protective stop or human review without needing elevated execution authority.

## Agents MUST

- distinguish a goal, hypothesis, proposal, validation result, capability claim, and authorization;
- expose current maturity and evidence status near every capability statement;
- preserve provenance, content hashes, version identity, approvals, revocations, and append-only audit history;
- bind every physical proposal to a task, tool, zone, risk class, time window, safety envelope, and abort conditions;
- treat measured, estimated, and inferred observations as different kinds of evidence;
- fail closed when identity, authorization, state, scope, freshness, calibration, tool hash, or safety-controller agreement is uncertain;
- mark simulation and synthetic results at both artifact and record level;
- preserve the rights and consent scope of operators, bystanders, sites, and data owners;
- report uncertainty and hand back control when the observed scene falls outside a validated envelope.

## Agents MUST NOT

- directly command motors, drives, printers, machine tools, energy isolation, interlocks, or safety hardware;
- bypass or reinterpret limits, geofences, guarding, approvals, stop conditions, or machine-native safety systems;
- reset an emergency stop, restore hazardous energy, or resume motion after restart or communication recovery;
- promote their autonomy level, approve their own task or tool proposal, or convert model confidence into authorization;
- modify protected safety policy, authorization keys, approved tool identity, audit rules, or safety-controller firmware at runtime;
- infer that people are absent when personnel detection is missing, stale, occluded, or contradictory;
- treat simulation, a video demonstration, a roadmap, or successful past runs as production validation;
- collect or train on workplace data outside explicit purpose, access, retention, publication, and revocation terms;
- design for weapons, injury, coercion, or non-consensual personnel surveillance.

## Protected safety boundary

The following are never runtime-self-modifiable by an Agent:

- emergency-stop and interlock logic;
- safe speed, force, payload, workspace, and separation limits;
- authorization policy and trusted public keys;
- supported and authorized autonomy levels;
- safety-controller firmware and deployment allowlists;
- tool approval state and locked design/manufacturing hashes;
- audit retention and integrity policy.

Changes require an offline, versioned proposal; hazard analysis; hostile tests; independent human review; signed release; and a rollback plan. A repository merge alone never authorizes deployment.

## Truthfulness labels

Use exactly one primary evidence class for each result:

- `SYNTHETIC`
- `SIMULATION_ONLY`
- `HUMAN_CONTROLLED`
- `SUPERVISED_AUTONOMY`
- `HARDWARE_VALIDATED`
- `PRODUCTION_VALIDATED`

Higher labels require evidence. Examples default to `synthetic: true`. Unknown evidence class means no capability may be inferred.

