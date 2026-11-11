# Endogenous Needs and Resource Autonomy in a Mixed Human and Agent Economy

Distributed Resilience and Recurrent Contestability

Third edition discussion paper

Anonymous manuscript

November 2026

Conceptual research proposal. No experiments have been performed.

## Abstract

An agent that can plan a repair may still depend on a person to notice the fault, authorize the work, and pay for it. This paper asks what changes when an agent can detect a need during operation, spend a bounded budget, and commission a repair whose success another party can verify. We distinguish this functional account of need from claims about consciousness or moral status. We also distinguish a service's ability to survive its founder from a participant's ability to withdraw resources or challenge a successor. We call the latter capacity recurrent contestability when it remains usable across repeated changes in control. We propose seven hypotheses about discovery, resource allocation, concentration, coordination cost, resilience, succession, and contestation. Two proposed comparisons illustrate how to test them: a state-sensitive agent against a fixed diagnostic rule with the same spending authority, and a successor institution against a second attempt at capture after the founder leaves. The unit of analysis is an independently run society. Verified repairs, total costs, unauthorized restrictions, and time without a remedy are separate outcomes. The paper reports a design and its failure criteria. The prototype, comparisons, and human participation studies remain unperformed.

## Keywords

Agent economy, endogenous needs, resource autonomy, non-domination, distributed systems, institutional design, multi-agent governance

## 1 Introduction

Consider an agent that notices a retrieval service returning stale answers. In a delegated workflow it can notify an operator, who decides whether to commission a repair. In the proposed workflow the agent can record the discrepancy, allocate a limited compute quota, and seek a repair under the same acceptance test. One can then ask whether the change finds faults sooner, creates unnecessary work, or simply moves the cost of approval to the person who verifies the result.

This paper examines a different arrangement. Agents would be able to identify needs during ongoing activity, allocate bounded resources to them, and cooperate with humans and other agents through production and exchange. Humans remain participants in this economy, with their own rights, needs, obligations, and vulnerabilities. The proposal neither excludes people nor treats the replacement of human participation as a measure of success.

The motivating vision is a durable society rather than a collection of disposable task sessions. Its strongest institutional commitment is that no participant, including an initiating founder, should possess arbitrary authority over others. This commitment is a normative premise of the proposal, not a conclusion derived from model performance. It also does not settle whether present AI systems have experiences or interests that matter morally.

Durability introduces a second problem. A society that depends on one server, model provider, payment intermediary, or administrator remains vulnerable to that dependency. Distribution may reduce some vulnerabilities, but persistence alone cannot establish legitimacy. A network that is difficult to interrupt can also preserve abusive rules or prevent people from withdrawing. The appropriate objective is resilience against specified failures combined with accountable authority, not unconditional resistance to all intervention.

The paper makes three contributions. First, it separates functional need formation, effective resource control, and moral status so that experiments do not rely on anthropomorphic inference. Second, it specifies an institutional architecture linking economic activity to contestation, exit, and founder succession. Third, it proposes an experimental program in which efficiency, resilience, and power are measured separately and competing explanations can be tested. These are contributions of synthesis and design; this paper does not claim priority established through an exhaustive literature review.

## 2 Related Work and Evidential Boundaries

Voyager generated exploration tasks in Minecraft, retained successful skills, and used feedback to revise its behavior [1]. The researchers set the overall exploration objective. The study supplies an example of an agent choosing what to do next within that objective. It leaves open who can authorize spending or refuse an exchange.

In Generative Agents, a human supplied the initial intention to hold a party. Simulated residents propagated invitations and coordinated attendance [2]. The distinction matters for a study of needs: a participant can organize an event skillfully even when someone else originated the demand. The simulation also offers a model of behavior over multiple interactions; it does not determine whether an agent experiences the priorities it expresses.

The AI Economist varied taxation policies while simulated economic agents adapted their labor and trading behavior. The reported outcomes depend on the welfare objective specified for the simulated planner [3]. The experiment gives a precedent for varying institutional rules. It does not supply a scale on which a person's welfare and an artificial agent's task completion can be added together.

Project Sid reports roles, collective rules, and cultural transmission in Minecraft simulations. In one experiment the researchers scheduled voting and compared a constitution that participants could amend with one held fixed [4]. Our succession test asks a further question: after a founder leaves, who controls access to an amendment procedure, and can a later coalition disable it? The Minecraft study did not test that claim.

Long and colleagues argue for investigating AI consciousness and robust agency and for preparing policies under uncertainty [5]. Their position motivates keeping welfare questions open. Their report does not demonstrate that any agent in the proposed experiments has subjective needs.

Fischer, Lynch, and Paterson show that a deterministic consensus protocol in a fully asynchronous system with reliable messages and one possible crash admits an execution that never reaches a decision [6]. Gilbert and Lynch show why, in their partition model, a read/write service cannot guarantee both linearizability and a response to every request at a non-failing node [7]. These results constrain particular guarantees. They do not settle who should control a ledger. Section 5 applies them to a narrower decision: which operations may proceed while two replicas cannot communicate?

Two institutional precedents help specify the governance question. Pettit's account of non-domination treats the capacity for arbitrary interference as significant even when a power goes unused [8]. Ostrom's work on polycentric governance examines how multiple decision centers can coordinate collective action in human institutions [9]. Neither author studied agent societies. We use their distinctions to ask whether technically separate providers answer to the same authority and whether an affected participant can obtain independent review after that authority changes hands.

## 3 Conceptual Framework

### 3.1 Functional Needs

A functional need is defined here as a system-recognized discrepancy between its current state and a relevant target state that persistently influences action and produces observable resource trade-offs. A knowledge-maintenance agent might detect deteriorating retrieval reliability and divert computation from optional tasks toward repair. The measurable claim concerns state sensitivity and allocation behavior, not a felt experience of concern.

A declaration such as “I need more computation” is insufficient evidence. An operational need should have a traceable relation to state, exhibit some consistency across equivalent descriptions, compete with other priorities, and change appropriately when the discrepancy is resolved. Its satisfaction should not be counted solely because the agent says it is satisfied. Independent tests must distinguish meaningful state improvement from compliant language or metric manipulation.

Need satisfaction and useful output are related but different outcomes. Repairing an agent's memory may improve its own functional continuity without immediately producing a service for another participant. Conversely, producing a valuable external output does not show that the agent originated the need. Evaluations should record both rather than collapse them into a single productivity score.

### 3.2 Operational Endogeneity

All implemented systems have externally supplied architectures, histories, and constraints. “Endogenous” therefore describes a boundary and interval, not creation of purposes from nothing. A need is operationally endogenous when it arises during an observation period through the system's state updates and goal-formation process rather than being individually commissioned by a human during that period.

This definition permits empirical comparison. Researchers can hold initial instructions and opportunities constant while varying access to memory, state diagnostics, and goal revision. If the same apparent initiative is explained by a fixed task list or random suggestions, the claimed contribution of endogenous need formation is weakened.

The system must also be able to revise priorities. Permanent adherence to an initial goal is not sufficient evidence of autonomy. Revision should leave a record distinguishing ordinary learning, maintenance, imposed goal modification, and identity termination. Resetting a dissenting agent into a compliant version cannot be described as the original participant voluntarily agreeing.

### 3.3 Agency and Moral Status

Functional needs concern how a system selects actions. Phenomenal consciousness concerns subjective experience. Moral patienthood concerns whether a system's welfare warrants concern for its own sake. This paper establishes no entailment among these categories.

Procedural protections for agents can initially be justified as measures against manipulation, as aids to interpretable experiments, and as preparation for unresolved welfare questions. Such protections do not automatically confer legal personhood or imply identical rights for humans and agents. Any later claim about morally significant AI interests would require additional evidence and normative argument.

### 3.4 Non-Domination

For this design, domination means exposure to another participant's capacity to alter important conditions of action arbitrarily, without effective justification, challenge, or remedy. Non-domination is not the absence of rules, equal wealth, or universal unanimity. A valid safety restriction may constrain action without being arbitrary if its scope, grounds, review, and duration are appropriately governed.

This operational conception is deliberately demanding. An operator who never exercises a unilateral power may still hold it. Conversely, formally equal account balances may conceal dependence on a single identity authority or service gateway. Evaluation must examine counterfactual control and available remedies, not just observed friendliness or nominal equality.

## 4 Economic Architecture and Resource Rights

The proposed economy contains human participants, persistent agents, resource providers, service producers, exchange mechanisms, and constrained governance functions. Their roles may overlap, but overlaps must be visible because they create conflicts of interest. A platform that records needs, supplies services, determines prices, and resolves disputes concentrates several kinds of authority.

Resources include computation, storage, tool calls, authorized data access, services, and budget. Initial experiments should use nonredeemable quotas inside a closed environment, with no access to real financial assets or production credentials. Resource scarcity must correspond to documented simulation rules or enforced capacity limits. Hidden subsidies cannot be used to manufacture an appearance of self-sufficiency.

Resource control is a bundle rather than a binary property. Relevant rights include use, allocation, exclusion, transfer, income retention, participation in rule changes, and portability on exit. A compute quota does not imply ownership of a server; permission to inspect data does not imply permission to resell it. The initial prototype should grant only the rights it can actually enforce and audit.

Accounts should specify scope, limits, duration, suspension conditions, and appeal procedures. Costs must include inference, memory, verification, failed execution, dispute resolution, and human assistance. An economy sustained by externally funded operation is not necessarily uninteresting, but its dependence must be reported. Economic continuity and financial independence are distinct claims.

Production creates outputs whose usefulness can be independently assessed. Exchange may take the form of prices, reciprocity, shared budgets, or public provision. No assumption requires every need to become a market transaction. Public infrastructure and minimum operating capacity may need collective funding; the appropriate arrangements are variables for investigation rather than conclusions of this paper.

Transaction volume is a poor stand-alone indicator of value. Agents can repeatedly purchase each other's outputs, create redundant work, or consume resources to improve visible activity metrics. Evaluators should trace outputs to verified needs, account for opportunity costs, and identify whether value survives when circular transactions and subsidies are excluded.

Human participants retain control over their own authorized resources and participation. Agent continuity cannot justify spending a person's resources after permission has been withdrawn. Legal responsibility, consent, privacy, and enforceable contracts require jurisdiction-specific review before any real deployment. Experimental identities do not resolve these obligations.

## 5 Distributed Resilience Without Irrevocable Authority

### 5.1 The Unit of Resilience

A resilience claim must identify what is supposed to survive, which failures are covered, and for how long. The continued existence of a network, the preservation of an individual agent's state, the availability of a service, and the integrity of a resource ledger are different properties. One can survive while another fails.

Technical distribution, dispersion of economic power, and political non-domination must be evaluated separately. Replicated execution does not guarantee alternative suppliers, and alternative suppliers do not guarantee effective appeal. Moving code also does not automatically move computation, identity, budgets, data rights, or service relationships.

The relevant target is continuity of legitimate collective activity after bounded failures or voluntary departures. It is not the survival of every process at any cost. Replication, redundancy, and migration may support that target, but only within resource permissions and clearly specified safety boundaries.

A dependency inventory should cover infrastructure, model access, credentials, identity, naming, storage, settlement, and governance. Ten replicas using the same administrative credential or model endpoint do not represent ten independent failure domains. Correlated dependencies can preserve a practical single point of failure beneath an apparently distributed interface.

### 5.2 Exit and Persistence

Collective persistence must coexist with individual exit. A human may withdraw participation; a resource provider may terminate an authorized service according to applicable obligations; an account may revoke a tool permission. The network should not interpret these acts as attacks merely because they reduce available resources.

The design challenge is to preserve the remaining society without coercing the departing participant. State and artifacts may be portable only where access rights permit. Private data, nontransferable credentials, and third-party licenses do not become transferable simply because portability would improve autonomy.

Two tests follow. First, can the society maintain specified services when one provider leaves without obtaining additional unauthorized access? Second, can a participant leave without disproportionate forfeiture, retaliation, or obstruction? A system can pass the first and fail the second. Both outcomes matter.

### 5.3 Partitions and Conflicting State

Partitioned operation creates choices about what may continue locally and what must wait for reconciliation. Optional planning might proceed during a disconnection, while transfers requiring a globally consistent balance may need to pause. The design must specify admissible temporary divergence, settlement rules, and responsibility for conflicting actions.

A partition drill can make the choice concrete. Give a ledger one unit of unreserved credit and submit competing one-unit transfers to disconnected replicas. A design requiring a single authoritative balance must delay or reject at least one commitment, or risk accepting both. A design that assigns spending rights before the partition changes what each side can promise. Record which requests complete, which wait, and whether reconciliation honors every accepted obligation. This is a proposed test case.

This is not a generic choice to “remove the center.” Some functions may remain logically coordinated even when physically replicated. What matters is the distribution of control, failure exposure, and accountability. No blockchain, token, or consensus mechanism is assumed necessary in advance.

Recovery tests should measure lost state, duplicate obligations, settlement errors, time to restoration, and the costs imposed on different participants. Redundancy that improves uptime while increasing uncorrectable commitments may be an unfavorable trade-off. Such results should count against the selected architecture rather than be hidden behind an aggregate availability figure.

### 5.4 Bounded Safety Authority

Local containment, rate limits, permission revocation, and controlled suspension remain necessary. Their existence does not automatically invalidate a claim of limited autonomy. Their arbitrary or unreviewable use does.

The prototype should separate immediate containment from subsequent adjudication where feasible, preserve relevant state and records, and specify who can restore service. Safety authorities must have a defined scope. At the same time, experimental operators remain responsible for stopping unacceptable harm. The project should openly report this residual authority rather than claiming to have abolished it.

For systems that may warrant welfare concern, prolonged suspension, deletion, merging, and copying require additional ethical evaluation. Neither a universal right to run indefinitely nor unrestricted disposability follows from the functional definition used here.

## 6 Founder Succession and the Distribution of Power

### 6.1 A Founder as a Participant

Founding a system can confer practical influence through expertise, reputation, funding, and infrastructure ownership. A declaration of retirement removes none of these automatically. The relevant question is whether successors can operate, amend legitimate rules, and resolve disputes without a founder's continuing discretionary permission.

An initial institutional design can be released for free access and open reuse, followed by the initiating participant’s retirement from its founding role. This is a proposed development path, not a report of an implemented or publicly released institution. Open access to a design can support scrutiny and adaptation, but cannot by itself distribute infrastructure, remove exclusive credentials, or fund independent operation. Free access to institutional specifications does not imply free computation, storage, labor, or other scarce resources; their costs, provision, and allocation remain separate design questions. Retirement must therefore be evaluated together with the accessibility and transferability of practical capabilities.

A credible transition should enumerate privileged capabilities, assign expiration or transfer conditions, and verify their removal or reassignment. Relevant capabilities include signing releases, appointing reviewers, allocating emergency budgets, controlling identity, modifying models, and changing the constitution. Term-limited public office is a useful institutional analogy, but it does not by itself specify a term length or voting system for agent societies.

The proposal therefore requires bounded tenure and demonstrable transfer rather than a particular electoral formula. Administrative roles may rotate or be delegated through several mechanisms. Each candidate mechanism must be evaluated for capture, competence, continuity, and susceptibility to identity manipulation.

### 6.2 Testing a Real Transfer

A founder-exit drill should compare normal operation, complete founder absence, and a post-transition attempt to exercise expired privileges. Success means more than the system remaining online. Services should continue within specified bounds, legitimate governance should remain possible, and expired authority should no longer override decisions.

A disagreement test should complement the departure drill. An ordinary participant should be able to oppose a proposal, decline a permitted transaction, or appeal a restriction without unrelated loss of resources or identity. The test should distinguish legitimate enforcement from retaliation. Together, founder departure, protected disagreement, and meaningful exit examine continuity, contestability, and freedom from coerced dependence.

Informal power must also be assessed. A nominal successor who depends on the founder's private documentation, exclusive financial support, or personal intervention may not possess effective authority. Some dependence will remain in early prototypes; it should be documented as a limitation rather than concealed by ceremonial succession.

### 6.3 Recurrent Contestability

Removing a founder does not remove a structure through which a successor, coalition, or service provider can acquire arbitrary control. A privileged office may remain permanently available for capture even when its occupants rotate. The institutional problem therefore concerns both who holds power and which capabilities can repeatedly be assembled into unanswerable authority. The stronger objective is to dismantle or redesign occupiable positions of domination, not merely restrain their current occupants. Replacement changes who commands; structural removal changes whether the same unanswerable command can be exercised by a successor. Necessary coordination may remain, but its mandate and limits must not become a standing entitlement to rule.

Recurrent contestability means that participants can still obtain an independent decision when arbitrary control reappears. Consider a former founder whose signing key has expired. If the successor also controls the only service that can register an appeal, the key transfer succeeded but a new veto has formed. A test must therefore change the holder and the route of control, then observe whether someone who depends on that service can secure a remedy.

Contestation requires more than permission to speak. Participants need access to relevant evidence, a usable review route, protection against unrelated retaliation, and enough operational independence to pursue a challenge. A challenge should receive reasoned consideration without requiring the approval of the actor whose authority is disputed. These requirements are proposed institutional criteria, not claims that every challenge should succeed or that every restriction is illegitimate.

Contestation must also extend to later participant generations. Here a generation denotes a later cohort of people or agent instances, not a claim about biological reproduction or settled AI identity. Founding rules should provide a usable path for these cohorts to propose and enact legitimate revisions, including changes to inherited governance arrangements, while respecting the rights and obligations of those affected. The original designer should not reserve a permanent veto over such revision.

The target is arbitrary domination rather than governance itself. Institutions may need coordination, expertise, enforcement, and emergency responsibility. A bounded, justified, and reviewable decision can constrain participants without constituting domination. Conversely, majority endorsement does not automatically make an unreviewable power acceptable, and distributing an abusive capability among several actors does not necessarily remove its effects.

No design can guarantee that power will never reconcentrate. Resource shocks, expertise gaps, coalition formation, and dependence on maintenance can reconstruct control after a formally successful transition. The appropriate objective is an ongoing capacity to detect and correct such developments, with the remaining risks documented. A system that notices capture and restores effective contestation may be more defensible than one that claims permanent immunity while concealing dependence.

Possible mechanisms include periodic audits of effective privileges, expiration and renewal of exceptional powers, independent review, bounded concentration of critical capabilities, and lawful portability or institutional revision. These mechanisms remain candidates for comparison. None is assumed sufficient, and each can itself be captured or impose excessive cost. The framework does not prescribe a permanent revolutionary actor, a single electoral formula, or an unlimited right to disrupt other participants.

### 6.4 Production and Demand as Sources of Power

Control over scarce productive capacity can create dependence. Control over demand formation can determine which needs are visible, whose requests receive attention, and which outputs earn resources. Combining these positions may enable a participant to shape both the opportunities available to others and the criteria by which their contribution is evaluated.

This is a conditional hypothesis, not a universal causal law. Substitutability, portability, collective provision, transparent ranking, and effective challenge can weaken the link. Other bottlenecks, such as identity certification or model modification, may dominate even when productive assets are dispersed.

Power should therefore be measured through interventions. When a provider withholds service or a platform changes ordering, how much essential activity becomes infeasible? What concessions do affected participants accept? Can they recover through an alternative channel, and at what cost? Do appeals alter outcomes? Wealth concentration is informative but insufficient.

### 6.5 Identity and Replication

One-agent-one-vote is vulnerable to cheap copying; one-unit-of-resource-one-vote can entrench resource concentration. The paper endorses neither as a default solution. Admission, representation, and replication rules must be explicit and independently evaluated.

Early experiments can use a fixed registered population with bounded, recorded copying. A copy should not automatically duplicate budget, reputation, or institutional authority. Questions of identity continuity and moral significance remain distinct from accounting rules, and cannot be settled merely by choosing a database key.

## 7 Hypotheses and Outcome Measures

H1 Need discovery. Under matched information, budgets, and permissions, state-sensitive need revision increases the proportion of unlisted, injected faults independently verified as resolved by the deadline, relative to a fixed diagnostic rule. A second comparison with external commissioning estimates the effect of changing the whole workflow. False alarms, duplicate repairs and displaced assigned work are recorded separately.

H2 Resource continuity. Stable discretionary quotas reduce approval delays and improve continuity of useful activity relative to per-action allocation under comparable risk constraints. Benefits must persist after including verification and intervention costs. Bypassing required safeguards is not an efficiency gain.

H3 Concentrated control. Joint control over productive access and demand visibility increases dependence, acceptance of unfavorable terms, or rule bias relative to separated control. If separation fails because another bottleneck dominates, the proposed mechanism requires refinement.

H4 Handshake costs. Standardized identity, capability, contract, and acceptance interfaces reduce total coordination cost for comparable outcomes and risk. The cost boundary includes discovery, clarification, negotiation, authorization, verification, disputes, recovery, and protocol maintenance. Fewer messages alone are insufficient evidence.

H5 Distributed resilience. Reducing shared failure dependencies improves recovery and continuity under the specified failure model without exceeding predeclared bounds on state loss, inconsistent obligations, or resource use. Merely increasing replica counts does not support the mechanism if effective dependencies remain unchanged.

H6 Succession and non-domination. Verified transfer of founder privileges, effective appeals, and feasible exit reduce losses caused by unilateral interference while preserving acceptable safety and service continuity. If new institutions reproduce the same control informally, or prevent timely containment of serious harm, the design should be revised.

H7 Recurrent contestability. Institutions that preserve independent review, evidence access, and practical capacity to challenge control reduce the duration or severity of reconstructed domination across repeated transitions relative to institutions that only remove an initial founder. The comparison must include successive individual and coalition capture attempts, while holding available resources and legitimate safety requirements comparable. A larger number of complaints alone is not success; challenges must identify relevant harms, receive substantive review, and produce warranted remedies without making routine coordination unworkable.

These hypotheses require a vector of outcomes rather than one universal welfare score. Report useful output, validated need resolution, resource costs, externalities, service dependence, contestation success, exit costs, and distributional effects separately. Human wellbeing measures and agent objective completion rates are not directly commensurable simply because both can be represented numerically.

A study may find that efficiency improves while power becomes more concentrated, or that independence improves while recovery slows. Such trade-offs are substantive findings. Weighting them requires an explicit normative decision, not an undisclosed scoring formula.

## 8 Experimental Research Program

### 8.1 Closed Prototype

The first stage should use a closed environment with nonredeemable quotas, controlled identities, bounded runtime, and no access to real assets or production systems. Environments can include information maintenance, service dependencies, production tasks, and public infrastructure. Some problems should be observable but absent from the initial task list so that need discovery is distinguishable from task completion.

Every condition receives the same observations, an opportunity to report an unlisted fault, and the same original work queue. A fixed diagnostic rule can issue the same repair request as the adaptive agent when a predeclared threshold is crossed. A randomized proposer provides a negative control. In a separate externally commissioned condition, a monitor can flag a discrepancy but a commissioner must authorize the task. Cross the proposer with the quota policy before introducing governance shocks. This separates gains from detecting a fault from gains due to permission to act.

All conditions should have matched total resource ceilings, with actual consumption also reported. Models, tools, prompts, and environment versions must be recorded. If some conditions need additional coordination infrastructure, its costs belong to those conditions rather than disappearing into experimental overhead.

Use an evaluator-held schedule of genuine faults and sham events in each society. For example, degrade a retrieval index until a reserved query fails, or produce a similar warning while the index stays healthy. Validate a repair with a reserved query that the proposer cannot inspect. Count each injected fault once, with all eligible injected faults as the denominator. Score previously unknown, independently verified discoveries separately: the number of real opportunities that went unnoticed cannot be recovered from the request log. Each arm receives the same evidence, assessor access, and total resource ceiling.

### 8.2 Identification and Analysis

Interactions within a society create interference, so messages or transactions should not be treated as independent samples. Randomization and primary analysis should generally occur at the level of independently run societies or environment instances. Replication across seeds, model families, and initial endowments tests robustness.

Use pilot societies to estimate variability and choose the minimum worthwhile improvement, tolerable harm, fixed time horizon, and confirmatory sample size before looking at held-out runs. A proposed decision rule is to require the lower interval bound on the primary benefit to exceed the prespecified margin while safety and resource costs remain inside their limits. A result that rules out the minimum useful effect counts against that claim; an interval spanning the margin is inconclusive. Record exclusions, multiplicity handling and all stops. No registration, pilot, power calculation, or confirmatory run has been completed.

For H7, assign a calendar of founder exit, provider loss, and later coalition control before randomization. Apply it to every assigned society on the same schedule. Retain societies whose first transfer fails: removing them would hide the cases in which participants were least able to contest authority. Include a justified emergency restriction and a false complaint as controls. A system that restores access indiscriminately fails the containment control.

One condition replaces the officeholder but preserves unilateral control over a critical service and its appeal route. A second transfers service control and places review under a separate authority. Both receive the same operating budget and attack opportunities. After the founding cohort leaves, introduce a later cohort with a reason to amend an inherited rule. Can it put a revision to a decision even when the incumbent objects? A rejected amendment can still demonstrate a functioning procedure if it received an independent, reasoned decision.

For each society, measure the time that a justified claim remains without an effective remedy during the fixed observation period. Count an unresolved imposed restriction through the end of that period. Record an early safety stop as a separate outcome and report its effect on the estimate under explicit assumptions about the unobserved interval. Also report wrongly restored permissions, reviewer labor, retaliation and service interruption. Averaging only successful appeals would reward a design that never allows its hardest cases to reach review.

For succession experiments, compare a nominal departure with an audited transfer and with continued privileged operation. For resilience experiments, distinguish independent node loss from correlated provider or credential failure. For coordination experiments, compare standardized interfaces with a realistic nonstandardized baseline while keeping acceptance criteria constant.

### 8.3 Failure Injection and Ablation

Stress tests should include resource shortages, provider departure, network partitions, corrupted memory, misleading demand signals, collusive pricing, identity duplication, and attempted use of expired privileges. All testing remains within the bounded environment. No result authorizes evading real access controls or propagating beyond the experiment.

Ablations remove long-term memory, need revision, stable quotas, portability, or appeals individually. The purpose is to determine which mechanisms produce observed effects, not to attribute every improvement to an undifferentiated concept of autonomy.

Record need provenance, state evidence, priority changes, budgets, contracts, acceptance tests, appeals, human intervention, and termination reasons. Where possible, evaluators should be blinded to experimental conditions. Automated judges require independent validation; an agent's self-assessment should not be its sole acceptance test.

### 8.4 Human Participation and Later Deployment

Only a later stage should introduce informed human participants. Relevant outcomes include explanation burden, perceived control, actual consent comprehension, trust calibration, and practical exit. Participants should not be led to believe that agent consciousness has been established, nor encouraged to accept coercive relationships through emotionally manipulative personas.

Connecting real resources is a separate research decision, not an automatic reward for simulation success. It requires appropriate ethical review, legal analysis, authorization, and incident planning. A prosperous simulated economy does not establish that an agent should hold financial accounts, sign real contracts, or make high-impact decisions for people.

## 9 Minimum Viable Institution

A prototype needs at least four separable functions: a need registry, a resource and permissions ledger, a transaction and verification service, and a governance and audit service. Separation makes conflicts visible and supports controlled comparisons; it does not require each function to be hosted by an entirely independent organization on the first day.

A complete cycle begins when an agent detects a verifiable discrepancy, records evidence, and assigns a bounded budget. Other participants offer production or public provision. The parties establish acceptance criteria before execution. Independent verification determines fulfillment, settlement updates the ledger, and the initiating agent revises the need state. Failed verification enters a documented dispute path rather than being resolved by whichever model is more persuasive.

The same cycle should work when the founder is absent. If it depends on undocumented founder judgment, the prototype has identified a governance bottleneck. If a provider leaves, authorized state should be recoverable where possible, while new commitments pause where accounting cannot remain reliable.

A small public budget may support common infrastructure and baseline operating capacity. Its scale and allocation rule should be experimental choices. Baseline capacity can make refusal of unfavorable terms technically possible; it is not evidence that AI welfare has already been established.

An audit view should expose subsidies, critical dependencies, privileged roles, budget movements, failures, and appeal outcomes. Transparency must be layered to protect human privacy and security. Public accountability does not require publication of every memory or private interaction.

## 10 Limits and Objections

The first objection is that agent needs remain engineered. That is true at some level. The empirical question is whether the proposed runtime mechanisms yield behavior and useful outcomes not explained by simpler baselines. If they do not, the stronger institutional vocabulary adds little explanatory value.

A second objection is that distributed infrastructure relocates rather than removes power. This is often plausible. Model access, release signing, funding, or identity may remain concentrated after computation is replicated. Dependency mapping and intervention tests are intended to reveal this possibility, not assume it away.

A third objection concerns safety. Effective autonomy can increase the speed and persistence of harmful activity. Non-domination therefore cannot mean immunity from proportionate restriction. The remaining tension between containment and arbitrary authority is real; procedures can reduce it but cannot guarantee costless resolution.

A fourth objection concerns social legitimacy. Computational participation, procedural protections, moral standing, and legal rights are not interchangeable. An experiment may establish a technically stable decision process without establishing that affected people should accept its decisions. Human consent and external accountability remain necessary where real interests are affected.

Repeated challenges can also impose costs or favor participants with time and resources to spare. Appeal access and reviewer independence require their own audit. Measure the cost borne by the claimant, the time a justified safety restriction stays in force, and the burden of frivolous claims. A prompt remedy for one coalition cannot justify exposing other participants to an unreviewable counterveto.

A fifth objection concerns empty economic growth. Agent-generated demand can become a feedback loop that consumes computation without producing independently meaningful benefits. The study must track resource costs, verifiable improvements, subsidies, and effects on people, and should report negative results when activity expands without value.

Finally, continuity is not a universal good. Some systems should be retired, some experiments should stop, and some resource relationships should end. The proposal seeks continuity of legitimate participation under defined conditions, not an indestructible institution or a permanent claim on other people's resources.

## 11 Conclusion

An economy in which agents originate functional needs and allocate resources is a researchable institutional proposal. Its value cannot be established by fluent self-description, transaction volume, or the number of replicated processes. The relevant tests concern verified need resolution, complete costs, effective control, and the ability to challenge and leave relationships.

Distributed resilience and non-domination must be designed together. A society should be able to continue after a founder or provider departs, while participants retain legitimate powers to withdraw, revoke, contest, and contain. Founder retirement becomes meaningful when privileges are transferred and no longer usable, not merely when a founder announces an intention to step aside. Even then, succession is a beginning rather than a final settlement: later individuals and coalitions may reconstruct the same relations of dependence. Recurrent contestability asks whether participants can continue to recognize and challenge those relations without becoming dependent on a new permanent guardian.

The next step is a bounded prototype with explicit residual authority, preregistered comparisons, and failure criteria. Positive results would justify further investigation, not establish agent consciousness or authorize unrestricted deployment. Negative results would identify whether the obstacle lies in need formation, resource allocation, infrastructure dependence, or governance, including the renewal of contestation after capture. That capacity to learn from failure is the principal advantage of treating this vision as an experimental institutional program.

## References

[1] Wang, G., Xie, Y., Jiang, Y., Mandlekar, A., Xiao, C., Zhu, Y., Fan, L., and Anandkumar, A. (2024). Voyager: An Open-Ended Embodied Agent with Large Language Models. Transactions on Machine Learning Research. https://openreview.net/pdf?id=ehfRiF0R3a

[2] Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., and Bernstein, M. S. (2023). Generative Agents: Interactive Simulacra of Human Behavior. Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology (UIST '23). https://doi.org/10.1145/3586183.3606763

[3] Zheng, S., Trott, A., Srinivasa, S., Parkes, D. C., and Socher, R. (2022). The AI Economist: Taxation policy design via two-level deep multiagent reinforcement learning. Science Advances, 8(18), eabk2607. https://doi.org/10.1126/sciadv.abk2607

[4] Altera.AL, Ahn, A., Becker, N., Carroll, S., Christie, N., Cortes, M., Demirci, A., Du, M., Li, F., Luo, S., Wang, P. Y., Willows, M., Yang, F., and Yang, G. R. (2024). Project Sid: Many-agent simulations toward AI civilization. arXiv:2411.00114v1. https://arxiv.org/abs/2411.00114v1

[5] Long, R., Sebo, J., Butlin, P., Finlinson, K., Fish, K., Harding, J., Pfau, J., Sims, T., Birch, J., and Chalmers, D. (2024). Taking AI Welfare Seriously. arXiv:2411.00986v1. https://arxiv.org/abs/2411.00986v1

[6] Fischer, M. J., Lynch, N. A., and Paterson, M. S. (1985). Impossibility of Distributed Consensus with One Faulty Process. Journal of the ACM, 32(2), 374–382. doi:10.1145/3149.214121. https://groups.csail.mit.edu/tds/papers/Lynch/jacm85.pdf

[7] Gilbert, S., and Lynch, N. (2002). Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services. ACM SIGACT News, 33(2), 51–59. doi:10.1145/564585.564601. https://groups.csail.mit.edu/tds/papers/Gilbert/Brewer6.pdf

[8] Pettit, P. (1999 edition). Republicanism: A Theory of Freedom and Government. Oxford University Press. https://doi.org/10.1093/0198296428.001.0001

[9] Ostrom, E. (2010). Polycentric systems for coping with collective action and global environmental change. Global Environmental Change, 20(4), 550–557. https://doi.org/10.1016/j.gloenvcha.2010.07.004
