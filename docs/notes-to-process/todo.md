---
title: TODO
description: "Development backlog and brainstormed plugin ideas."
navigation: false
---

# TODO

## Backlog

### dev-team

- [ ] definition of done (skill + hook)
- [ ] code conventions and standards (skill)
- [ ] git conventions (skill)
- [ ] tdd (skill)
- [ ] debugging (skill — frameworks, workflows)
- [ ] code review (skill)
- [ ] docs review (skill)

### New plugin candidates

- [ ] Documentation Authoring
- [ ] Claude Research
- [ ] Frontend Development
- [ ] Backend Development
- [ ] Database Development
- [ ] Claude Prose
- [ ] CLI Password Manager integration for storing secrets etc.

### CI pipeline

- [ ] Add skill validation (`quick_validate.py`) to CI once the script is ready
- [ ] Add agent validation (`validate_subagent.py`) to CI once the script is ready
- [ ] External link health checks (scheduled weekly workflow)
- [ ] Conventional commits linting via `amannn/action-semantic-pull-request` on PR titles

## Research

- brainstorming — are there frameworks?
- swarm — spawning multiple subagents in parallel as default strategy
- gathering/refining requirements — any frameworks?
- dynamic programming / DSA skill — is this useful?

## Brainstormed Skills & Hooks

From session 2025-02-04. Tagged by target plugin.

### Epistemic Discipline / Reasoning Hygiene

**Skills** `[new plugin: reasoning-tools]`

- show_reasoning — Toulmin structure (claim, grounds, warrant, qualifier, rebuttal)
- assume_failure — Pre-mortem: assume the task failed, explain why (Klein)
- find_counterexample — Actively try to disprove own claim (Popper/Falsificationism)
- competing_hypotheses — Evaluate evidence against multiple hypotheses (ACH/Heuer)
- failure_modes — Systematic failure analysis: how could each component fail? (FMEA)
- reversal_cost — Estimate how hard a decision is to undo; prefer reversible options

**Hooks** `[dev-team or standalone]`

- prove_or_flag — PreToolUse/Stop: verify claim with evidence or flag as unverified
- capability_check — PreToolUse: verify required tools exist before attempting
- stuck_detection — Stop: detect circular behavior, repeated failures
- definition_of_done — Stop (exit code 2): block completion until checklist passes
- calibration_tracking — PostToolUse: log confidence vs actual outcomes (telemetry)

### Debugging

**Skill: debugging** `[dev-team]` — Loaded on request, routes to sub-resources

Steps: reproduce → isolate → hypothesize → test_hypothesis → verify_fix → regression_check

Conditional resources:

- capability_check.md (before starting), reproduction_strategies.md (if reproduction fails)
- bisection.md (if isolation is difficult), stuck_detection.md (if 3+ attempts fail)
- show_reasoning.md (before proposing fix), assume_failure.md (after proposing fix)

### Agent Self-Management

**Skills** `[dev-team or standalone]`

- escalation — Recognize when to stop and ask for guidance; summarize what was tried
- scope_awareness — Detect task growing beyond original bounds; surface to user
- context_triage — Before starting: do I have enough context? What's missing?
- graceful_degradation — "I can do A, B, C without tool X. I cannot do D. Proceed?"

## References

### Dependencies

- https://github.com/microsoft/markitdown
- https://github.com/cli/cli

### Competitor / inspiration repos

- https://github.com/softaworks/agent-toolkit
- https://github.com/antfu/skills
- https://github.com/hashicorp/agent-skills
- https://github.com/vercel-labs/skills
- https://github.com/anthropics/claude-plugins-official
- https://github.com/anthropics/skills
- https://github.com/anthropics/claude-code
- https://github.com/openai/skills
- https://github.com/avifenesh/awesome-slash
- https://github.com/jarrodwatts/claude-hud

### Frameworks (potential skill content)

- Toulmin Model, Falsificationism (Popper), ACH (Heuer), Pre-mortem (Klein)
- FMEA, Calibration (Tetlock), Polya, Means-ends analysis
- Working backwards, 5 Whys, Scientific method, Bisection / Wolf fence

### Architecture notes

- Skills: reasoning, generation, context-dependent decisions
- Hooks: enforcement, gates, deterministic checks
- Meta-skill pattern: broad SKILL.md routes to resources/ mid-task
- Open question: do agents load skills mid-task from metadata alone? Needs testing
