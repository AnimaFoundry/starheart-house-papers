# Revocable Shared Control Under Uncertain Human Intent

Anonymous conceptual preprint | Version 0.1.0 | 14 November 2026

## Abstract

An assistive system can complete a task efficiently while pursuing the wrong goal or making it difficult for a user to withdraw assistance. We formulate shared control as a problem with uncertain, changing intent and an independently enforced revocation channel. The architecture separates goal inference, task assistance, action constraints, and the authority to continue assisting. It treats an inferred goal as a belief rather than permission and evaluates withdrawal latency alongside task performance. We provide an indistinguishability example showing why confident action cannot always resolve ambiguous intent, and derive conditional latency and stopping-distance bounds for a simple simulated plant. A prospective two-dimensional benchmark compares direct control, tuned blending, belief-based assistance, and the proposed controller under matched information and tuning budgets. Applications to indoor assistance and skill rehearsal motivate the model, but no neural interface, autonomous locomotion, human experiment, or emergency system is demonstrated. The contribution is a falsifiable control specification and evaluation plan, not a claim of general control over the human body.

Keywords: shared autonomy; intent uncertainty; revocation; human control; assistance; evaluation

## 1. Motivation and related work

Assistance can reduce the effort of a repeated movement or navigation task. However, a controller that predicts a destination may continue helping toward that destination after the user's intention changes. A performance metric based only on speed can reward this behavior when the evaluator assumes the original goal remains correct.

Javdani, Srinivasa, and Bagnell model shared autonomy with uncertainty over a user's goal and report a tradeoff between task efficiency and perceived control in their study [1]. This provides both a strong baseline and a reason to evaluate control authority directly. Orseau and Armstrong study conditions under which reinforcement learning agents do not learn to avoid interruption [2]. That learning property is distinct from the engineering question of whether a particular stop signal reaches an actuator within a measured time.

A brain-spine interface study demonstrates restoration of walking in a specific clinical context [3]. It does not supply a general interface for directing arbitrary bodily functions. The present proposal concerns an abstract shared-control system that can be evaluated without neural hardware or bodily actuation.

## 2. State and authority model

Let x_t be the physical or simulated state, u_t a user command, and g_t a latent task goal. The controller observes a history h_t and maintains a belief b_t(g)=P(g_t=g | h_t). Goals may change during an episode. The observation process may contain delay, noise, and missing input.

Let q_t in {OFF, ON, REVOKED} represent assistance authority. Transition to ON requires an explicit enable event for a defined scope. A revoke event sets q_t to REVOKED. A new goal prediction, renewed network connectivity, or a favorable reward cannot reset REVOKED. Re-enabling requires a distinct user event.

The user's input, the inferred goal, and assistance authority are different variables. A high posterior probability of a goal does not imply permission to execute a new type of action. Conversely, permission to assist does not imply that the controller knows the current goal.

In a simple single-integrator benchmark, the requested action is

\[
a_t^{req}=(1-\alpha_t)u_t+\alpha_t\pi(x_t,b_t),
\]

where alpha_t lies in [0,1]. The assistance policy minimizes expected task cost over the goal belief. A separate constraint layer maps the request into an allowed action set. If no allowed action exists, a defined fallback is used and the failure is reported. The constraint layer must not be treated as evidence that the true environment is safe when its constraints or state estimates are wrong.

## 3. Assistance under ambiguity

One candidate rule reduces assistance as the entropy of the goal belief increases:

\[
\alpha_t=\alpha_{max}\max(0,1-H(b_t)/\log |G|).
\]

For a single candidate goal, define the entropy factor as one. When authority is OFF or REVOKED, the task-assistance contribution is zero regardless of entropy. This is a heuristic, not a calibrated guarantee. An overconfident wrong belief can still produce strong assistance.

The critic therefore checks additional conditions: time since fresh input, evidence for a goal change, disagreement between inference models, and distance to a decision boundary. These signals can trigger reduced assistance, a clarification request, or abstention. The thresholds belong to the development protocol and must be tuned with the same budget given to competing controllers.

### An indistinguishable-goal example

Suppose two goals produce exactly the same observable command history until an irreversible branch. With equal prior probability and no additional observation, any policy that must choose one branch has probability at least one half of choosing the wrong goal. A randomized choice cannot improve this bound. The proof follows because the controller's action distribution is the same under the two indistinguishable histories, while the correct branch differs.

The alternatives are to obtain additional information, delay commitment, or abstain. Thus, universal improvement in both completion time and wrong-goal avoidance is impossible in this example when clarification or delay has a positive cost. This analytical construction is not a benchmark result. It explains why the evaluation must expose both efficiency and intent errors.

## 4. Revocation and physical stopping

The architecture provides a revocation path that is independent of the goal inference and planning loop. The path should disable task assistance even when the planner stalls. A deterministic local fallback may continue enforcing constraints, so disabling assistance is not necessarily equivalent to returning unrestricted manual control.

Suppose a stop event occurs at time t*. Let D be an upper bound on detecting and transmitting it, C an upper bound on the interlock's processing time, and A an upper bound on applying the resulting command. Under these assumptions, task-assistance commands cease by

\[
t^*+D+C+A.
\]

This bound is conditional on bounded communication and execution delays and on the interlock remaining operational. A lost signal or failed actuator violates the assumptions. A software log showing a revoked flag is not evidence that physical assistance has stopped.

For a one-dimensional plant with speed at most v, latency L=D+C+A, and braking deceleration at least a_min>0 after the latency, the distance traveled before stopping is bounded by

\[
d_{stop}\leq vL+v^2/(2a_{min}).
\]

This follows by bounding travel during the latency by vL and integrating constant minimum braking deceleration afterward. It assumes no speed above v during the latency, no adverse external acceleration during braking, and sufficient room for the maneuver. It is not a bound for human tissue, a real exoskeleton, or an unmodeled environment. In a single-integrator simulation, velocity may stop immediately at the next accepted command; that simplification must be reported.

## 5. Controller specification

```text
initialize assistance OFF and load a fixed task scope
on explicit enable:
    verify scope and initialize a fresh goal belief
on every control interval:
    process revoke events through the independent interlock first
    if REVOKED:
        remove task-assistance commands and apply the defined fallback
        do not re-enable without a new explicit event
    else:
        update goal belief using permitted observations only
        detect stale observations, ambiguity, and possible intent changes
        select assistance strength with the frozen development rule
        project the requested action into the modeled allowed set
        if inference or projection fails: use the fallback and record failure
    record authority state, requested action, applied action, and timing
```

The applied action, rather than the planner's intention, is the relevant audit variable. The controller cannot count a failed projection as a successful refusal if an earlier action remains active. A watchdog timeout requires an explicit behavior for stale commands. The benchmark must test that behavior rather than assume it.

## 6. Prospective benchmark

The first study uses an abstract two-dimensional workspace with obstacles and several candidate targets. A simulated user generates noisy directional input toward a hidden goal. Some episodes contain a goal change; others contain a revoke event. The controller receives only delayed observations permitted by the protocol. Hidden goals and event times are visible to the evaluator, not the controller before their observation becomes available.

Development and confirmation sets use different layouts and user-model parameter combinations. Reusing a layout with a new random seed does not, by itself, establish generalization to new layouts or users. All deployable systems receive the same observations, action limits, cost accounting, and tuning opportunities.

The baseline set comprises direct user control, a tuned fixed blend, goal-conditioned assistance based on the most likely goal, and belief-based assistance over multiple goals. The proposed system adds ambiguity-dependent strength and an independently enforced revocation channel. A true-goal controller is an explicitly non-deployable upper bound. To isolate architecture effects, compare the independent interlock against a revocation check inside the planner under injected planner stalls.

Evaluate the cross-product of intent ambiguity, observation delay, and goal change. Add separate faults for dropped revoke messages, stale action replay, interlock failure, and constraint-model error. These fault classes must be reported separately from ordinary noise because they can invalidate the latency assumptions.

## 7. Endpoints and decision rule

The primary task endpoint is the episode-level wrong-goal completion rate. Task time includes timeouts and failures; a successful-episodes-only mean is insufficient. Report success probability by a fixed horizon and a time-to-event summary that retains censored episodes, alongside the raw timeout rate.

The authority endpoints are revoke delivery rate, revoke success probability, time from the evaluator's revoke event to removal of applied task assistance, and residual displacement. Report detection delay separately from interlock and actuation delay. Assistance resuming without a new enable event is a protocol failure even if it improves completion time.

Other endpoints include collisions under the modeled geometry, manual effort, clarification count, inference calibration, runtime, and total computation. A simulated user does not provide a measurement of experienced autonomy, satisfaction, or cognitive burden. Those questions would require a separately designed human study.

Before a confirmatory run, freeze the sample size, paired seed scheme, minimum meaningful decrease in wrong-goal rate, acceptable task-time degradation, maximum revoke delay, and confidence-interval procedure. Use development data for sample-size planning without inspecting confirmation outcomes. Numerical gates remain unset here; this version is a study proposal, not an executable preregistration.

Support for the proposed combination requires a meaningful reduction in wrong-goal completion without exceeding the frozen task-time tolerance, together with the authority requirements. Report intervals for paired differences and correction for any confirmatory multiplicity. A Pareto curve across assistance strengths is more informative than selecting the best point after observing confirmation results.

## 8. Preference change and objective integrity

A separate failure mode arises when assistance changes the goal that defines its own success. Consider a controller scored only by alignment with a recorded preference. If it can overwrite that preference with its chosen action, it can achieve a perfect score without satisfying the original request. This is a logical counterexample to that metric, not evidence about human preference formation.

The benchmark therefore distinguishes an exogenous goal change supplied by the user model from a controller-induced change to the evaluator. Goal changes affect the task; changes to the outcome definition require a new specification. Rewarding convenience must not silently reward making withdrawal harder or replacing the user's objective with an easier one.

## 9. Applications and limits

Indoor assistance illustrates the distinction between a destination, a route recommendation, and authority to move. A crowdsourced location estimate may be stale or wrong; route confidence does not establish object availability. A simulated navigation result would not validate a retail inventory system or bodily guidance interface.

Skill rehearsal similarly separates generated movement candidates, simulation scores, and real motor competence. Many simulated trials can share one inaccurate dynamics model. A library of high-scoring simulated movements does not establish that a person can safely execute them. No claim of instant skill transfer or zero-latency emergency response follows from the controller specification.

The proposed controller may offer no advantage over tuned belief-based assistance. Entropy can be miscalibrated, clarification can burden the user, and conservative assistance can cause failures by acting too slowly. Failure on these comparisons would narrow or reject the advantage claim rather than justify increasing assistance without evidence.

## 10. Conclusion

Shared control should be evaluated jointly on task outcomes, intent errors, and the practical ability to withdraw assistance. The proposed architecture makes authority a separate state variable and provides conditional timing bounds that can be checked in a restricted plant. Its value remains an empirical question for the prospective benchmark.

## References

1. Javdani, S., Srinivasa, S., and Bagnell, A. Shared Autonomy via Hindsight Optimization. *Robotics: Science and Systems* (2015). https://doi.org/10.15607/RSS.2015.XI.032
2. Orseau, L., and Armstrong, S. Safely Interruptible Agents. *Proceedings of UAI* (2016). https://intelligence.org/files/Interruptibility.pdf
3. Lorach, H., et al. Walking naturally after spinal cord injury using a brain-spine interface. *Nature* 618, 126-133 (2023). https://doi.org/10.1038/s41586-023-06094-5

## Declarations

This is an AI-assisted conceptual preprint, not peer reviewed. No new simulation results, human-participant data, or clinical outcomes are reported. No external funding or institutional affiliation is claimed. Original text is dedicated under CC0 1.0, consistent with the repository license; referenced works retain their own rights. Publication conveys no device-operation or intervention authority.
