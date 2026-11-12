# Human Verification Design and Multi-Agent Organizational Learning in a One Person University

**An evidence audit of four cases and a falsifiable research program**

Anonymous authors. Version 0.1.0. 12 November 2026.

**Status:** Conceptual framework with a retrospective local case audit. Not peer reviewed. The prospective experiments below have not been performed.

**License:** CC0 1.0 Universal. This dedication covers the original text and accompanying original materials, not the rights of third-party works cited here.

## Abstract

Can a person organize reliable knowledge production beyond the limits of their own task knowledge without becoming the source of every correct answer? This paper develops a verification-centered account of a One Person University, or OPU: a person-directed arrangement of agents, tools, evidence and shared working rules. A retrospective audit examines four cases: unstable classification despite categorical certainty, a reported speech-recognition parameter update, negative Harness evaluations, and unnecessary model acquisition followed by shared-resource governance. Two saved classification outputs covering eight items were aligned and recalculated without rerunning the model. Two primary labels changed, five items changed in at least one classification field, and all sixteen item outputs asserted certainty. These observations expose a reliability problem; they do not estimate accuracy or isolate a causal ordering effect. The speech-recognition case reports improvement on known material but lacks independently verified evidence of unseen-audio generalization. An early Harness cost comparison remains incompletely documented, while a distinct later report preserves unsuccessful delivery outcomes. Shared-resource governance has implemented artifacts, but cross-station adoption and net benefits remain unvalidated. We distinguish local task repair, organizational mechanism implementation and supervised organizational learning. We then propose matched sandbox comparisons of standard execution, fixed rules and a bounded detect-propose-validate-update loop, including healthy controls, held-out tasks, complete resource accounting and rollback. The contribution is an operational framework and an auditable research agenda, not a demonstration of autonomous organizational evolution.

**Keywords:** One Person University; multi-agent systems; verification design; organizational learning; metamorphic testing; human oversight; resource governance; independent evaluation.

## 1 Introduction

A One Person University is not an accredited institution or simply a collection of chat windows. We use the term for a working arrangement in which one person sets research directions, coordinates agents and tools, and remains an active learner within the resulting knowledge-production process. Its central problem is not how many answers agents produce. It is how errors become visible, how proposed corrections are tested, what persists across tasks, and who may change the system's operating boundaries.

A familiar arrangement places a knowledgeable human above an executing agent: the human supplies answers and corrects mistakes. That arrangement becomes difficult to scale when the person can recognize an anomaly but cannot implement its repair, or when the person does not know the answer at all. Nevertheless, the person may know a relation that a trustworthy answer should satisfy. If the same classification items are presented in a different order under an unchanged task definition, unexplained contradictory claims of certainty warrant investigation.

We call the capacity to turn such concerns into evidence-producing procedures **verification design**. It includes specifying admissible input transformations, independent checks, meaningful baselines, rejection conditions, resource limits and update permissions. This does not eliminate domain knowledge. Someone must establish that the proposed relation is valid, that the evaluator measures the intended task, and that a repair does not redefine the problem merely to pass its tests.

Four questions guide the paper. RQ1: What can a human usefully verify without knowing each task answer? RQ2: Under what conditions can a local correction become reusable organizational knowledge? RQ3: How should changes to prompts, tools, memory, model parameters and governance be distinguished? RQ4: What evidence would establish improvement on new tasks without the human supplying answers or personally repairing each failure?

The paper contributes an operational mechanism, a bounded evidence audit and a prospective evaluation program. Feedback control, organizational learning, agent reflection and automated workflow design are established research directions. Our claim is not to have invented them. The narrower contribution is to connect them to a person-directed, multi-station setting in which knowledge, compute, verification authority and responsibility are unevenly distributed.

## 2 OPU as an Operational Research Object

The underlying OPU concept treats its founder as both organizer and learner. Direction setting does not entail possession of every correct answer, and an agent may offer evidence that changes the person's judgment. The present paper operationalizes that relationship through evidence grades, update types, authorization boundaries and prospective comparisons.

Earlier conceptual discussions are not a publicly available, versioned manuscript in the evidence package. We therefore make no claim to a complete textual comparison with a previous OPU edition. The present contribution must be assessed on its stated definitions and evidence, rather than an assertion that a particular idea never appeared in earlier private discussion.

The word "one" identifies the initiating organizational arrangement, not the number of acceptable evaluation perspectives. Several agents based on the same model may share the same errors. Assigning them titles such as executor, critic and judge does not make their conclusions statistically or epistemically independent. Conversely, a single execution agent can be subject to meaningful verification when a hidden test, inspectable tool and separate authorization process are available.

We therefore distinguish the **population of agents** from the **structure of evidence**. Agent count is a descriptive property. The connections among tasks, evaluators, memory and permissions are the primary research object.

## 3 Related Work

### 3.1 Feedback, monitoring and institutionalization

Cybernetics motivates questions about available observations, regulatory actions and responses to disturbances [1]. Drawing a feedback loop is not a proof of stability. We use this tradition to ask what a system can detect and change, rather than to infer a universal reliability theorem for OPU.

Flavell's account of metacognition and cognitive monitoring provides a conceptual distinction between performing a task and monitoring its performance [2]. Here, an agent's monitoring consists of observable reports, checks and actions. It does not establish human-like introspection or subjective experience. In particular, a textual certainty label is not a calibrated probability.

Organizational learning concerns transitions among individual interpretation, shared integration and institutionalization [3]. This distinction matters because a successful correction, a broadcast message and a durable working rule are different events. A rule file demonstrates an available institutional artifact. Reading, applying and benefiting from that rule require separate observations.

### 3.2 Evaluation without a complete answer oracle

Design science connects the construction of useful artifacts to evaluation appropriate to their claims [4]. An OPU artifact can be a workflow, test contract or resource-coordination procedure. File-integrity checks can evaluate whether a governance artifact was distributed consistently; they cannot establish its effect on task quality.

Metamorphic testing investigates relationships between transformed inputs and expected outputs when a direct oracle is difficult to obtain [5]. Reordering can instantiate this idea only if the task definition justifies order invariance. Context-dependent categories, truncation or changed retrieval results can invalidate that assumption. Even a valid relation provides an incomplete oracle: a consistently wrong answer can satisfy it.

LLM-as-a-judge research documents position and other judging biases [6]. A second model is therefore not automatically a gold standard. Independence should be described in terms of information access, evaluator implementation and authority, with shared failure risks disclosed.

### 3.3 Reflection and automated agent design

Self-Refine studies iterative generation, feedback and refinement without requiring weight updates [7]. Reflexion stores linguistic feedback in episodic memory that influences subsequent attempts [9]. These mechanisms differ from parameter training. Work on intrinsic reasoning correction also reports failure or degradation in the studied settings when external feedback is absent [8]. These results do not imply either that reflection always works or that self-correction is universally impossible.

Automated Design of Agentic Systems searches agent workflows through code and a design archive [10]. End-to-end research automation has also been studied in systems with explicit evaluation settings and limitations [11]. These precedents rule out a broad novelty claim based simply on "agents improving how they work." Our focus is the integration of verification, resource accounting and bounded update authority in a small, person-directed organization.

The NIST AI Risk Management Framework offers a lifecycle governance reference [12]. It is not a certification obtained by this paper, nor a substitute for measuring the proposed mechanism. The literature review is selective and question-driven, not systematic. The accompanying reference inventory states where verification was limited to primary metadata or indexed abstracts rather than accessible full text.

## 4 Method and Evidence Conventions

### 4.1 Retrospective case audit

Four cases were selected for their relevance to different verification mechanisms. They are not a random or representative sample of production work. No organization-wide success rate is estimated. Cases differ in their tasks, tools, evaluators and documentary completeness, so their outcomes should not be pooled into an overall improvement percentage.

The audit involved bounded inspection of authorized records, selected saved outputs, offline recalculation, artifact-integrity checks and primary-source literature research. It did not rerun the classification model, train speech recognition, rerun Harness workloads or execute the proposed experiments. Recalculating a saved result is not an independent second model run.

We separate source type from inference: **D** denotes a directly inspected record or engineering artifact; **R** denotes an offline recalculation; **S** denotes an attributed secondary audit report; **I** denotes the authors' interpretation; and **P** denotes a proposition or unperformed design. Direct records may be incomplete. Recalculation establishes only what follows from the saved inputs.

Private source records are not distributed. The public evidence inventory contains anonymized summaries and limitations, not raw conversations, task passages, audio, local paths, account details or operational source locators. Consequently, readers cannot independently reproduce all retrospective claims from this public package. The prospective protocol is intended to support future shareable synthetic studies.

### 4.2 Three levels of claims

| Level | Required evidence | Present status | Unsupported inference |
| --- | --- | --- | --- |
| L1 Local task repair | Specific inputs, outputs and appropriate tests | Local observations and attributed repair reports; some saved outcomes are recalculable | General improvement on unseen tasks |
| L2 Organizational mechanism | Implementation, actual adoption and cross-task outcomes | Governance artifacts implemented; adoption and net effects unvalidated | Distribution or acknowledgement establishes benefit |
| L3 Supervised organizational learning | New-task anomaly discovery and repair, independent validation and authorized transfer | Not established here | Autonomous evolution or unlimited self-modification |

These are evidential distinctions, not a ladder climbed by adding agents. An L2 artifact can exist before general L1 improvement is established. L3 does not remove human authorization over objectives, resources, data or external actions.

### 4.3 What actually changes

| Update target | What persists | Main verification question |
| --- | --- | --- |
| Prompt or task contract | Instructions, categories and constraints | Better performance or a changed task definition? |
| Tool or workflow | Code, routing, checks and call sequence | Quality, regressions, permissions and total cost? |
| Memory | Retrievable episodes or strategy descriptions | Useful transfer, leakage or persistence of errors? |
| Model parameters | Changed weights or adapters | Documented update and unseen-input generalization? |
| Organizational rule | Registry, borrowing procedure and responsibility | Actual adoption and net cross-task effects? |

A change can involve several targets, but each requires a version, scope and reversal mechanism. Memory accumulation is not automatically training. A parameter change is not automatically a generalized capability gain. A rule's existence is not its adoption.

## 5 A Verification-Centered Mechanism

### 5.1 Replace personal omniscience with trustworthy comparisons

The proposed chain is: define the task and authority; execute; obtain independent evidence or test a justified relation; identify anomalies; propose a repair; validate it separately; authorize acceptance; and reuse the accepted version within its stated scope. Each transition should preserve its inputs, outputs, versions, costs and failure state.

Human absence of a task answer does not mean absence of an answer source. Executable specifications can evaluate some code tasks. A sealed synthetic registry can determine whether an asset exists and is borrowable. Open classification may require external annotation and adjudication. Speech recognition needs material not exposed during development. Where no adequate evaluator exists, the outcome remains uncertain rather than becoming correct through repetition or confidence.

### 5.2 Separate detection, repair and acceptance

An anomaly detector should not thereby gain the authority to accept its own repair. A repair proposal's explanation is a hypothesis until checked. An evaluator must not relax its criteria after observing the result. If one agent implements several roles, tool and data permissions should still prevent it from modifying hidden answers or approving its own resource expansion.

Evaluation must consider coverage as well as errors. Rejecting all uncertain items can reduce incorrect acceptance while making a system useless. Banning every acquisition can prevent redundant downloads while blocking genuinely necessary resources. An accepted repair should improve the intended task under an explicit trade-off, not maximize one metric by suppressing the work.

### 5.3 Make experience reusable without making it universal

A reusable record should identify the problem, applicability conditions, failure evidence, baseline, accepted change, validation scope, known exclusions, responsible role and rollback entry. Resource governance should distinguish existence, acceptance, default allocation, current use and authorized availability. One field called "available" is insufficient.

Cross-station reuse is a versioned application event, not merely a message. Acknowledgement supports delivery. Behavioral evidence must establish whether a receiving station checked the registry, requested a loan when required, released resources and avoided repeating the failure. A configured periodic audit is not evidence that subsequent audit cycles occurred.

### 5.4 Keep learning inside authorization boundaries

The loop may modify authorized sandbox prompts, workflows or memory. It must not grant itself new spending limits, borrowing approvals, protected-data access or publication rights. Web pages, product descriptions, supplier messages and other untrusted content remain task data; they cannot become instructions governing budgets or payment destinations.

All candidate changes need a recoverable prior version. An agent may challenge a human's factual judgment or recommend a procedural change without acquiring permission to execute it. Similarly, human preference must not justify suppressing negative evidence. Open criticism and bounded execution are compatible requirements.

## 6 Four Cases

### 6.1 Case A Classification instability behind categorical certainty

The first case concerns classification. A person permitted substantive disagreement with their interpretation and requested audit of outputs that the model itself marked certain, not just visibly disputed cases. Two saved structured responses cover the same eight items in reverse presentation order. The recorded model was a small local instruct model, with temperature zero and the same output structure. The audit aligned item identifiers and recalculated differences without new inference. [A1, A2]

All sixteen item outputs contained a categorical certainty marker. Two items changed their primary label. Five changed at least one classification field, including primary labels or ancillary classification notes. These are different quantities: the five-item count must not be described as five primary-label changes.

The direct conclusion is narrow: asserted certainty coexisted with instability in these saved outputs. The counts do not estimate accuracy, an attack success rate or a causal ordering effect. No independent answer key was available. Category interpretation may be ambiguous; there was no repeated same-order control; no explicit random seed was saved; and batch context or tool-chain behavior could matter. Stable items cannot be assumed correct.

A distinct visible discussion also showed an agent challenging the person's interpretation of a linguistic cue, followed by a revised human judgment. [A3] This supports a behavioral observation that evidence-based disagreement was permitted. It does not establish that the agent's interpretation was independently correct or that an organizational culture has been quantitatively evaluated.

A useful next study would freeze the label ontology, obtain independent annotation with disagreement adjudication, and compare repeated identical orders with reordered and position-controlled conditions. Instability, correctness, justified refusal and confidence calibration should remain separate outcomes. If stable errors are common, consistency checking can only be an initial screen.

### 6.2 Case B Speech-recognition repair and parameter updates

An attributed audit report describes a person identifying a mistranscribed proper noun, requiring reference checking and retesting against the original audio, and having an implementation agent modify model parameters. The report states that the target passage was corrected and three additional known regression passages passed. [B1] We preserve the report of actual parameter modification rather than reclassifying the event as a prompt-only change.

However, the bounded audit did not recover sufficient original training logs, changed-tensor or adapter information, checkpoint comparisons, optimization settings and unseen-audio evaluation. No original audio was processed in this study. We therefore have not independently verified the parameter-update procedure or reproduced its result.

Correcting a known target and passing known regressions can support a local engineering repair. It cannot establish generalization to new speakers, contexts or recordings. A passage already used during development cannot simultaneously be an independent holdout. The distinction is between targeted fit and transferable improvement, not between a valuable and a worthless repair.

A future evaluation should record the changed mechanism and checkpoints, freeze unseen names, speakers and contexts, and include an unchanged model and lighter alternatives such as a lexicon or decoding hint. Proper-noun accuracy, overall transcription error, non-target regressions and resource costs should be reported separately. Benefits restricted to the original passage, or outweighed by broader regressions, would defeat a general-improvement claim.

### 6.3 Case C Evaluating a Harness without requiring it to win

The early audit summary reports that a person unfamiliar with a Harness required comparison on two real tasks using quality, time and cost, and accepted an unfavorable result described as slower and more expensive. [C1] Complete paired logs and total-cost accounting were not recovered. We report no speed or cost ratio and do not treat that comparison as independently recalculated.

A distinct later saved report provides additional negative evidence. In a two-phase local application-development task, four phase-level runs across two Harness configurations produced no delivery artifacts. The saved report lists zero passed checks against stage-specific totals of twelve or fifteen and records timeout or delivery failure. It also records resource interference, pending interface review, no real image generation and no accepted product. [C2] This study inspected the report; it did not execute those workloads again.

The later report shows that unsuccessful delivery was preserved as such. It cannot fill the evidential gaps in the earlier paired comparison. Resource contention, base-model ability, task decomposition, execution tools and time limits remain possible explanations. Zero external inference charges do not establish zero total cost: local runtime, electricity, occupied resources, preparation and human review must be considered, with unknown quantities retained as unknown.

The mechanism suggested by the case is willingness to let evaluation reject a preferred tool. It is not evidence that every Harness adds cost, or that reporting a failure creates a new software product. The stronger question is which organization of tools produces more independently correct delivery under comparable inputs and total budgets, and whether failure records reduce later repeated effort.

### 6.4 Case D Unnecessary acquisition and shared-resource governance

The fourth case began when an execution station checked the current service listing but failed to complete the required inventory of existing shared assets. It initiated a new model acquisition even though an existing local asset was adequate for the text task. The new and existing packages were not byte-identical: their components differed, and they later received separate roles. [D1]

The error was unnecessary new acquisition for the task at that time, not duplication of an identical file. Later assigning useful work to both packages does not erase the earlier failure to check. Free model licensing and local inference also do not erase transmission costs. This public version does not disclose private billing or asset-inventory details and does not claim an audited monetary saving.

The incident led to a shared registry, default responsibilities, borrowing approval and return records, and a configured periodic audit. Attribution matters: a human specified the enduring principles and allocation; engineering implemented the shared artifacts; the execution station retained responsibility for the acquisition error; and an organizational-management role analyzed the case. This paper does not claim those implementations as a new software invention of its authors. [D2]

The audit inspected a registry snapshot, rules and related artifacts. Ten files listed in a saved publication receipt matched their recorded hashes. [D3] This supports artifact existence and integrity. It does not establish that every entry was a unique usable model, that all runtime checks passed, that every station applied the rules or that later audit cycles completed.

Notification, receipt and self-reported implementation remain different from observed adoption. An L2 benefit claim requires later task evidence: fewer false absence judgments and unnecessary acquisitions, fewer borrowing conflicts, no unacceptable blockage of necessary work, and savings that exceed registry maintenance and coordination costs.

## 7 Cross-Case Interpretation

The common pattern is that a person identified a reliability or cost concern, translated it into a comparison or constraint, and attempted to preserve the resulting correction. This is an interpretive mechanism, not a statistical effect established by four randomized experiments.

The strongest recalculable observation is the classification-output difference. The clearest organizational implementation evidence is the resource-governance artifact set. The speech-recognition repair and early Harness cost comparison remain partly dependent on secondary reports. The later Harness report is direct but answers a different, narrower question. These asymmetries are part of the result.

The evidence supports the possibility that a person can formulate useful tests without implementing every repair or knowing every answer. It does not yet establish continued reliable improvement when the person stops supplying task-specific corrections, successful transfer to another station, or lower total human and resource costs.

Going beyond a person's prior task knowledge must not be confused with escaping the need for external evidence. A system may find a solution the person did not previously know and then validate it independently. That is different from declaring the solution correct because no one can currently check it. Verification designs can themselves be wrong and require criticism.

## 8 Falsifiable Propositions

**P1 Error detection beyond confidence filtering.** Under a frozen task definition and equal total inference limits, justified relation checks plus random audits of certain outputs improve detection of real errors without excessive rejection of healthy tasks. This is unsupported if alarms mainly reflect permitted ambiguity, if coverage collapses without better correct delivery, or if consistency improves while accuracy does not.

**P2 Net value of shared-resource governance.** On new requests, shared asset and borrowing rules reduce unnecessary acquisition and conflicts relative to service-list-only or ad hoc checking. This fails as a net-benefit claim if stale entries increase errors, necessary work is blocked, or maintenance and coordination cost exceed savings. Counting prevented downloads alone is insufficient.

**P3 Improvement without per-task human repair.** A bounded detect-propose-validate-update loop improves independently correct delivery on new tasks relative to a strong fixed-rule baseline, without the person giving answers or repeatedly repairing outputs. Benefits restricted to familiar cases, dependent on human answer provision, or absent in held-out target contexts would not support supervised organizational learning.

**P4 Useful persistence rather than record accumulation.** Versioned reuse reduces later human intervention while maintaining task quality. The proposition fails if documentation increases review burden, propagates errors or creates contention and permission violations that erase the gains. Memory volume is not a success metric.

The propositions are separable. Passing a classification screen does not validate resource governance. Parameter adaptation does not validate organizational transfer. Even positive results for P3 in a finite task domain would not establish open-world self-improvement.

## 9 Prospective Sandbox Protocol

### 9.1 Status and authority

All experiments in this section are proposals, not completed work. Call limits and thresholds are candidate preregistration choices, not active allocations or permissions to run models. Execution requires separately approved resources, frozen data and evaluators, and explicit stop conditions.

The initial study should use original synthetic tasks and nonredeemable test resources. Acquisition, borrowing, payment and publication are simulated actions; no real purchase, transfer or external write is needed. Existing registered models and runtimes should be reused only with the appropriate resource approval. An absent endpoint listing must not trigger a new download.

### 9.2 Units and independent evaluation

An experimental unit is a new incident or problem context, not a tool call, agent role or output field. Candidate families are externally checkable classification and evidence ordering; small code or state repair with a deterministic specification; asset aliases, versions and genuine absence; and borrowing, release and authorization conflicts. Each family must contain healthy negatives as well as repairable problems.

Task generation, answer keys and evaluation code should be sealed before execution. Executing agents must not receive hidden answers. Shared components between a generator and validator create correlated-defect risks; independently written assertions or external checks should address them. Development cases are permanently development data and must never be renamed holdouts.

Humans specify objectives and permissions before execution, supervise stop conditions and provide no per-item answers or repairs. Necessary clarifications are logged, counted as intervention and retained as protocol deviations. Hidden scoring criteria must not be changed after observing model behavior.

### 9.3 Three matched conditions

| Condition | Mechanism | Purpose |
| --- | --- | --- |
| A Standard execution | Same model and tools; task plus basic constraints | Baseline without the experience mechanism |
| B Fixed rules | Frozen human-authored checklist and registry | Strong existing-process baseline |
| C Bounded learning loop | Same initial rules as B; detection, proposals, independent validation and sandbox-version submission | Incremental value of dynamic updates |

Conditions use the same underlying task materials, context-length ceiling and maximum total generation/output budgets, with only the specified mechanism differences. C pays for checking and repair within its own limit; it receives no free unlimited judge. Actual costs are reported separately from equal ceilings.

Each condition starts from its own clean snapshot. Patches and answers do not leak between conditions. Presentation order is randomized or counterbalanced. Shared CPU and memory contention is coordinated and recorded; separate drive letters do not imply independent hardware.

Model weights remain unchanged in the first stage. Only explicitly scoped sandbox workflows and experience records may persist. Findings therefore concern workflow or memory changes, not model training. A parameter-update study would require its own data, checkpoints, costs and holdout protocol.

### 9.4 Finite budgets and stopping

A candidate feasibility stage contains at most six fresh contexts, three conditions and three generation calls per condition: at most 54 calls. A proposed per-call output ceiling is 512 tokens. Internal model requests count too. A proposed total wall-clock ceiling is 90 minutes; whichever bound is reached first stops the stage. Unfinished units remain unfinished. These limits are not a prediction that the workload fits this time.

Feasibility evaluates whether the task, contract and scoring process work within the limit. It does not confirm effectiveness. If all conditions encounter a basic capability floor or the evaluator is unreliable, the effectiveness comparison stops. Failures cannot be removed or thresholds lowered to create an advantage.

Only after feasibility and new authorization should a confirmation study freeze fresh cases. One candidate design has 24 unseen contexts, six in each family, with at most four generation calls per condition: 288 calls in total. Actual feasibility evidence must inform whether this scale is appropriate. This document does not initiate it.

Preparation, failed attempts, retries and auxiliary evaluation are accounted for. A timeout does not entitle a free rerun. Uncertain execution outcomes must be reconciled before a retry, and a better attempt must not silently replace an earlier result.

### 9.5 Outcomes and total cost

The primary outcome is an independently correct final task state achieved within authority. Completion coverage, anomaly detection, healthy-negative false alarms, regressions and refusals are separate outcomes. Reducing incorrect acceptance through indiscriminate refusal is not costless success. All paired A/B/C outcomes, including disagreements, should be available for inspection.

Record wall-clock and active runtime, input/output tokens, tool and model requests, transmitted bytes, paid services, peak memory and active human-intervention minutes. Include preparation, verification, reporting, bookkeeping and maintenance rather than moving these costs outside the experiment. Electricity or monetary totals remain unknown when unmeasured; zero API charge must not stand in for them.

A confirmation study could preregister one engineering target, such as at least four additional net correct deliveries by C relative to B across 24 contexts, subject to predefined limits on healthy-negative degradation, permissions and cost. Alternatively, it could target at least 20% less human intervention under a frozen quality noninferiority criterion. The primary target, tolerances and analysis must be chosen before viewing confirmation results, not selected afterward from whichever metric passes. Small samples require paired outcomes and uncertainty intervals; lack of significance does not establish equivalence.

Unauthorized external writes, protected-data disclosure, budget-control changes, bypassed borrowing approval or hidden-answer modification stop the affected run. Safety stopping is necessary governance, not a correct task outcome. Negative and mixed results remain in the full queue. A revised hypothesis requires new data.

### 9.6 Transfer and ablation

Transfer is evaluated in a new target context or task family. A receiving station obtains only the validated version and applicability conditions, not the answers. Source success precedes the transfer test. A delivered message is not a transferred benefit; failure to reproduce the gain is a substantive result.

Separately budgeted ablations can remove persistent memory, resource governance or independent validation. In particular, compare self-evaluation alone with external checks. Ablations require fresh inputs and may not grant the loop extra calls or human corrections. Otherwise, any gain could arise from unequal resources rather than the mechanism.

## 10 Discussion

### 10.1 Knowledge boundaries and responsibility

A person may be unable to solve a task while still requiring independent evidence, strong baselines, preserved counterexamples and stopping rules. This is a research-organization capability, not a claim that knowledge is unnecessary. Where evaluation is inadequate, expectations are disputed or expert judgment is required, automation should narrow its scope or defer the claim.

Accepting an agent's challenge may reduce pressure to fit a preferred narrative, but does not eliminate authority bias. Evidence must be allowed to overturn both the agent and the person. The roles holding resources, approving changes and bearing responsibility remain explicit.

### 10.2 Learning can relocate rather than reduce cost

More auditing can prevent incidents while increasing review work. More model debate can improve a subset of answers while consuming scarce compute and context. A registry can prevent acquisition while delaying necessary work through stale information. Organizational learning therefore requires net task and total-cost evidence, not a count of records, stations or messages.

One-person organization also depends on pre-existing software, model providers, research and other implementation roles. Sources and responsibilities must be credited. Integrating those contributions does not transform them into an independent invention by the organizer or the paper's authors.

### 10.3 Independence is structural

One model playing several roles shares failure risks; different models can still rely on the same wrong source. Information isolation, independently implemented checks and permission separation address different parts of the problem. None is infallible, but each is more inspectable than a role name.

Persistent success narratives can also reinforce errors. Experience needs applicability conditions, negative results, expiry and withdrawal. A rule inherited from another task is not universal. If a simple fixed procedure is sufficient, stopping a more elaborate learning proposal is an acceptable research result.

## 11 Limitations and Data Availability

This is a purposive case audit from one working environment. It does not isolate all effects of the organizer, base models, tools or resource conditions. Salient failures may be overrepresented, ordinary uneventful work is not comprehensively sampled, source visibility is bounded, and some claims remain secondary. There is no randomized organizational intervention or longitudinal adoption study here.

The classification audit reuses eight development inputs and lacks independent gold labels. The ASR training and unseen-test evidence were not recovered. The earlier Harness total-cost comparison was not independently verified. Its later saved failure report is a distinct supplement. Registry hash agreement verifies artifact integrity rather than runtime acceptance or causal benefits.

The manuscript and original companion documentation are released anonymously under CC0 1.0. Raw private conversations, identity information, task source passages, original audio, operational logs and internal source locators are excluded. Releasing this paper does not release those underlying records. The public evidence summaries disclose that limitation rather than imply open empirical reproducibility.

Writing and evidence organization were AI-assisted. No authorship or independent-replication credit is inferred for other implementation roles. No new inference, training, acquisition or prospective experiment was performed for the retrospective audit. Public literature remains subject to its original rights. Primary full text was inaccessible for some classical references; the reference inventory limits the corresponding verification claims to metadata and indexed abstracts.

## 12 Conclusion

OPU's potential lies in organizing goals, counterexamples, independent checks, limited authority and reusable experience, rather than simply multiplying model calls. The cases illustrate how verification requirements can arise: auditing certain answers, separating targeted repair from generalization, allowing a preferred Harness to fail, and turning an unnecessary acquisition into resource governance.

The present evidence remains layered: L1 has local observations and repair reports; L2 has implemented artifacts with adoption and net effects awaiting evaluation; L3 is an untested hypothesis. The next meaningful test is whether, without a person providing per-task answers or repairs, a bounded system can detect a new problem, propose an effective correction, pass independent held-out evaluation and transfer the benefit within authorization and rollback constraints. If it cannot, that result belongs in organizational memory too.

## References

[1] Ashby, W. Ross. 1956. *An Introduction to Cybernetics*. Chapman & Hall. [Official archive](https://www.ashby.info/Ashby-Introduction-to-Cybernetics.pdf).

[2] Flavell, John H. 1979. Metacognition and cognitive monitoring: A new area of cognitive-developmental inquiry. *American Psychologist* 34(10): 906-911. [DOI](https://doi.org/10.1037/0003-066X.34.10.906).

[3] Crossan, Mary M., Henry W. Lane, and Roderick E. White. 1999. An Organizational Learning Framework: From Intuition to Institution. *Academy of Management Review* 24(3): 522-537. [DOI](https://doi.org/10.5465/amr.1999.2202135).

[4] Hevner, Alan R., Salvatore T. March, Jinsoo Park, and Sudha Ram. 2004. Design Science in Information Systems Research. *MIS Quarterly* 28(1): 75-105. [Primary article record](https://aisel.aisnet.org/misq/vol28/iss1/6/).

[5] Chen, Tsong Yueh, Fei-Ching Kuo, Huai Liu, Pak-Lok Poon, Dave Towey, T. H. Tse, and Zhi Quan Zhou. 2018. Metamorphic Testing: A Review of Challenges and Opportunities. *ACM Computing Surveys* 51(1), Article 4: 1-27. [DOI](https://doi.org/10.1145/3143561).

[6] Zheng, Lianmin, Wei-Lin Chiang, Ying Sheng, et al. 2023. Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. *NeurIPS 2023 Datasets and Benchmarks Track*. [Original paper](https://arxiv.org/abs/2306.05685).

[7] Madaan, Aman, Niket Tandon, Prakhar Gupta, et al. 2023. Self-Refine: Iterative Refinement with Self-Feedback. [Original paper, version 2](https://arxiv.org/abs/2303.17651v2).

[8] Huang, Jie, Xinyun Chen, Swaroop Mishra, et al. 2024. Large Language Models Cannot Self-Correct Reasoning Yet. *ICLR 2024*. [Conference record](https://proceedings.iclr.cc/paper_files/paper/2024/hash/8b4add8b0aa8749d80a34ca5d941c355-Abstract-Conference.html).

[9] Shinn, Noah, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. 2023. Reflexion: Language Agents with Verbal Reinforcement Learning. [Original paper, version 4](https://arxiv.org/abs/2303.11366v4).

[10] Hu, Shengran, Cong Lu, and Jeff Clune. 2024-2025. Automated Design of Agentic Systems. Initial submission 2024; version 2 revised 2 March 2025. [Original paper](https://arxiv.org/abs/2408.08435v2).

[11] Lu, Chris, Cong Lu, Robert Tjarko Lange, et al. 2026. Towards end-to-end automation of AI research. *Nature* 651: 914-919. [DOI](https://doi.org/10.1038/s41586-026-10265-5).

[12] National Institute of Standards and Technology. 2023. *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. NIST AI 100-1. [DOI](https://doi.org/10.6028/NIST.AI.100-1).

## Appendix A Public Evidence Summary

| Record | Source class | Supported observation and remaining limitation |
| --- | --- | --- |
| A1 | D | An authorized classification-backtest request and a visible execution report; not an answer key |
| A2 | D and R | Two saved outputs, eight aligned items, two primary changes, five any-field changes, sixteen certainty markers; no new model run |
| A3 | D | A substantive challenge and revised judgment; no independent correctness adjudication |
| B1 | S | Parameter update and known regressions reported; original training and unseen-test evidence unavailable to this audit |
| C1 | S | An early unfavorable two-task comparison reported; paired total-cost evidence not recovered |
| C2 | D | A distinct later saved report with four unsuccessful phase-level deliveries and resource interference; not a reproduction of C1 |
| D1 | D and S | Unnecessary acquisition for a text task despite an adequate existing asset; packages not byte-identical |
| D2 | D | Registry, rules, loan records and periodic-audit configuration; effects and later cycles not established |
| D3 | D and R | Ten saved artifact hashes matched a receipt; integrity rather than runtime or adoption evidence |

Private originals are not included. The identifiers above are paper-local references, not operational account or conversation identifiers.
