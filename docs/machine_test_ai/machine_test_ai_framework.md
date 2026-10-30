# ZECPath AI – Machine Test AI Framework
## Day 50: Machine Test AI Design

**Status:** Design specification only; not implemented or production validated.

## 1. Objective

Design a machine-test system that evaluates job-related practical technical skills through realistic tasks. It supports coding problems, debugging tasks, file-based tasks, and mini system-design exercises. The system captures candidate work and produces explainable, rubric-based evaluation results.

The machine test is one evidence source in the hiring process. It must not be the sole basis for a hiring decision.

## 2. Machine-test types

### 2.1 Coding problems
Candidates implement a function, module, or small feature against a written specification.
- Inputs: prompt, language/runtime, starter repository, constraints, examples, hidden and visible tests.
- Outputs: source-code snapshots, test results, execution metadata, final submission.
- Evaluation: functional correctness, edge cases, complexity, readability, and explanation of approach.

### 2.2 Debugging tasks
Candidates receive a repository or code sample containing intentional defects.
- Inputs: issue description, reproducible failing tests, repository snapshot, permitted tools.
- Outputs: patch/diff, changed files, test execution results, candidate notes.
- Evaluation: defect diagnosis, regression safety, fix correctness, scope control, and reasoning.

### 2.3 File-based tasks
Candidates manipulate supplied files such as CSV, JSON, spreadsheets, logs, or documents.
- Inputs: files, task instructions, expected output schema, allowed libraries/tools.
- Outputs: generated files, transformation scripts where relevant, validation logs, artifact hashes.
- Evaluation: output correctness, schema compliance, data integrity, reproducibility, and clarity.

### 2.4 Mini system-design tasks
Candidates design a small service or feature, for example an API, data pipeline, or notification system.
- Inputs: requirements, constraints, expected design artifacts, optional diagram format.
- Outputs: architecture diagram, API/data model, trade-off notes, assumptions, and risk analysis.
- Evaluation: requirement coverage, architecture coherence, scalability appropriate to scope, reliability, security, and trade-off reasoning.
- Do not evaluate diagram aesthetics as a proxy for engineering skill.

## 3. Evaluation dimensions

| Dimension | What is evaluated | Example evidence |
|---|---|---|
| Correctness | Meets functional and stated requirements | Unit/hidden tests, output validation, acceptance checklist |
| Efficiency | Reasonable time and resource complexity for the task | Runtime, memory, algorithmic analysis, avoidable work |
| Code quality | Maintainability, clarity, modularity, error handling, conventions | Code review rubric, lint/static checks where appropriate |
| Problem-solving approach | Decomposition, assumptions, debugging method, trade-offs, validation | Work notes, checkpoints, patch history, candidate explanation |

Weights are configurable by task type. Automated tests should evaluate only criteria they can reliably observe. Human review is required for reasoning, design trade-offs, and context-dependent code quality.

## 4. Input, work, and output capture

### Candidate input
- Candidate/session/task identifiers (pseudonymous where possible).
- Task version, task type, difficulty, language/runtime and allowed resources.
- Start time, deadline, time limit, accommodation configuration.
- Candidate consent and assessment policy version.

### Work capture
- Periodic code snapshots and explicit save/submit events.
- File change list and patch/diff history.
- Execution events: command, exit code, duration, resource usage, test summary.
- Candidate explanation / approach notes, if requested.
- For file-based tasks: output artifact metadata, MIME type, size, hash, schema-validation result.
- For system design: submitted diagrams, structured design notes, API/data models.

Capture must be transparent and limited to the assessment workspace. Do not use covert screen recording, keystroke surveillance, or inspect unrelated applications. Avoid storing secrets or environment variables in logs.

### Final output
- Final submission and immutable task version.
- Test and validation results.
- Snapshot / artifact references and checksums.
- Dimension scores with evidence and explanations.
- Time metadata and any approved accommodation context.
- Human-review status and evaluator identity where applicable.

## 5. Scoring model

Each dimension is rated from 0 to 4 and converted to a weighted score from 0 to 100.

Base score:

`base_score = Σ((dimension_rating / 4) × dimension_weight × 100)`

Dimension weights by task type:

| Task type | Correctness | Efficiency | Code quality | Problem-solving |
|---|---:|---:|---:|---:|
| Coding | 40% | 20% | 20% | 20% |
| Debugging | 35% | 15% | 20% | 30% |
| File-based | 45% | 15% | 20% | 20% |
| Mini system design | 25% | 15% | 25% | 35% |

Task-specific rubric criteria must be published to the candidate at an appropriate level before the assessment. Hidden tests may protect against hard-coded outputs but must remain job-related and reviewed.

### Rating anchors

- 0 – Missing or wholly incorrect evidence.
- 1 – Major gaps; limited partial progress.
- 2 – Partially meets requirements; material gaps remain.
- 3 – Meets core requirements with minor issues.
- 4 – Fully meets requirements with strong, well-supported evidence.

A score must include evidence references and a short explanation. Missing evidence is not automatically a zero; mark the dimension `not_assessable` and route for review if the task or capture failed.

## 6. Time-based scoring

Time is recorded separately from the technical base score.

- The task has a published time limit and clear start/deadline rules.
- Use server-authoritative timestamps and monotonic elapsed-time measurement where possible.
- Pause or extend time for platform outages and approved accommodations.
- Do not award a large speed bonus. Fast completion is not proof of skill.
- Do not penalize candidates for using the allowed time to validate or improve their solution.
- If time weighting is required, use a small, capped process-completion component only after core correctness is met.

Recommended design:
- `time_status`: `within_limit`, `submitted_after_limit`, `paused_for_approved_reason`, `technical_extension`.
- `time_efficiency_rating`: 0–4, assessed against task-specific expected effort and quality, not raw speed alone.
- Keep the time-efficiency dimension within the task-type efficiency weight.
- Never let time efficiency compensate for failed correctness or missing required deliverables.

## 7. Evaluation pipeline

1. Task assignment and candidate instructions.
2. Workspace provisioning and environment verification.
3. Start event and time-limit tracking.
4. Candidate work with transparent snapshots and execution capture.
5. Submission freeze and artifact integrity checks.
6. Automated evaluation: tests, schema checks, static checks, resource limits.
7. Human evaluation: code quality, reasoning, design trade-offs, ambiguous cases.
8. Weighted score calculation and evidence-linked report generation.
9. Human review and documented disposition.

## 8. Security and reliability

- Run candidate code in isolated, ephemeral sandboxes.
- Apply CPU, memory, wall-clock, filesystem, network, and process limits.
- Default to no outbound network access; allow only explicitly approved dependencies.
- Use non-root execution, read-only base images, temporary workspaces, and cleanup after evaluation.
- Never execute candidate code on the application server or production database.
- Prevent access to other candidates' workspaces and secrets.
- Version tasks, tests, runtimes, and scoring rubrics.
- Log evaluator actions and maintain artifact hashes.
- Test for flaky tests and environment-dependent outcomes.

## 9. Accessibility, fairness, and accommodations

- Provide clear instructions and accessible editor/workspace options.
- Support approved extra time or alternative input methods without lowering technical expectations.
- Do not treat typing speed, mouse movement, or continuous activity as a measure of problem-solving ability.
- Validate tasks across supported operating systems and runtimes.
- Review score distributions and error rates for unintended barriers.
- Provide a human review and appeal/clarification path.

## 10. Report format

A machine-test evaluation report should contain:
- candidate/session/task metadata;
- task type, version, difficulty, and allowed environment;
- submission and artifact references;
- execution/test results;
- dimension scores, weights, evidence and explanations;
- time status and approved adjustments;
- limitations, failed infrastructure checks, and human-review status;
- evaluator and rubric versions.

## 11. Acceptance criteria

- Four task types are supported in the design.
- Every score maps to a defined rubric and captured evidence.
- Code execution is sandboxed and resource-limited.
- Code snapshots and execution results are captured transparently.
- Time is measured separately and cannot override correctness.
- Automated and human evaluation responsibilities are clearly separated.
- Failed infrastructure or missing evidence does not silently become a candidate failure.
- Reports are explainable, versioned, and reviewable.

## 12. Implementation boundary

This deliverable is a design specification. It does not claim that a task runner, code sandbox, snapshot service, automated grader, timer, or scoring engine has been implemented.
