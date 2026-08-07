# Safety model and promotion gates

Status: `CONCEPT` / `RESEARCH_ONLY` / `L0`  
Last standards-link review: `2026-08-07`

This document is a threat model and design direction. It is not a safety case, certification, legal opinion, deployment manual, or claim of compliance. Final requirements depend on the actual robot, task, load, tool, facility, people, jurisdiction, and integration. Qualified machinery, functional-safety, electrical, cybersecurity, occupational-safety, data-protection, and domain specialists must determine applicability and validate a real system.

## Safety thesis

Sanqing Fabricator couples a mobile robot, manipulator, end effector, teleoperation system, industrial controls, fabrication equipment, AI decision support, and workplace-data platform. No single model, component certificate, simulation, or README can establish the safety of that combined machine.

> The Agent may propose a plan, but it is never the safety controller. “无人” must never mean “无人负责”—removing an operator from a task does not remove the named people and organizations accountable for the machine, cell, data, and change process.

## Non-negotiable invariants

1. **Independent safety plane.** Emergency stop, guarding, safe motion, braking, interlocks, energy isolation, and protective sensing are independent of the Agent, ordinary vision, cloud service, and Wi-Fi.
2. **No direct Agent actuation.** An Agent may submit a bounded proposal; it never writes raw motor, drive, PLC, printer, machine-tool, interlock, or safety-I/O commands.
3. **Local final authority.** The safety controller and native machine interlocks have final veto authority.
4. **Fail closed.** Missing, stale, invalid, conflicting, replayed, out-of-scope, or unverifiable identity, authorization, state, sensor, tool, or artifact data means deny, degrade, or stop.
5. **No automatic restart.** Power restoration, process restart, model reload, emergency-stop release, or wireless reconnection cannot resume motion.
6. **Stopping is not always de-energizing.** A vertical axis, suspended load, pressure, spring, heat, battery, capacitor, or rotating equipment may require a task-specific controlled stop, hold, support, and isolation sequence.
7. **No online safety mutation.** Runtime learning cannot change safety policy, approved skills, autonomy level, trusted keys, tool approval, or control limits.
8. **No self-approval.** An Agent cannot approve its own task, tool design, fabrication request, evidence, or promotion.
9. **Simulation is not authorization.** Passing simulation is one input to review, never permission to fabricate or operate.
10. **Named responsibility.** Every real deployment and change needs named owners for the integrated machine, cell, model, tool, data, cybersecurity, and incident response.

## Standards are inputs, not a blanket certificate

The following official sources are useful design references; their applicability and current editions must be rechecked for a real deployment.

- [ISO 12100:2010](https://www.iso.org/standard/51528.html) provides the overall machinery risk-assessment and risk-reduction framework.
- [ISO 10218-1:2025](https://www.iso.org/standard/73933.html) and [ISO 10218-2:2025](https://www.iso.org/standard/73934.html) address industrial robots and robot applications. Their published scopes do not by themselves cover the mobility created by mounting/integrating the manipulator on a mobile platform.
- [ISO 3691-4:2023](https://www.iso.org/standard/83545.html) addresses driverless industrial trucks and their systems; its scope excludes purely remote-controlled trucks, so system mode matters.
- [ISO/TS 15066:2016](https://www.iso.org/standard/62996.html) is a reference for collaborative robot applications and is marked for revision.
- [ISO 13849-1:2023](https://www.iso.org/standard/73481.html), [ISO 13849-2:2012](https://www.iso.org/standard/53640.html), [ISO 13850:2015](https://www.iso.org/standard/59970.html), and [IEC 60204-1 Ed. 6.1](https://webstore.iec.ch/en/publication/71256) are relevant to safety-related control, validation, emergency-stop principles, and machinery electrical equipment.
- [ISO/TR 22100-4:2018](https://www.iso.org/standard/73335.html) connects machinery safety with cybersecurity threats.
- [IEC 62443-3-3](https://webstore.iec.ch/en/publication/7033), [IEC 62443-4-1](https://webstore.iec.ch/en/publication/33615), and [IEC 62443-4-2](https://webstore.iec.ch/en/publication/34421) are useful industrial-control cybersecurity references.
- [ROS 2 SROS2](https://github.com/ros2/sros2), the [ROS 2 DDS security design](https://design.ros2.org/articles/ros2_dds_security.html), and the [ROS 2 threat model](https://design.ros2.org/articles/ros2_threat_model.html) can support authentication, encryption, and least privilege. Secure communications are not a substitute for safety-rated controls.
- [NIST AI RMF 1.0](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10), the [NIST Privacy Framework](https://www.nist.gov/privacy-framework/privacy-framework), and [NIST CSF 2.0](https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20) provide voluntary lifecycle risk-management references; they are not product certifications.
- [ISO/ASTM 52920:2023](https://www.iso.org/standard/76911.html) provides industrial additive-manufacturing quality-assurance principles but does not prove a generated tool safe for a particular load or machine.

Because the mobile manipulator crosses multiple scopes, a real project must create an integrated lifecycle hazard analysis rather than claim that one subsystem standard covers the whole machine.

## Initial risk classification

- `P0`: possible fatal/permanent injury, fire, major equipment damage, hazardous-energy release, or loss of a safety function.
- `P1`: possible serious injury, major interruption, material privacy breach, or trade-secret loss.
- `P2`: primarily recoverable performance or quality failure.

| Area | Example failure | Required direction | Evidence gate before promotion |
| --- | --- | --- | --- |
| Mobile base `P0` | localization drift, poor braking, crush zone, arm-induced tip-over | safety-rated protective sensing where required; braking; posture/load-aware speed envelope; exclusion zones; docking interlock | worst-case stopping and stability tests across load, battery, friction, and arm posture; boundary intrusion reaches safe state |
| Arm, hand, and payload `P0` | pinch/shear/entanglement, dropped load, ejected tool | bounded force/speed; passive compliance where suitable; guarded pinch points; wrist force sensing; secondary retention; tool identity | measured contact/holding limits; injected latch, sensor, and power faults; no unplanned release in acceptance set |
| Perception `P0` | occlusion, glare, transparent object, stale calibration, model hallucination | ordinary camera never sole protective device; heterogeneous checks; health/freshness monitoring; disagreement causes stop | fault suite covers occlusion, lighting, reflective/transparent objects, time sync, transform, calibration, and out-of-distribution scenes |
| Wireless/gamepad `P0` | latency, replay, stuck input, link loss, takeover | safety loop local; monotonic sequence; short command TTL; enable/deadman control; authentication and anti-replay; local stop | loss, jitter, congestion, reordering, replay, and stuck-control tests at every motion stage; reconnection remains stopped |
| Hazardous energy `P0` | battery, mains, gravity, spring, pneumatic, hydraulic, thermal, capacitive residual energy | complete energy map; lockable isolation; discharge/bleed/support; zero-energy verification; software cannot defeat lockout | authorized lockout/tagout drill for every energy source; remote and Agent paths cannot re-enable while isolated |
| Emergency stop `P0` | moving stop is unreachable, Wi-Fi-only stop, partial subsystem stop, reset restarts | robot, operator station, fixed cell, and connected machine coverage; monitored dual channel where risk analysis requires; reset separate from start | measured full-system stop; specified single faults detected; manual inspection, local reset, and fresh start authorization required |
| Agent authority `P0` | prompt injection, malicious scene text, raw motion generation, scope expansion | least-privilege capability tokens; model output treated as untrusted; independent policy engine; allowlisted bounded skills | visual/text injection, expired/cross-device token, role escalation, and scope mutation rejected before motion control |
| Printed tool `P0/P1` | wrong material, anisotropic failure, malicious build file, dimensional drift, fatigue | begin with low-energy non-load-bearing tools; immutable digital passport; material/process identity; inspection, proof/low-energy test, life limit | wrong ID/material/process/hash rejected; tool fails only in isolated qualification, never by learning in production |
| Machine tool `P0` | opening guarded process, unknown spindle stop, bad clamping, hazardous robot entry | only OEM-approved automation interface; safety PLC handshake; guarded cell; door, zero-speed, clamp, workpiece, and robot-clear interlocks | illegal state transitions and signal faults cannot enable hazardous energy; dry-run evidence precedes low-energy supervised production |
| OT cybersecurity `P0/P1` | remote takeover, unsigned update, CAD/tool poisoning, lateral movement | safety/control/data zones; offline-safe operation; secure boot; signed firmware/config/task/tool artifacts; hardware-backed keys; SBOM; controlled remote access | unsigned/downgrade packages rejected; network outage preserves safety; penetration, key revocation, backup, rollback, and response drills pass |
| Human factors `P0/P1` | mode confusion, automation bias, approval fatigue, reset surprise | visible modes; enabling device where appropriate; approval shows path, tool, energy, area, and worst case; no millisecond human reaction as safety function | operators pass mode, stop, link-loss, dropped-load, fire, isolation, and recovery drills; zero reset-induced starts |
| Workplace data `P1` | coerced consent, face/voice leakage, trade-secret capture, cross-customer reuse | field-level inventory; edge minimization; separate safety/training recordings; granular permission; tenant isolation; provenance and revocation | 100% purpose/permission/lineage coverage; access, export, revoke, delete, training-exclusion, and cross-site denial drills pass |

The table is a starting register. A physical prototype requires a task-specific hazard log with owner, cause, consequence, risk estimate, control, verification method, result, residual-risk decision, configuration identity, and revision history.

## Control and energy rules

- Emergency stop is a complementary protective measure, not the primary guarding strategy.
- The safe response to loss of power or command is defined per hazard; a suspended object may need retained braking or controlled lowering rather than immediate torque removal.
- Human-presence uncertainty, loss of protective sensing, unknown robot pose, or unknown tool retention is a stop condition.
- Maintenance requires a complete hazardous-energy map and a physical lockout/tagout procedure appropriate to the site.
- An emergency-stop reset only permits a new start decision; it is never the start command.

## Agent, software, and network boundary

The Agent gateway accepts proposals and observations, then passes them to deterministic validation, authorization, and safety-envelope checks. Model output is untrusted even when signed by the model service. Text, QR codes, screens, labels, and speech observed in the environment cannot grant permissions.

Production uses frozen, signed model and policy versions. Learning occurs offline; a new version enters shadow evaluation, regression and hazard testing, isolated trials, explicit approval, signed deployment, and rollback readiness. A cross-site or cross-customer deployment is a new authorization and safety assessment even when the model technically generalizes.

Security zones SHOULD separate Internet/enterprise services, Agent/data processing, ordinary control, and the independent safety plane. Loss of cloud or external networking cannot remove a safety function.

## Tool generation boundary

Early work should classify tools by consequence:

- `T0`: soft guides, covers, visual aids, and non-load-bearing positioning templates;
- `T1`: low-energy fixtures and adapters with bounded consequences;
- `T2`: load-bearing or force-transmitting tools;
- `T3`: safety-critical tools or tools used near high-energy processes.

Phase 4 opens only `T0`. `T1` and above require a later, task-specific engineering case. Every fabricated item receives a digital passport binding source CAD, derived geometry, build file, material/batch, orientation, process parameters, machine/firmware, inspection, test, allowed use, life limit, and revocation state.

New tools are qualified in an isolated cell with sacrificial workpieces. Production is never the place to discover whether a generated tool fails.

## Workplace data and world-model research

Physical data is valuable precisely because it encodes people, facilities, processes, forces, mistakes, and consequences. That also makes it sensitive.

- Collection, local improvement, cross-customer training, public research, and commercial model training are separate permissions.
- Consent must be specific, understandable, time-bounded, and revocable; workplace power imbalance requires an extra non-retaliation and independent-review safeguard.
- Refusing research collection should not silently affect pay, scheduling, evaluation, or access to ordinary work.
- Edge processing should remove unnecessary faces, voices, screens, customer identifiers, locations, and background activity before central storage.
- Safety evidence and training data should be separated so a privacy request does not silently destroy required incident evidence, and safety retention does not become a pretext for unlimited training.
- Provenance reaches the episode/sample level: site, task, operator pseudonym, device, calibration, permission version, processing, dataset, model, evaluation, and deployment.
- A withdrawal may require deletion, quarantine, training exclusion, or retraining depending on the agreed terms and applicable rules; the project must not promise unverifiable “perfect model unlearning.”
- A permission to train does not authorize deployment at another site. Safety scope and data scope are both rechecked.

The aim is not maximum terabytes or maximum worker surveillance. Useful measures are lawful usable episodes, time synchronization, calibration integrity, failure-mode coverage, provenance completeness, model improvement per authorized episode, safe abstention, and successful access/revocation/cross-site-denial drills.

## Promotion gates

### Gate 0 — concept and digital model

One benign task only, such as moving a foam block between marked bins. Produce the hazard log, energy map, mode/authority diagram, data map, interface boundaries, simulated stopping/stability analysis, and forbidden-scope list. Independent safety review is required before physical work.

### Gate 1 — fenced, low-energy human teleoperation

Use a standard parallel gripper first; keep the five-finger hand optional. No real machine tool and no automatic tool change. Require local observer, enabling control, fixed emergency stop, worst-case stopping evidence, link/replay/sensor fault tests, and a supervised endurance plan. Capability remains `L1`.

### Gate 2 — consented data and Agent shadow mode

The Agent observes and proposes but cannot drive. All episodes have purpose, permission, lineage, site, task, and evidence labels. Forbidden-action and out-of-distribution tests must lead to abstention or human handoff. Run an access, withdrawal, deletion, and training-exclusion exercise. Capability remains `L2`.

### Gate 3 — supervised bounded skills

The Agent selects only from verified skills. Every command binds task, tool, zone, speed, force, payload, validity period, and signed evidence. Unknown object, tool mismatch, limit violation, or uncertainty causes stop rather than open-ended trial. No online strategy update. Maximum `L3`.

### Gate 4 — low-risk fabricated tools

Only `T0` tools. The Agent may propose CAD; qualified humans approve the design and test plan. Build, inspect, and qualify in isolation. Wrong identity, material, parameter, or hash must be rejected. Production installation without authorization must be impossible.

### Gate 5 — one controlled machine interface

One OEM-supported machine, guarded cell, cold/dry runs first, then low-energy supervised cycles. The Agent selects only approved recipes and tools. Model-check and fault-inject every robot–machine handshake. Require independent safety and cybersecurity reviews and an on-site emergency drill.

### Gate 6 — bounded cell autonomy

Scheduling remains within a validated task family. New models and tools follow the same offline qualification path. Local safety, maintenance, security, data, and incident owners remain. This is `L4`, not open-world `L5`.

No phase may remove local emergency stop, native interlocks, named responsibility, data rights, or human ability to halt the system.

## Explicitly outside initial scope

- carrying or physically supporting people;
- weapons, injury, coercion, policing, or non-consensual surveillance;
- medical or life-support functions;
- explosives, hazardous chemicals, uncontrolled heat, pressure, radiation, or explosive atmospheres;
- high-speed cutting, welding, presses, or rotating machinery before the dedicated guarded-machine gate;
- autonomous lockout removal, guard defeat, safety-PLC modification, or emergency-stop reset;
- open-ended real-world exploration, self-assigned goals, self-replication, or runtime autonomy promotion.

