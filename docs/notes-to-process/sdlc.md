---
title: SDLC Workflows
description: "Domain reference mapping 14 SDLC workflows, 7 reusable sub-flows, and Definition of Done."
---

# SDLC Workflows

> Domain reference for planning future core plugins. This document does NOT define the Bazaar's own development process — it maps the SDLC domain that core plugins will encode as skills, hooks, and agents.

**Purpose:** This document maps standard software development workflows as the domain model for the Bazaar's core plugins. Each workflow identifies the agent roles, decision points, and reusable sub-flows that plugins encode as skills, hooks, agents, MCP servers, and LSP servers. Plugin specs reference this document rather than duplicating its analysis.

**Status:** Draft

---

## Workflow Catalog

| Workflow              | Description                                              | Frequency  | Status                       |
| --------------------- | -------------------------------------------------------- | ---------- | ---------------------------- |
| New Project Setup     | Greenfield scaffold, configure, establish patterns       | Rare       | Mapped                       |
| New Feature           | Full cycle: plan → decompose → implement → verify → docs | Common     | Mapped                       |
| Extend/Modify Feature | Change existing behavior, has prior context              | Common     | Mapped                       |
| Bug Fix               | Diagnose → fix → regression test                         | Common     | Mapped                       |
| Refactoring           | Improve code without behavior change                     | Occasional | See Story Cycle, Maintenance |
| Spike/Exploration     | Research before committing to approach                   | Occasional | Mapped                       |
| Maintenance           | Dependency updates, cleanup, security patches            | Periodic   | Mapped                       |
| Documentation         | Standalone doc work (not tied to feature)                | Occasional | Mapped                       |
| Infrastructure Change | CI/CD, deployment config, environment setup              | Occasional | Mapped                       |
| Release / Deployment  | Prepare and ship a release                               | Periodic   | Mapped                       |
| Incident Response     | Production incident, fast diagnosis and fix              | Rare       | Mapped                       |
| Audit                 | Security audit, performance review, code quality sweep   | Periodic   | Mapped                       |
| Retrospective         | Team reflection, process improvement                     | Periodic   | Mapped                       |
| Onboarding            | New project context, getting oriented                    | Rare       | Mapped                       |

---

## Sub-flows

Reusable building blocks composed by main workflows.

### Review Gate

Quality check before merge. Used by Story Cycle and Infra Cycle.

**Agents:** Code Reviewer (primary), Architect (contributor for design/security concerns)

```mermaid
flowchart TD
    START([Changes Ready]) --> CR[Code Reviewer: Review]
    CR --> DECIDE{Approved?}
    DECIDE -->|Changes requested| AUTHOR[Author addresses feedback]
    AUTHOR --> CR
    DECIDE -->|Approved| DONE([Ready for Merge])
```

---

### Three Amigos

Planning ceremony for shared understanding.

**Agents:** Business Analyst (leads), Software Engineer, Test Engineer, Architect (always present, chooses engagement level)

**Output:** Refined acceptance criteria, edge cases, escalation flag

```mermaid
flowchart TD
    START([Work Item Identified]) --> BA[Business Analyst: Present requirements]
    BA --> DISCUSS[BA + SE + TE + Architect: Discuss understanding]
    DISCUSS --> EDGE[Test Engineer: Identify edge cases]
    EDGE --> TECH[Software Engineer: Flag technical concerns]
    TECH --> DEPTH{Deep design needed?}
    DEPTH -->|Yes| DESIGN[Architect: Lead design discussion]
    DESIGN --> OUTPUT
    DEPTH -->|No| OUTPUT
    OUTPUT([Output: Refined criteria, edge cases, escalation flag])
```

---

### Decomposition

Break approved scope into trackable issues.

**Agents:** Business Analyst (stories), Architect (technical tasks), Software Engineer (technical tasks), Test Engineer (testing tasks)

```mermaid
flowchart TD
    START([Approved Scope]) --> MS[Business Analyst: Create milestone]
    MS --> STORIES[Business Analyst: Draft user stories]
    STORIES --> TASKS[Architect + Software Engineer: Identify technical tasks]
    TASKS --> TEST[Test Engineer: Add testing tasks if needed]
    TEST --> ISSUES[Create issues, link to milestone]
    ISSUES --> OP[/Code Actual: Approve breakdown/]
    OP --> DONE([Ready for execution])
```

---

### Story Cycle

Implement a single issue from start to merge. Includes TDD's red-green-refactor.

**Agents:** Software Engineer, Test Engineer (if integration tests needed), Code Reviewer

**Assumes:** 1 Issue = 1 PR

```mermaid
flowchart TD
    START([Issue Assigned]) --> IMPL[Software Engineer: Implement with TDD]
    IMPL --> GREEN{Tests green?}
    GREEN -->|No| IMPL
    GREEN -->|Yes| REFACTOR[Software Engineer: Refactor if needed]
    REFACTOR --> VERIFY{Integration tests needed?}
    VERIFY -->|Yes| TE[Test Engineer: Add integration/e2e tests]
    VERIFY -->|No| REVIEW
    TE --> REVIEW[Code Reviewer: Review code + tests]
    REVIEW --> APPROVED{Approved?}
    APPROVED -->|Changes requested| IMPL
    APPROVED -->|Yes| PASS{Tests pass?}
    PASS -->|No| IMPL
    PASS -->|Yes| OP[/Code Actual: Merge decision/]
    OP --> MERGE[Merge + Close Issue]
    MERGE --> DONE([Issue Complete])
```

---

### Infra Cycle

Implement and deploy infrastructure changes.

**Agents:** DevSecOps Engineer (primary), Architect (design review), Code Reviewer (code quality)

```mermaid
flowchart TD
    START([Infra Change Needed]) --> IMPL[DevSecOps Engineer: Implement IaC/pipeline changes]
    IMPL --> VALIDATE[DevSecOps Engineer: Validate/lint/dry-run]
    VALIDATE --> REVIEW[Architect + Code Reviewer: Review]
    REVIEW --> APPROVED{Approved?}
    APPROVED -->|Changes requested| IMPL
    APPROVED -->|Yes| STAGE[DevSecOps Engineer: Deploy to staging]
    STAGE --> SMOKE[Verify: Smoke tests]
    SMOKE --> PASS{Pass?}
    PASS -->|No| IMPL
    PASS -->|Yes| OP[/Code Actual: Production approval/]
    OP --> PROD[DevSecOps Engineer: Deploy to production]
    PROD --> DONE([Infra Change Complete])
```

---

### Doc Update

Create or update documentation.

**Agents:** Technical Writer (primary), Business Analyst (requirements accuracy), Software Engineer or Architect (technical accuracy), Document Reviewer (quality review)

```mermaid
flowchart TD
    START([Docs Needed]) --> IDENTIFY[Technical Writer: Identify scope and audience]
    IDENTIFY --> DRAFT[Technical Writer: Draft documentation]
    DRAFT --> VERIFY[BA + SE/Architect: Verify accuracy]
    VERIFY --> ACCURATE{Accurate?}
    ACCURATE -->|No| DRAFT
    ACCURATE -->|Yes| REVIEW[Document Reviewer: Quality review]
    REVIEW --> CLEAR{Clear?}
    CLEAR -->|No| DRAFT
    CLEAR -->|Yes| DONE([Docs Published])
```

---

### Discovery

Understand current state before proposing changes. Used when modifying existing behavior.

**Agents:** Business Analyst (spec), Software Engineer (code), Test Engineer (coverage), Architect (if cross-cutting)

**Output:** Current state summary, dependencies identified, regression risk areas flagged

```mermaid
flowchart TD
    START([Change Request]) --> SPEC[Business Analyst: Review existing spec]
    SPEC --> CODE[Software Engineer: Review current implementation]
    CODE --> TESTS[Test Engineer: Review existing test coverage]
    TESTS --> CROSS{Cross-cutting?}
    CROSS -->|Yes| ARCH[Architect: Identify dependencies and ripple effects]
    ARCH --> OUTPUT
    CROSS -->|No| SE[Software Engineer: Identify local dependencies]
    SE --> OUTPUT
    OUTPUT([Output: Current state summary, impact assessment, regression risks])
```

---

## Mapped Workflows

### New Feature

**When:** Code Actual requests new functionality
**Frequency:** Common

#### Agents Involved

- **Business Analyst** — Requirements, spec, stories, acceptance criteria
- **Architect** — (if escalated) Architectural guidance, ADRs, technical tasks
- **Software Engineer** — Technical tasks, implementation with TDD
- **Test Engineer** — Edge cases, integration/e2e tests, testing tasks
- **Code Reviewer** — Quality gate
- **DevSecOps Engineer** — (if infra needed) Pipeline or environment changes
- **Technical Writer** — (if user-facing) Documentation updates

#### Flow

```mermaid
flowchart TD
    subgraph Planning
        START([New Feature Request]) --> SPEC[Business Analyst: Draft spec]
        SPEC --> TA[[Three Amigos]]
        TA --> OP1[/Code Actual: Approve scope/]
    end

    subgraph Breakdown
        OP1 --> DECOMP[[Decomposition]]
    end

    subgraph Execution
        DECOMP --> LOOP{More issues?}
        LOOP -->|Yes| STORY[[Story Cycle]]
        STORY --> INFRA{Infra needed?}
        INFRA -->|Yes| IC[[Infra Cycle]]
        IC --> LOOP
        INFRA -->|No| LOOP
        LOOP -->|No| INTEGRATION[Test Engineer: Final integration verification]
    end

    subgraph Wrap-up
        INTEGRATION --> DOCS{User-facing?}
        DOCS -->|Yes| DOC[[Doc Update]]
        DOC --> CLOSE
        DOCS -->|No| CLOSE[Close milestone]
        CLOSE --> DONE([Feature Complete])
    end
```

#### Code Actual Checkpoints

- After Three Amigos → approve scope before decomposition
- After Decomposition → approve breakdown and sequencing
- Per Story Cycle → merge decision for each issue
- Per Infra Cycle → production deployment approval (if applicable)

#### Key Points

- **Spec before code** — Business Analyst drafts spec during Planning
- **Three Amigos required** — Shared understanding before decomposition
- **One Issue = One PR** — Per Story Cycle convention
- **User-facing = docs** — Technical Writer updates docs at wrap-up

#### Variations

- **Small feature:** Skip Decomposition if it's genuinely one story
- **API change:** Architect involved from Planning, not just on escalation
- **Infra-heavy feature:** DevSecOps Engineer joins Three Amigos

---

### Extend/Modify Feature

**When:** Code Actual requests changes to existing functionality
**Frequency:** Common

#### Agents Involved

- **Business Analyst** — Spec review, spec updates, stories
- **Architect** — (if cross-cutting) Impact assessment, ADRs if patterns change
- **Software Engineer** — Code review, implementation, local impact assessment
- **Test Engineer** — Coverage review, regression risks, integration/e2e tests
- **Code Reviewer** — Quality gate
- **DevSecOps Engineer** — (if infra affected) Pipeline or environment changes
- **Technical Writer** — (if user-facing) Documentation updates

#### Flow

```mermaid
flowchart TD
    subgraph Understanding
        START([Change Request]) --> DISC[[Discovery]]
        DISC --> OP1[/Code Actual: Proceed or abort/]
    end

    subgraph Planning
        OP1 --> SPEC[Business Analyst: Draft spec updates]
        SPEC --> TRIVIAL{Trivial change?}
        TRIVIAL -->|No| TA[[Three Amigos]]
        TA --> OP2[/Code Actual: Approve scope/]
        TRIVIAL -->|Yes| OP2
    end

    subgraph Breakdown
        OP2 --> SINGLE{Single story?}
        SINGLE -->|No| DECOMP[[Decomposition]]
        DECOMP --> EXEC
        SINGLE -->|Yes| EXEC
    end

    subgraph Execution
        EXEC[Verify work breakdown] --> LOOP{More issues?}
        LOOP -->|Yes| STORY[[Story Cycle]]
        STORY --> INFRA{Infra affected?}
        INFRA -->|Yes| IC[[Infra Cycle]]
        IC --> LOOP
        INFRA -->|No| LOOP
        LOOP -->|No| REGR[Test Engineer: Regression verification]
    end

    subgraph Wrap-up
        REGR --> PASS{All good?}
        PASS -->|No| LOOP
        PASS -->|Yes| DOCS{User-facing?}
        DOCS -->|Yes| DOC[[Doc Update]]
        DOC --> CLOSE
        DOCS -->|No| CLOSE[Close milestone/issue]
        CLOSE --> DONE([Change Complete])
    end
```

#### Code Actual Checkpoints

- After Discovery → decide whether to proceed (impact might be too high)
- After Planning → approve scope
- After Decomposition → approve breakdown (if applicable)
- Per Story Cycle → merge decision for each issue
- Per Infra Cycle → production deployment approval (if applicable)

#### Key Points

- **Discovery first** — Understand current state before proposing changes
- **Abort option** — Discovery may reveal change isn't worth impact
- **Regression focus** — Test Engineer verifies existing behavior preserved
- **Delta specs** — Update existing specs, don't create new ones

#### Key Differences from New Feature

- **Discovery phase** — Must understand current state before planning
- **Spec updates** — Delta changes, not new spec creation
- **Regression verification** — Explicit step to verify existing behavior preserved
- **Abort option** — Discovery might reveal the change isn't worth the impact

#### Variations

- **Trivial change:** Skip Three Amigos if change is obviously contained
- **Breaking change:** Architect involved throughout, may need ADR for migration strategy
- **Deprecation:** Business Analyst documents sunset plan, Technical Writer updates migration guides

---

### Bug Fix

**When:** Post-merge defect reported or discovered
**Frequency:** Common

**Scope:** Defects in merged code. Bugs found during active development are fixed inline as part of Story Cycle.

#### Agents Involved

- **Business Analyst** — Triage (user-facing severity), acceptance criteria for fix
- **Software Engineer** — Triage (technical assessment), diagnosis, fix implementation
- **Test Engineer** — Verify fix, add regression test
- **Code Reviewer** — Quality gate (always)
- **Architect** — (if systemic) Root cause reveals architectural issue

#### Flow

```mermaid
flowchart TD
    subgraph Triage
        START([Bug Reported]) --> REPRO{Repro steps clear?}
        REPRO -->|No| CLARIFY[Business Analyst: Clarify with reporter]
        CLARIFY --> REPRO
        REPRO -->|Yes| ASSESS[BA + SE: Assess severity]
        ASSESS --> SEV{Severity?}
    end

    subgraph Diagnosis
        SEV -->|Critical| DIAG[Software Engineer: Diagnose root cause]
        SEV -->|High/Normal/Low| ISSUE[Business Analyst: Create issue]
        ISSUE --> DIAG
        DIAG --> SYSTEMIC{Systemic problem?}
        SYSTEMIC -->|Yes| ARCH[Architect: Assess scope]
        ARCH --> OP1[/Code Actual: Scope decision/]
        SYSTEMIC -->|No| FIX
    end

    subgraph Fix
        OP1 --> FIX[Software Engineer: Implement fix with TDD]
        FIX --> REGR[Test Engineer: Add regression test]
        REGR --> REVIEW[Code Reviewer: Review fix + test]
        REVIEW --> APPROVED{Approved?}
        APPROVED -->|Changes requested| FIX
        APPROVED -->|Yes| OP2[/Code Actual: Merge decision/]
    end

    subgraph Close
        OP2 --> MERGE[Merge + Close Issue]
        MERGE --> SPEC{Spec update needed?}
        SPEC -->|Yes| UPDATE[Business Analyst: Update spec]
        UPDATE --> DONE
        SPEC -->|No| DONE([Bug Fixed])
    end
```

#### Code Actual Checkpoints

- After Architect assessment (if systemic) → decide scope of fix
- After Code Review → merge decision

#### Severity Handling

| Severity | Issue first?   | Notes                                   |
| -------- | -------------- | --------------------------------------- |
| Critical | No — fix first | Create issue retroactively for tracking |
| High     | Yes            | Prioritize immediately                  |
| Normal   | Yes            | Standard queue                          |
| Low      | Yes            | Backlog                                 |

#### Key Points

- **No Three Amigos** — Bugs have clear acceptance criteria: "it should work"
- **No Decomposition** — Single issue. If diagnosis reveals bigger problems, escalate to Code Actual
- **Regression test required** — Per Definition of Done for bugs
- **Spec update** — If the bug revealed a spec gap, fix the spec too

#### Variations

- **Critical/production:** Skip issue creation, fix immediately, document retroactively
- **Systemic issue:** May spawn Refactoring or Maintenance workflow after immediate fix
- **Flaky test:** Test Engineer owns diagnosis, not Software Engineer

---

### Spike/Exploration

**When:** Uncertainty needs resolution before committing to an approach
**Frequency:** Occasional

**Output:** Knowledge, not production code. May produce throwaway prototypes.

#### Agents Involved

- **Architect** — Design spikes, evaluating architectural options
- **Software Engineer** — Technical feasibility spikes
- **Test Engineer** — (if relevant) Testability exploration
- **DevSecOps Engineer** — (if relevant) Infra/deployment exploration

#### Flow

```mermaid
flowchart TD
    START([Uncertainty Identified]) --> DEFINE[Code Actual + Architect: Define question and time box]
    DEFINE --> OP1[/Code Actual: Approve spike scope/]
    OP1 --> EXPLORE[Assigned agent: Investigate]
    EXPLORE --> DOCUMENT[Document findings + options]
    DOCUMENT --> RECOMMEND[Recommendation to Code Actual]
    RECOMMEND --> OP2[/Code Actual: Decide next steps/]
    OP2 --> OUTCOME{Outcome}
    OUTCOME -->|Feasible| ADR{ADR needed?}
    ADR -->|Yes| WRITE[Architect: Write ADR]
    WRITE --> DONE
    ADR -->|No| DONE([Spike Complete])
    OUTCOME -->|Not feasible| PIVOT[Revisit approach]
    PIVOT --> DONE
```

#### Code Actual Checkpoints

- Before spike → approve scope and time box
- After findings → decide next steps (proceed, pivot, or abandon)

#### Key Points

- **Time-boxed** — Fixed duration, not open-ended research
- **No code review** — Prototype code is throwaway
- **No tests** — It's exploratory
- **ADR if significant** — Capture the decision for future reference

#### Variations

- **Library evaluation:** Software Engineer compares options, documents trade-offs
- **Architecture spike:** Architect explores design approaches, may involve multiple agents
- **Vendor evaluation:** May involve external research, demos, proof of concept

---

### Maintenance

**When:** Periodic maintenance cycle or triggered by vulnerability report
**Frequency:** Periodic

**Output:** Prioritized Issues for maintenance work

#### Agents Involved

- **DevSecOps Engineer** — Dependency audit, security scan, infra health
- **Software Engineer** — Code quality audit, TODO/FIXME review
- **Test Engineer** — Test health, flaky test identification, coverage gaps
- **Architect** — Pattern compliance, structural concerns
- **Code Reviewer** — (optional) Quick code smell survey

#### Flow

```mermaid
flowchart TD
    START([Maintenance Cycle Triggered]) --> AUDIT

    subgraph AUDIT[Parallel Audit]
        direction LR
        DEPS[DevSecOps: Dependency + security scan]
        CODE[Software Engineer: Code quality review]
        TEST[Test Engineer: Test health check]
        ARCH[Architect: Pattern compliance]
    end

    DEPS --> COLLECT[Collect findings]
    CODE --> COLLECT
    TEST --> COLLECT
    ARCH --> COLLECT
    COLLECT --> TRIAGE[/Code Actual: Prioritize findings/]
    TRIAGE --> ISSUES[Create Issues for approved items]
    ISSUES --> EXECUTE[Execute via normal cycles]
    EXECUTE -->|Code changes| STORY[[Story Cycle]]
    EXECUTE -->|Infra changes| INFRA[[Infra Cycle]]
    STORY --> DONE([Maintenance Complete])
    INFRA --> DONE
```

#### Code Actual Checkpoints

- After audit → prioritize what gets addressed this cycle
- Per Issue → normal merge decisions via Story/Infra Cycle

#### Key Points

- **Discovery-focused** — Main job is surfacing and organizing work
- **Batched execution** — Multiple small Issues, worked in sequence
- **Lower ceremony** — No spec, no Three Amigos (work is well-defined)
- **Escalation** — If audit reveals big problems, escalate before creating Issues

#### Variations

- **Security-triggered:** Vulnerability report triggers immediate audit of affected area
- **Pre-feature cleanup:** Targeted audit before starting major new work
- **Scheduled:** Regular cadence (monthly, quarterly) for proactive hygiene
- **Process-triggered:** Retro findings spawn maintenance work

---

### Documentation (Standalone)

**When:** Doc work not tied to a specific feature
**Frequency:** Occasional

**Scope:** Creating new docs or overhauling existing docs as an independent initiative. For docs accompanying features, use Doc Update sub-flow.

#### Agents Involved

- **Technical Writer** — Primary owner, drafting, structure
- **Business Analyst** — User-facing accuracy, requirements docs
- **Architect** — Technical accuracy for architecture docs
- **Software Engineer** — Technical accuracy for implementation docs
- **DevSecOps Engineer** — Infra/ops docs
- **Document Reviewer** — Quality review before publishing

#### Flow

```mermaid
flowchart TD
    START([Doc Need Identified]) --> SCOPE[Technical Writer: Assess scope and audience]
    SCOPE --> GAPS[Technical Writer: Identify gaps in existing docs]
    GAPS --> OP1[/Code Actual: Approve scope/]
    OP1 --> PLAN[Technical Writer: Create outline, identify SMEs]
    PLAN --> DRAFT[Technical Writer: Draft content]
    DRAFT --> SME[SMEs: Verify accuracy]
    SME --> ACCURATE{Accurate?}
    ACCURATE -->|No| DRAFT
    ACCURATE -->|Yes| PEER[Peer review for clarity]
    PEER --> CLEAR{Clear?}
    CLEAR -->|No| DRAFT
    CLEAR -->|Yes| PUBLISH[Publish docs]
    PUBLISH --> DONE([Documentation Complete])
```

#### Code Actual Checkpoints

- After scoping → approve scope and priority

#### Key Points

- **Audience-first** — Define who the docs are for before writing
- **SME involvement** — Right experts verify right sections
- **Iterative** — Draft → review → refine cycle

#### Variations

- **Onboarding docs:** Heavy BA + Architect involvement for system overview
- **API reference:** Software Engineer as primary SME
- **Runbooks:** DevSecOps Engineer as primary author, Technical Writer polishes

---

### Infrastructure Change

**When:** Standalone infra work not tied to a specific feature
**Frequency:** Occasional

**Scope:** CI/CD changes, environment setup, cloud resources, monitoring. For infra work supporting a feature, use Infra Cycle sub-flow within the feature workflow.

#### Agents Involved

- **DevSecOps Engineer** — Primary owner, implementation
- **Architect** — Design review, patterns, ADR if needed
- **Software Engineer** — (if app changes needed) Config, environment variables
- **Technical Writer** — Runbooks, setup guides

#### Flow

```mermaid
flowchart TD
    START([Infra Need Identified]) --> SCOPE[DevSecOps Engineer: Assess scope and impact]
    SCOPE --> DESIGN[DevSecOps + Architect: Design approach]
    DESIGN --> OP1[/Code Actual: Approve design/]
    OP1 --> ADR{Significant decision?}
    ADR -->|Yes| WRITE[Architect: Write ADR]
    WRITE --> IMPL
    ADR -->|No| IMPL
    IMPL[[Infra Cycle]]
    IMPL --> DOCS[DevSecOps → Technical Writer: Update runbooks/guides]
    DOCS --> DONE([Infrastructure Change Complete])
```

#### Code Actual Checkpoints

- After design → approve design and approach
- Within Infra Cycle → production deployment approval

#### Key Points

- **Planning upfront** — Scope and design before implementation
- **ADR for significant choices** — Capture decisions that are hard to reverse
- **Infra Cycle handles execution** — Validate, review, stage, prod
- **Documentation required** — Runbooks and setup guides updated

#### Variations

- **New environment:** Heavy planning, likely ADR, full documentation
- **Pipeline optimization:** Lighter planning, may skip ADR
- **Migration:** Phased approach, rollback plan critical

---

### Release / Deployment

**When:** Ready to ship a release
**Frequency:** Periodic

**Scope:** Versioning, changelog, deployment, verification. May include multiple merged features/fixes.

#### Agents Involved

- **DevSecOps Engineer** — Build, deploy, verify infrastructure
- **Business Analyst** — Release notes (user-facing changes)
- **Technical Writer** — Polish release notes, update docs
- **Test Engineer** — Smoke tests, post-deploy verification
- **Architect** — (if needed) Verify architectural integrity

#### Flow

```mermaid
flowchart TD
    START([Release Triggered]) --> SCOPE[DevSecOps + BA: Define release scope]
    SCOPE --> OP1[/Code Actual: Approve release scope/]
    OP1 --> VERSION[DevSecOps Engineer: Version bump]
    VERSION --> CHANGELOG[BA + Technical Writer: Changelog and release notes]
    CHANGELOG --> BUILD[DevSecOps Engineer: Build release artifacts]
    BUILD --> STAGE[DevSecOps Engineer: Deploy to staging]
    STAGE --> VERIFY_STAGE[Test Engineer: Smoke tests on staging]
    VERIFY_STAGE --> PASS_STAGE{Pass?}
    PASS_STAGE -->|No| FIX[Fix issues, rebuild]
    FIX --> BUILD
    PASS_STAGE -->|Yes| OP2[/Code Actual: Approve production deploy/]
    OP2 --> PROD[DevSecOps Engineer: Deploy to production]
    PROD --> VERIFY_PROD[Test Engineer: Smoke tests on production]
    VERIFY_PROD --> PASS_PROD{Pass?}
    PASS_PROD -->|No| ROLLBACK[DevSecOps Engineer: Rollback]
    ROLLBACK --> POSTMORTEM[Investigate, return to Fix]
    POSTMORTEM --> FIX
    PASS_PROD -->|Yes| ANNOUNCE[Technical Writer: Publish release notes]
    ANNOUNCE --> DONE([Release Complete])
```

#### Code Actual Checkpoints

- Before release → approve scope (what's shipping)
- Before production → approve production deployment

#### Key Points

- **Staged rollout** — Always staging before production
- **Rollback plan** — Must have a way back if production fails
- **Verification required** — Smoke tests at each stage
- **Release notes** — User-facing communication of changes

#### Variations

- **Hotfix:** Expedited path — smaller scope, faster cycle, still needs staging verification
- **Scheduled release:** Regular cadence, scope defined by what's merged
- **Feature flag release:** Deploy code dark, enable via flags separately

---

### Incident Response

**When:** Production is broken, needs immediate attention
**Frequency:** Rare

**Scope:** Stabilize production first, root cause and proper fix later. Speed over ceremony.

#### Agents Involved

- **DevSecOps Engineer** — Infra investigation, rollback, emergency deployment
- **Software Engineer** — Code investigation, hotfix
- **Test Engineer** — Verify fix works
- **Architect** — (if systemic) Broader assessment
- **Business Analyst** — Stakeholder communication, status updates

#### Flow

```mermaid
flowchart TD
    START([Incident Detected]) --> TRIAGE[DevSecOps + SE: Assess severity]
    TRIAGE --> SEV{Severity?}
    SEV -->|Critical| CAN_ROLLBACK
    SEV -->|High| NOTIFY[BA: Notify stakeholders]
    NOTIFY --> CAN_ROLLBACK
    SEV -->|Medium| SCHEDULE[Schedule for normal hours]
    SCHEDULE --> CAN_ROLLBACK

    subgraph Stabilize
        CAN_ROLLBACK{Can rollback fix it?}
        CAN_ROLLBACK -->|Yes| ROLLBACK[DevSecOps: Rollback]
        CAN_ROLLBACK -->|No| HOTFIX[Software Engineer: Emergency hotfix]
        HOTFIX --> VERIFY[Test Engineer: Verify fix]
        VERIFY --> DEPLOY[DevSecOps: Emergency deploy]
        ROLLBACK --> CONFIRM
        DEPLOY --> CONFIRM[Confirm stability]
    end

    CONFIRM --> STABLE{Stable?}
    STABLE -->|No| CAN_ROLLBACK
    STABLE -->|Yes| UPDATE[BA: Status update — resolved]
    UPDATE --> OP1[/Code Actual: Proceed to postmortem/]

    subgraph Postmortem
        OP1 --> RCA[Team: Root cause analysis]
        RCA --> WHYS[Apply 5 Whys or similar]
        WHYS --> DOCUMENT[Document findings]
        DOCUMENT --> ISSUES[Create follow-up Issues]
    end

    ISSUES --> DONE([Incident Closed])
```

#### Code Actual Checkpoints

- After stabilization → decide when to proceed to postmortem (may need rest first)

#### Key Points

- **Stabilize first** — Get production working, proper fix comes later
- **Rollback preferred** — If rollback fixes it, do that before attempting hotfix
- **Communication** — Keep stakeholders informed throughout
- **Postmortem required** — Always understand what happened
- **5 Whys** — Or similar root cause technique to dig beyond surface symptoms
- **Follow-up Issues** — Postmortem spawns proper Bug Fix or System Story work

#### Severity Levels

| Severity | Example                                 | Response                  |
| -------- | --------------------------------------- | ------------------------- |
| Critical | System down, data loss                  | All hands, immediate      |
| High     | Major feature broken, workaround exists | Core team, urgent         |
| Medium   | Degraded performance, partial outage    | Normal hours, prioritized |

#### Variations

- **Security incident:** DevSecOps leads, may involve external notification requirements
- **Data incident:** Extra care around communication, potential compliance implications
- **Cascading failure:** Architect involved early to assess system-wide impact

---

### New Project Setup

**When:** Greenfield project initiation
**Frequency:** Rare

**Scope:** Initial repository, CI/CD, project structure, foundational ADRs, and documentation. Ends when ready for first feature work.

#### Agents Involved

| Agent              | Responsibility                                                   |
| ------------------ | ---------------------------------------------------------------- |
| Architect          | Tech selection, initial ADRs, patterns, project structure design |
| DevSecOps Engineer | Repo setup, CI/CD pipeline, dev environment, secrets management  |
| Software Engineer  | Scaffold implementation, initial code structure                  |
| Business Analyst   | Project vision doc, initial backlog/milestones                   |
| Technical Writer   | README, contributing guide, initial docs structure               |
| Test Engineer      | Test framework setup, initial test structure                     |
| Code Reviewer      | Review scaffold before approval                                  |

#### Flow

```mermaid
flowchart TD
    subgraph Vision
        START([Project Initiated]) --> VISION[Code Actual: Define project vision and constraints]
        VISION --> BRIEF[Architect + BA: Draft project brief]
        BRIEF --> OP1[/Code Actual: Approve brief/]
    end

    subgraph TechSelection
        OP1 --> UNCERTAIN{Tech stack unclear?}
        UNCERTAIN -->|Yes| SPIKE[[Spike/Exploration]]
        SPIKE --> TECH
        UNCERTAIN -->|No| TECH[Architect: Tech selection]
        TECH --> ADR[Architect: Write foundational ADRs]
        ADR --> OP2[/Code Actual: Approve tech decisions/]
    end

    subgraph Setup
        OP2 --> REPO[DevSecOps: Create repo, CI/CD, environments]
        REPO --> SCAFFOLD[Software Engineer: Scaffold project structure]
        SCAFFOLD --> TESTS[Test Engineer: Setup test framework]
        TESTS --> DOCS[Technical Writer: Initial documentation]
        DOCS --> REVIEW[Code Reviewer: Review scaffold]
        REVIEW --> OP3[/Code Actual: Approve setup/]
    end

    OP3 --> DONE([Ready for First Feature])
```

#### Code Actual Checkpoints

- After project brief → approve scope and vision
- After tech selection → approve technology choices
- After scaffold complete → approve readiness for feature work

#### Key Points

- **ADRs early** — Capture foundational decisions before code
- **Spike if needed** — Unknown tech requires exploration first
- **CI/CD from day one** — No "we'll add tests later"
- **Documentation structure** — Set up docs/, specs/, adrs/ early

#### Variations

- **Spike-first:** If tech is uncertain, run Spike workflow before full setup
- **Monorepo addition:** Lighter setup, inherit existing patterns
- **Forked/template:** Start from existing template, customize

---

### Audit

**When:** Periodic health check, compliance requirement, or triggered by concern
**Frequency:** Periodic

#### Audit Types

| Type          | Primary Agent                        | Focus                                  |
| ------------- | ------------------------------------ | -------------------------------------- |
| Security      | DevSecOps Engineer                   | Vulnerabilities, secrets, dependencies |
| Performance   | Software Engineer + Architect        | Bottlenecks, scaling concerns          |
| Code Quality  | Code Reviewer + Software Engineer    | Standards, smells, consistency         |
| Architecture  | Architect                            | Pattern drift, coupling, tech debt     |
| Test Health   | Test Engineer                        | Coverage, flakiness, gaps              |
| Accessibility | Technical Writer + Software Engineer | a11y compliance                        |
| Process       | Retro Analyst                        | Workflow efficiency, team patterns     |

#### Agents Involved

Varies by audit type. Core team:

- **DevSecOps Engineer** — Security, dependency scanning
- **Architect** — Architecture compliance, pattern review
- **Software Engineer** — Code quality, performance profiling
- **Test Engineer** — Test coverage, test health
- **Code Reviewer** — Standards enforcement, code smells
- **Retro Analyst** — Process audits, workflow efficiency

#### Flow

```mermaid
flowchart TD
    START([Audit Triggered]) --> SCOPE[Code Actual: Define audit scope and type]
    SCOPE --> OP1[/Code Actual: Approve audit scope/]

    subgraph Execution
        OP1 --> AUDIT[Assigned agents: Execute audit in their domains]
        AUDIT --> COLLECT[Collect findings into structured report]
        COLLECT --> PRIORITIZE[Prioritize findings: Critical/High/Medium/Low]
    end

    PRIORITIZE --> OP2[/Code Actual: Review findings, approve remediation scope/]

    subgraph Remediation
        OP2 --> ISSUES[Create Issues for approved remediation items]
        ISSUES --> EXECUTE{Execute via normal cycles}
        EXECUTE --> STORY[[Story Cycle]]
        EXECUTE --> INFRA[[Infra Cycle]]
    end

    STORY --> DONE([Audit Complete])
    INFRA --> DONE
```

#### Code Actual Checkpoints

- Before audit → approve scope
- After findings → prioritize and approve remediation

#### Key Points

- **Scoped audits** — Don't boil the ocean; focus on specific area
- **Findings ≠ action** — Code Actual decides what gets fixed
- **Feeds other workflows** — Audit findings become Issues executed via normal workflows
- **Documented** — Audit report persisted for future reference

#### Variations

- **Compliance-driven:** External requirements dictate scope
- **Pre-release:** Quick audit before major release
- **Incident-triggered:** Post-incident audit of affected area

---

### Onboarding

**When:** New context needed — new team member, returning after break, or new project
**Frequency:** Rare

#### Onboarding Types

| Type               | Scenario                            |
| ------------------ | ----------------------------------- |
| Project onboarding | Understanding a new-to-you codebase |
| Context refresh    | Returning after extended absence    |
| New team member    | Human joining the project           |

#### Agents Involved

| Agent              | Responsibility                                     |
| ------------------ | -------------------------------------------------- |
| Architect          | Architecture overview, key ADRs, system boundaries |
| Business Analyst   | Project vision, current priorities, active work    |
| DevSecOps Engineer | Environment setup, access, tooling                 |
| Technical Writer   | Documentation gaps, reading order                  |
| Software Engineer  | Code walkthrough, patterns in use                  |

#### Flow

```mermaid
flowchart TD
    START([Onboarding Needed]) --> SCOPE[Code Actual: Define onboarding scope]
    SCOPE --> READING[Technical Writer: Assess doc completeness, recommend reading order]

    subgraph Walkthrough
        READING --> ARCH[Architect: Architecture overview, key ADRs]
        ARCH --> BA[Business Analyst: Current state — milestones, priorities]
        BA --> DEVSEC[DevSecOps: Environment setup guidance]
        DEVSEC --> SE[Software Engineer: Code walkthrough of key paths]
    end

    SE --> OP1[/Code Actual: Confirm understanding, identify gaps/]
    OP1 --> GAPS{Doc gaps found?}
    GAPS -->|Yes| ISSUES[Create Issues for doc gaps]
    ISSUES --> DONE
    GAPS -->|No| DONE([Onboarding Complete])
```

#### Code Actual Checkpoints

- After walkthrough → confirm understanding, flag remaining questions

#### Key Points

- **Reading order matters** — Don't dump everything at once
- **Active state** — What's in flight, not just architecture
- **Gaps are findings** — Missing docs discovered during onboarding become Issues
- **Interactive** — Q&A throughout, not just info dump

#### Variations

- **Self-onboarding:** Code Actual exploring new project alone
- **Area-focused:** Only need to understand one subsystem
- **Handoff:** Outgoing person transferring knowledge

---

### Retrospective

**When:** Something felt off, after a significant milestone, or periodic health check
**Frequency:** Periodic

**Scope:** Analyze recent work sessions for patterns — what's working, what's not, what to change.

#### Agents Involved

| Agent         | Responsibility                                |
| ------------- | --------------------------------------------- |
| Retro Analyst | Analyze conversation patterns, produce report |
| Code Actual   | Review findings, decide on actions            |

#### Flow

```mermaid
flowchart TD
    START([Retro Triggered]) --> GATHER[Retro Analyst: Gather recent session transcripts]
    GATHER --> ANALYZE[Retro Analyst: Analyze patterns across sessions]
    ANALYZE --> REPORT[Retro Analyst: Write report]
    REPORT --> OP1[/Code Actual: Review findings and act on recommendations/]
    OP1 --> ACTIONS{Actions needed?}
    ACTIONS -->|Yes| ISSUES[Create Issues for improvements]
    ISSUES --> ARCHIVE[Archive report]
    ACTIONS -->|No| ARCHIVE
    ARCHIVE --> DONE([Retrospective Complete])
```

#### Categories Analyzed

- Code Actual prompting issues
- Agent-specific problems
- Process gaps
- Tool/permission problems
- Successful patterns to reinforce

#### Code Actual Checkpoints

- After report → review findings, decide what to act on

#### Key Points

- **Use sparingly** — When something felt off or periodically for health checks
- **Patterns over incidents** — Look for recurring themes, not one-off problems
- **Actions, not observations** — Every finding should suggest a concrete improvement
- **Archive processed reports** — Keep history but don't clutter active docs

#### Variations

- **Post-milestone:** After shipping a major feature or release
- **Targeted:** Focus on specific pain point (e.g., test quality, PR cycle time)
- **Periodic:** Regular cadence (monthly, quarterly)

---

## Definition of Done

Completion criteria by work item type. Referenced by workflows above.

### User Story

- [ ] Acceptance criteria met
- [ ] Tests pass (TDD default)
- [ ] Code review approved
- [ ] Spec updated
- [ ] Docs updated (if user-facing)

### System Story

- [ ] Implementation complete per spec/ADR
- [ ] Tests pass
- [ ] Code review approved
- [ ] ADR updated (if architectural)

### Bug Report

- [ ] Root cause identified
- [ ] Regression test added
- [ ] Code review approved
- [ ] Spec updated (if bug revealed spec gap)

### Research Request

- [ ] Findings documented
- [ ] Recommendation provided to Code Actual
- [ ] ADR drafted (if significant decision)

---

_All workflows accounted for. Refactoring delegates to Story Cycle and Maintenance._
