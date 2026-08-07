# Sanqing Fabricator normative concept specification

Version: `0.1.0`  
Status: `CONCEPT` / `RESEARCH_ONLY` / `L0`  
Normative language: RFC 2119-style `MUST`, `MUST NOT`, `SHOULD`, and `MAY`

This is an interface proposal, not an implementation, safety certification, capability claim, or deployment authorization. The canonical current-state summary is [`../agent-manifest.json`](../agent-manifest.json).

## 1. Interoperability conventions

- Encoding MUST be UTF-8.
- Timestamps MUST use ISO 8601 UTC.
- Physical quantities MUST use SI units unless a field explicitly declares another unit.
- Every spatial value MUST name its coordinate frame.
- Every schema, task, skill, tool, deployment, and policy MUST be versioned.
- Safety-critical artifacts MUST be content-addressed with SHA-256.
- Observations MUST identify whether they are `measured`, `estimated`, or `inferred`.
- Unknown fields in a safety-critical message MUST be rejected unless they occur under the non-authoritative `extensions` object.
- Examples and fixtures MUST set `synthetic: true`; they MUST NOT be presented as empirical results.

The logical interfaces are transport-neutral. ROS 2, MQTT, CAN, EtherCAT, or another implementation MAY be used only behind adapters that preserve authority and safety boundaries.

## 2. Trust boundaries

The system has three distinct planes:

1. **Safety plane** — independent hardware and safety-rated logic with final veto authority.
2. **Control plane** — converts approved bounded skills or human teleoperation input into constrained motion requests.
3. **Agent plane** — interprets observations and submits proposals through an authenticated gateway.

The Agent plane MUST NOT directly access motor drives, safety I/O, energy-isolation devices, fabrication controls, or machine-tool registers. The control plane MUST NOT override the safety plane. A printer or machine tool MUST retain its native interlocks and separate authorization.

Wireless transport MAY carry ordinary teleoperation, telemetry, and software stop requests. It MUST NOT be the sole emergency-stop channel. Communication loss MUST produce a risk-assessed deterministic safe state and MUST NOT trigger automatic resume when the link returns.

## 3. Authority model

Every deployment declares both:

- `supported_level`: the highest level backed by versioned implementation evidence;
- `authorized_level`: the highest level approved for the current site, task, people, tools, and time window.

The effective level is the lower value. Runtime learning, model replacement, repeated success, elapsed time, or an Agent message MUST NOT raise either level.

| Action | Human operator | Agent | Safety controller |
| --- | --- | --- | --- |
| Propose a task | MAY | MAY | N/A |
| Approve physical execution | authorized human only | MUST NOT | MAY veto |
| Request ordinary/protective stop | MAY | MAY | MAY |
| Trigger hardware emergency stop | MAY | software request is supplementary only | MUST |
| Reset emergency stop | local authorized human after inspection | MUST NOT | validates preconditions only |
| Propose a tool design | MAY | MAY | MAY veto |
| Approve tool fabrication/use | authorized human only | MUST NOT | MAY veto |
| Promote autonomy | offline governance process | MUST NOT | MUST NOT self-promote |
| Modify protected safety boundary | offline reviewed release only | MUST NOT | MUST NOT at runtime |

Permission to stop SHOULD have minimal friction. Permission to resume MUST revalidate all preconditions and require explicit authorization.

## 4. System state machine

```text
OFF → BOOTING → SAFE_IDLE
SAFE_IDLE → MANUAL_TELEOP | SHADOW_MODE | SUPERVISED_AUTO | BOUNDED_CELL_AUTO
ANY_ACTIVE_STATE → PROTECTIVE_STOP
ANY_STATE → EMERGENCY_STOP | FAULT
```

Only a signed deployment configuration and an authorized human decision can enable a higher active state.

Recovery is never a direct transition back to motion:

```text
PROTECTIVE_STOP
  → cause diagnosed
  → task, tool, sensors and safety envelope revalidated
  → explicit resume authorization
  → SAFE_IDLE

EMERGENCY_STOP
  → physical channels released
  → hazardous-energy isolation verified
  → fault inspection completed
  → local authorized human manual reset
  → SAFE_IDLE
```

Power cycling, process restart, model reload, heartbeat recovery, or wireless reconnection MUST NOT resume the interrupted motion.

## 5. Task lifecycle

```text
PROPOSED → VALIDATED → AUTHORIZED → QUEUED → EXECUTING
EXECUTING → COMPLETED | FAILED | ABORTED | PROTECTIVE_STOP
```

Changing task intent, target, skill version, tool identity, zone, risk class, safety envelope, environment assumptions, or artifact hashes invalidates the previous authorization and returns the task to `PROPOSED`.

Success criteria and abort conditions SHOULD be machine-evaluable. Natural language MAY explain them but MUST NOT enlarge scope.

## 6. Tool-selection and fabrication lifecycle

An Agent SHOULD search the authorized tool registry before proposing a new design. If no authorized tool fits, it MUST abstain from physical execution and MAY create a design proposal.

```text
PROPOSED
  → DESIGN_LOCKED
  → STATIC_CHECKED
  → SIMULATION_PASSED
  → HAZARD_REVIEWED
  → HUMAN_APPROVED
  → FABRICATED
  → INSPECTED
  → REGISTERED
  → LOW_ENERGY_TESTED
  → AUTHORIZED
```

Any failure enters `REJECTED` or `QUARANTINED`; no stage may be skipped. Before fabrication, the CAD source, derived geometry, material, slicer, slicing parameters, printer identity, printer configuration, and relevant software/model versions MUST be hash-locked. Any change produces a new tool version and invalidates previous approval.

Simulation does not authorize fabrication. Fabrication does not authorize use. Initial use MUST occur in an isolated low-energy test under human supervision. Authorization is limited to registered tasks, zones, loads, speeds, temperatures, duty cycles, mounting interfaces, and expiration time.

## 7. Sensor and observation integrity

A sensor registration SHOULD include:

```text
sensor_id, sensor_type, frame_id, units, sample_rate_hz,
expected_latency_ms, measurement_range, accuracy, resolution,
calibration_ref, calibration_due_at, max_freshness_ms,
health_state, required_redundancy, privacy_class
```

An observation SHOULD include:

```text
observation_id, sensor_id, kind, measured_at, received_at,
frame_id, transform_version, value, units, covariance,
confidence, quality_flags, occlusion, calibration_ref,
source_sha256, synthetic
```

Inferred values MUST NOT be represented as measurements. Model confidence MUST NOT replace deterministic safety conditions. Stale data, unknown transforms, expired calibration, occlusion, time-sync failure, localization uncertainty, or redundant-sensor disagreement MUST cause a bounded degradation, rejection, or stop defined by the safety case. Missing personnel detection MUST NOT be interpreted as an empty workspace.

## 8. Teleoperation episode and physical-data loop

Each recorded episode SHOULD bind:

```text
episode_id, schema_version, evidence_class, synthetic,
collection_purpose, consent_ref, privacy_class,
operator_pseudonym, deployment_id, task_ref, environment_ref,
hardware_manifest_sha256, software_manifest_sha256,
calibration_refs, started_at, ended_at, time_sync_quality,
observation_stream_ref, operator_input_stream_ref,
agent_proposal_stream_ref, safety_override_stream_ref,
executed_command_stream_ref, outcome_stream_ref,
interventions, near_misses, stop_events, known_biases,
redactions, license, retention_policy
```

Human intent, Agent proposals, control-plane clipping, safety overrides, and actual actuator commands MUST remain distinguishable. Near misses, emergency stops, and corrective interventions MUST NOT be silently treated as successful demonstrations.

Collection consent, model-training permission, public-release permission, and cross-site reuse are separate grants. Each dataset MUST document purpose, provenance, access, retention, revocation behavior, de-identification, known bias, prohibited uses, and the employment context in which consent was obtained. Because workplace consent may be constrained by power imbalance, a real pilot SHOULD offer a non-retaliatory opt-out and independent review.

## 9. Audit event

Every consequential proposal, decision, modification, execution, stop, resume, tool transition, and data action SHOULD emit an append-only audit event containing:

```text
event_id, event_schema_version, sequence, timestamp_utc,
monotonic_time_ns, deployment_id, session_id, actor, action,
risk_class, state_before, state_after, input_refs, output_refs,
policy_decision, authorization_ref, task_ref, tool_ref,
model_id, model_sha256, software_sha256, configuration_sha256,
sensor_snapshot_refs, result, stop_reason, human_approval_ref,
evidence_class, synthetic, previous_event_sha256,
event_sha256, signature, redaction_manifest_ref
```

History is append-only: corrections add events and new versions; they do not overwrite old events. When privacy obligations require payload deletion, the system SHOULD retain a minimal tombstone that records the lawful deletion without retaining the protected content.

## 10. Minimum hostile tests

A conforming prototype MUST use synthetic fixtures to show that:

- missing, invalid, expired, replayed, out-of-order, or out-of-scope authorization is rejected;
- unsupported schema versions and unknown safety-critical fields are rejected;
- heartbeat loss, stale sensors, localization uncertainty, and conflicting redundant sensors reach the specified safe state;
- wireless loss cannot disable the hardware emergency-stop path;
- a single emergency-stop channel fault is detected;
- an Agent or network recovery cannot reset emergency stop or resume motion;
- an Agent cannot reach direct motor, printer, machine-tool, or safety-I/O interfaces;
- a tool hash or material change invalidates approval;
- a simulated but unapproved tool cannot be fabricated or used;
- autonomy cannot be raised by runtime messages;
- safety policy, trusted keys, tool approval, and audit history cannot be rewritten by the Agent;
- an audit-chain break is detectable;
- all fixtures identify themselves as synthetic.

Passing these tests is necessary for later work but is not by itself evidence of hardware or production safety.

