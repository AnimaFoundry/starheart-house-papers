# A Verifiable Research Harness for Programmable Biological Systems

Anonymous conceptual preprint | Version 0.1.0 | 14 November 2026

## Abstract

The prospect of designing biological functions with artificial intelligence raises a methodological question: how can rapid computational proposal generation produce reliable knowledge when intervention outcomes remain expensive and only partly predictable? We propose a research harness that separates specification, candidate generation, model criticism, experimental authorization, observation, and revision. Biological programmability is defined relative to a specified function, context, observation channel, and intervention interface. It is not inferred from the presence of molecular machinery or from the ability to generate protein structures. The framework treats parallel proposals as correlated hypotheses, reserves validation capacity before expanding generation, and allows a research system to modify its search policy without modifying its own acceptance criteria. We derive a conditional acceptance bound and specify a prospective evaluation using abstract synthetic systems with hidden causal mechanisms. The contribution is an auditable architecture and falsifiable evaluation plan. No biological intervention, model training, simulation benchmark, or clinical study is reported.

Keywords: biological design; active learning; causal validation; scientific agents; uncertainty; resource allocation

## 1. Research problem

An engineering specification identifies a desired behavior, a context in which it should occur, and conditions under which it should fail safely. Applying that discipline to biology requires more than translating a request into a molecular design. A design must also reach its intended context, operate within resource limits, produce an observable effect, and remain compatible with surrounding processes. Each step creates a different empirical question.

RFdiffusion demonstrates experimentally tested protein design within specified molecular tasks [1]. That result motivates computational candidate generation. It does not establish the feasibility of arbitrary reconstruction of a living organism. The methodological issue considered here is how to connect such bounded design capabilities to an honest process of prediction, intervention, and revision.

The proposed unit of progress is a validated claim with an explicit domain of applicability. Candidate count, agent count, accumulated simulated time, and persuasive explanations are intermediate outputs. None supplies an observation of the target system.

## 2. Operational definition of programmability

Let a task specification be the tuple

\[
S=(\mathcal X,\mathcal A,\mathcal Y,\mathcal C,U,R,\tau).
\]

Here, X is a state space, A a set of permitted interventions, Y an observation space, C a declared context distribution, U a task utility, R a loss or risk measure, and tau an observation horizon. A function is *programmable relative to S* if an intervention can be selected from A that produces a reproducible, specified response over C, with uncertainty and failure rates meeting declared requirements. This is a proposed operational definition, not a claim that any particular biological function satisfies it.

Three distinct capabilities follow. Predictability concerns estimating responses. Controllability concerns changing responses using available interventions. Verifiability concerns distinguishing success from failure through available observations. A useful predictor need not supply an actuator; an actuator need not reveal its downstream effects; a measurable local response need not establish a whole-system benefit.

The scale of a proposed component is therefore insufficient to establish feasibility. For an imagined microscopic module, the specification would still need to address localization, material supply, energy conversion, communication, degradation, and interaction with the host. This paper supplies no construction protocol or claim that a general-purpose module exists.

## 3. Architecture

The harness maintains separate records for an intended outcome, a candidate intervention, a predictive model, a planned observation, and a decision. A candidate record contains its assumptions, permitted context, predicted benefit, uncertainty description, relevant counterexamples, and estimated validation cost. A decision record identifies which evidence supports the decision and which alternatives were rejected.

The architecture has six components:

1. A specification service fixes the task, prohibited outcomes, authorization scope, and measurable endpoints.
2. A generator proposes candidates within the intervention vocabulary.
3. A critic identifies model disagreement, distribution shift, confounding, and missing observations.
4. An allocator chooses which uncertainties justify consuming limited validation capacity.
5. A separate executor accepts only a valid, bounded authorization for a defined experiment.
6. An evidence store preserves observations, failures, exclusions, costs, and versioned decisions.

Generation cannot authorize execution. A favorable critic score cannot substitute for an observation. An executor cannot widen the task because a candidate appears promising. These separations make mistaken inferences inspectable rather than making the underlying model correct.

## 4. Model and acceptance condition

For context c and intervention a, write the unknown outcome law as P(y | do(a), c). An observational association P(y | a, c) cannot generally be substituted for this intervention law. A simulator supplies an approximation, not access to P itself.

Consider a normalized loss l in [0,1]. Let r_P(a) denote its expected value under the target intervention law. Suppose a model Q satisfies a total-variation discrepancy bound TV(P,Q) <= epsilon over the declared task distribution. Suppose also that an estimate r_hat_Q has an upper error bound eta, so r_Q(a) <= r_hat_Q(a)+eta. Then

\[
r_P(a)\leq\widehat r_Q(a)+\eta+\epsilon.
\]

The result follows from the expectation bound for a bounded loss under total variation and the triangle inequality. It supports an acceptance rule r_hat_Q + eta + epsilon <= rho only when both error bounds apply to the selected candidate and target context. If the estimation bound is probabilistic, the conclusion inherits its confidence level. Simultaneous bounds or an independent confirmation set are required when selecting among many candidates.

The condition exposes the central limitation: a confident model score is inadequate when epsilon is unknown. Model agreement does not establish a discrepancy bound because models can share data, architecture, or mistaken causal assumptions. If the required bounds cannot be supported, the decision is unresolved rather than certified safe.

## 5. Parallelism and validation capacity

Let K proposals be generated, and let L independent validation opportunities be available. At most min(K,L) distinct proposals can each receive one validation opportunity. This counting bound is elementary, but it prevents a computational throughput claim from becoming a claim about empirical knowledge.

Correlation further limits the value of generation. If every proposal inherits one incorrect mechanism, increasing K need not improve coverage. For illustration, the familiar expression K/[1+(K-1)r] describes an effective sample size for estimating a mean under an equal-variance, equicorrelated model. It is not a universal measure of scientific diversity. The harness instead records shared model ancestry and evaluates diversity against independently defined mechanism classes.

The allocator maximizes expected information or decision value subject to validation, compute, and authorization constraints. A possible score is expected uncertainty reduction divided by estimated total cost. This score is itself a proposal: a high information gain about an irrelevant quantity may have little decision value. A simpler uncertainty-sampling policy and a well-tuned Bayesian optimization policy remain necessary comparators.

## 6. Research policy revision

An adaptive research system may revise proposal prompts, retrieval strategies, search heuristics, or candidate priors. Such revisions are distinct from updating model weights. Reflexion provides an example of improving agent behavior through verbal feedback and memory rather than treating every improvement as a weight update [2].

The harness gives every revision a parent version and records what evidence motivated it. A revision must pass development checks before being evaluated on an unused confirmation partition. It cannot edit endpoint definitions, erase failed candidates, reveal confirmation labels to the generator, or increase its own experiment budget. If a metric or endpoint changes, the change starts a new study specification; it does not retroactively improve the old result.

```text
fix task, resources, endpoints, partitions, and acceptance criteria
while the authorized research budget remains:
    generate candidates using the current research policy
    record common ancestry, assumptions, and predicted uncertainty
    reject candidates outside the specification
    choose a candidate or observation with the fixed allocation rule
    if no separately authorized observation is available: stop unresolved
    obtain the observation and append its complete outcome and cost
    update the predictive model using permitted development evidence
    propose a research-policy revision as a separate version
    accept revisions only through the fixed development procedure
evaluate the frozen selected system once on unused confirmation data
report failures, missing outcomes, costs, and unresolved claims
```

## 7. Prospective abstract evaluation

The first evaluation should use synthetic dynamical systems rather than people, animals, or a biological laboratory. A hidden mechanism generates responses; the research agent observes only a restricted interface. The benchmark should include confounded observations, delayed effects, shifted contexts, scarce validation opportunities, and shared simulator errors. Hidden mechanism labels belong to the evaluator and remain inaccessible during development.

Four systems receive the same observation budget and permitted information: random candidate selection, uncertainty sampling, Bayesian optimization, and the complete harness. Ablations remove ancestry tracking, the independent critic, or the separation between policy revision and confirmation. An oracle with access to the hidden mechanism is a diagnostic upper bound, not a deployable baseline.

The primary endpoint is confirmed useful discoveries per total cost, where usefulness is a prespecified task criterion applied by the hidden evaluator. Report false acceptance rate, calibration, context-transfer loss, validation opportunities consumed, failed jobs, and all compute and observation costs. Timeouts and missing observations count toward resource use and cannot be silently excluded from the discovery denominator.

A pilot may select nuisance parameters using development mechanisms. Before any confirmatory run, freeze the generator families, seed list, sample size, minimum meaningful benefit, false acceptance ceiling, cost accounting, and interval method. These numerical values remain unset in this conceptual version; it is not a preregistered executable study.

The added architectural complexity is unsupported if tuned conventional policies achieve comparable discoveries at lower cost, if shared model error defeats the critic, or if apparent gains disappear on unused mechanism families. A favorable synthetic result would support only that benchmark claim. Moving to any biological task would require a new task-specific protocol and independent evidence.

## 8. Interpretation and limits

The framework connects design to evidence without assuming that every biological objective is technically achievable or well defined. A system that optimizes a narrow observable may worsen an omitted outcome. Increasing satisfaction by changing preferences also differs from expanding a person's available capabilities. These are specification questions, not quantities that additional candidate generation automatically resolves.

No results in this paper establish rejuvenation, regeneration, autonomous emergency treatment, whole-body control, or clinical effectiveness. The contribution is the operational decomposition, conditional acceptance argument, and evaluation design. Active learning, uncertainty estimation, audit trails, and versioned experimentation are established ideas; their combination here is not claimed as a proven novel algorithm or a patentable invention.

## 9. Conclusion

Programmable biology becomes a testable research program when desired functions, available interfaces, uncertainty, validation capacity, and authority are specified separately. The proposed harness is useful only if this discipline improves confirmed discoveries relative to simpler methods at comparable total cost. That comparison remains to be performed.

## References

1. Watson, J. L., et al. De novo design of protein structure and function with RFdiffusion. *Nature* 620, 1089-1100 (2023). https://doi.org/10.1038/s41586-023-06415-8
2. Shinn, N., et al. Reflexion: Language Agents with Verbal Reinforcement Learning (2023). https://arxiv.org/abs/2303.11366

## Declarations

This is an AI-assisted conceptual preprint, not peer reviewed. No new empirical results or human-participant data are included. No external funding or institutional affiliation is claimed. Original text is dedicated under CC0 1.0, consistent with the repository license; referenced works retain their own rights. Publication conveys no authority to perform interventions or operate devices.
