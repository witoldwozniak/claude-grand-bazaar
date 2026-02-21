---
question: "What plugin-relevant knowledge exists in the Claude API Docs that is absent from Claude Code Docs?"
status: concluded
started: 2026-02-20
concluded: 2026-02-21
stale_after: 180
tags: [documentation, api-docs, content-gap]
---

# What plugin-relevant knowledge exists in the Claude API Docs that is absent from Claude Code Docs?

## Motivation

The Claude Developer Guide (`platform.claude.com`) frequently surfaces during research on Claude and Claude Code features. Some content overlaps with the Claude Code Docs we already fetch and reference — topics like tool use, system prompts, and streaming appear in both. However, the API Docs may contain unique knowledge relevant to plugin development: detailed model behavior documentation, advanced prompting techniques, or API-level capabilities that affect how Skills, Subagents, or Connectors should be designed.

**The decision this informs:** Should we build a second fetch script (mirroring `scripts/fetch_claude_code_docs.py`) to maintain a local copy of API Docs, reference them directly in Skills by URL, or neither? We need to quantify the gap before committing to additional maintenance burden.

Triggered by [Issue #1](https://github.com/witoldwozniak/claude-grand-bazaar/issues/1).

## Scope & Constraints

**In scope:**
- Surveying the Claude API Docs (`platform.claude.com`) for content absent from the Claude Code Docs (`code.claude.com/docs`)
- Assessing which gaps are relevant to the five plugin primitives (Skills, Hooks, Subagents, Connectors, LSP Servers)
- Recommending whether to build an automated fetcher, reference by URL, or ignore

**Out of scope:**
- Building the fetch script itself (that would follow from a "build it" recommendation)
- Evaluating the quality or accuracy of either docs source
- Comparing with third-party Claude documentation or tutorials

## Method

1. **Claude Code Docs baseline:** Fetched all 56 pages using `scripts/fetch_claude_code_docs.py` into `docs/claude-code-docs/`. These serve as the "already available" baseline.

2. **API Docs survey:** Used WebFetch to survey key sections of `platform.claude.com`:
   - [Features overview](https://platform.claude.com/docs/en/features) — catalog of API capabilities
   - [Tool use](https://platform.claude.com/docs/en/build-with-claude/tool-use/overview) — tool schemas, parallel execution, pricing
   - [Agent Skills](https://platform.claude.com/docs/en/build-with-claude/agentic-skills) — VM architecture, pre-built Skills
   - [MCP connector](https://platform.claude.com/docs/en/build-with-claude/mcp-connector) — API-level MCP integration
   - [Agent SDK](https://platform.claude.com/docs/en/build-with-claude/agent-sdk) — Python/TypeScript SDK reference
   - [Prompt engineering](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview) — 8-page prompting guide
   - [Models overview](https://platform.claude.com/docs/en/about-claude/models/all-models) — per-model comparison data

3. **Accessibility check:** ~~Verified that `platform.claude.com` has no `llms.txt` endpoint and no publicly accessible `sitemap.xml`. This means an automated fetcher would need to scrape the navigation structure — materially harder and more brittle than the Claude Code Docs fetcher (which uses `llms.txt`).~~ **Correction (2026-02-21):** This was wrong — `platform.claude.com` does expose `llms.txt`. See [Addendum: 2026-02-21](#addendum-2026-02-21) below.

4. **Gap analysis:** For each API Docs topic, checked whether equivalent content exists in the Claude Code Docs and assessed the nature of any gap.

## Findings

### Content Gap Analysis

The following table maps API Docs topics against Claude Code Docs equivalents, identifying where gaps exist:

| Category | API Docs Topics | Claude Code Docs Equivalent | Gap? |
|----------|----------------|---------------------------|------|
| Prompt engineering | 8-page guide (clear/direct, multishot, CoT, XML tags, system prompts, chaining, long context) | `best-practices.md` covers some basics | **Yes — significant depth** |
| Model capabilities | Detailed per-model comparison, pricing, context windows, training cutoffs | `model-config.md` (basic configuration) | **Yes — reference data** |
| Tool use (API-level) | Full tool schema, client vs server tools, parallel tool use, pricing | `how-claude-code-works.md` (internal view) | **Partial — different audience** |
| Agent Skills (API) | VM architecture, progressive disclosure, pre-built Skills (PPTX/XLSX/DOCX/PDF), API endpoints | `skills.md` (Claude Code perspective) | **Yes — complementary** |
| Agent SDK | Full Python/TypeScript SDK reference, hooks, subagents, sessions, permissions | `headless.md`, `sub-agents.md` (consumer view) | **Yes — builder perspective** |
| MCP connector | API-level MCP integration, OAuth, toolset config | `mcp.md` (Claude Code MCP config) | **Yes — different integration point** |
| Extended thinking | Detailed API params, budget tokens, streaming behavior | Not covered in Code Docs | **Yes — API-only** |
| Prompt caching | 5min/1hr caching tiers, automatic caching, token counting | Not covered in Code Docs | **Yes — API-only** |
| Batch processing | Async batch API, 50% cost savings | Not covered in Code Docs | **Yes — API-only** |
| Computer use | Client-side tool for UI automation | Not covered in Code Docs | **Yes — API-only** |
| Citations / Search results | Source attribution for RAG workflows | Not covered in Code Docs | **Yes — API-only** |
| Structured outputs | JSON schema conformance, strict tool use | Not covered in Code Docs | **Yes — API-only** |
| Context management | Compaction, context editing, token counting | Not covered in Code Docs (handled internally) | **Partial — internal vs explicit** |
| Files API | Upload and manage persistent files | Not covered in Code Docs | **Yes — API-only** |
| Evaluation / Testing | Define success criteria, develop test suites | Not covered in Code Docs | **Yes — API-only** |

### Plugin Relevance Assessment

Not all API-only content matters equally for plugin development. This table assesses relevance to each of the five primitives:

| API-only Topic | Skills | Hooks | Subagents | Connectors | LSP | Overall Relevance |
|---------------|--------|-------|-----------|------------|-----|-------------------|
| Prompt engineering | **High** | Low | **High** | Low | Low | **Directly relevant** — Skills and Subagents benefit from advanced prompting techniques |
| Model capabilities | Medium | Low | Medium | Low | Low | Reference data — useful for model selection in agent frontmatter |
| Agent Skills (API) | **High** | Low | Medium | Low | Low | **Directly relevant** — API-level Skills architecture informs plugin Skills design |
| Agent SDK | Medium | Medium | **High** | Medium | Low | **Directly relevant** — the programmatic interface to all five primitives |
| Extended thinking | Medium | Low | Medium | Low | Low | Tangentially relevant — useful for complex reasoning subagents |
| Prompt caching | Low | Low | Low | Medium | Low | Tangentially relevant — cost optimization for Connector-heavy workflows |
| Computer use | Low | Low | Medium | Low | Low | Tangentially relevant — niche use case for UI-testing subagents |
| Structured outputs | Medium | Low | Medium | **High** | Low | **Directly relevant** — Connectors producing structured data benefit significantly |
| MCP connector | Low | Low | Low | **High** | Low | **Directly relevant** — API-level MCP integration complements Claude Code MCP config |
| Batch processing | Low | Low | Low | Medium | Low | Tangentially relevant — cost optimization for bulk operations |
| Citations / Search | Low | Low | Low | Medium | Low | Tangentially relevant — RAG patterns for knowledge-heavy Skills |
| Files API | Low | Low | Low | Medium | Low | Tangentially relevant — file management for document-processing plugins |
| Evaluation / Testing | Medium | Medium | Medium | Low | Low | Tangentially relevant — testing strategies for plugin quality |

### Key Observations

1. **Prompt engineering** is the largest gap by volume and the most directly useful. The API Docs contain an 8-page guide covering techniques (chain-of-thought, multishot examples, XML tag structuring) that are directly applicable to writing effective Skills and Subagent prompts. The Claude Code Docs cover `best-practices.md` at a much higher level.

2. **Agent SDK** documentation describes the programmatic interface to hooks, subagents, sessions, and permissions — exactly the five primitives this marketplace is built around. The Claude Code Docs describe these from a consumer perspective; the API Docs describe them from a builder perspective.

3. **Structured outputs and MCP connector** documentation is highly relevant to Connectors (the fourth primitive). The API Docs describe JSON schema conformance and API-level MCP integration that complements the Claude Code Docs' configuration-focused MCP coverage.

4. **API-only features** (extended thinking, prompt caching, batch processing, computer use, citations, Files API) are tangentially relevant — they describe capabilities that could be leveraged by plugins but are not core to plugin *authoring*.

## Limitations

- **Survey, not exhaustive audit.** The API Docs were surveyed via representative pages, not read page-by-page. Minor topics may have been missed.
- **Point-in-time snapshot.** Both docs sources are actively maintained. Gaps identified today may close (or widen) as either source evolves. The `stale_after: 180` frontmatter field reflects this.
- **~~`llms.txt` absence was verified indirectly.~~ Confirmed wrong (2026-02-21).** The original check failed to find `llms.txt` at `platform.claude.com`. Subsequent verification confirmed it exists at `https://platform.claude.com/llms.txt` (~725 English pages) and `https://platform.claude.com/llms-full.txt` (>10 MB full content dump). The original indirect verification method was insufficient.
- **Relevance assessment is subjective.** The High/Medium/Low ratings reflect judgment about current plugin development needs, not measured impact.

## Addendum: 2026-02-21

The original research concluded that `platform.claude.com` had no `llms.txt` endpoint, making an automated fetcher infeasible. **This was incorrect.**

Subsequent verification confirmed two machine-readable endpoints:

- **`https://platform.claude.com/llms.txt`** — structured index with ~725 English documentation pages, using the format `- [Title](URL) - Description` (description is optional on some entries)
- **`https://platform.claude.com/llms-full.txt`** — full content dump (>10 MB), containing the complete text of all documentation pages

This discovery reverses the implementation recommendation from Conclusion #2. The `llms.txt` index uses a slightly different format than the Claude Code Docs version (`- [Title](URL) - Description` vs `- [Title](URL): Description`), but is equally parseable. The index contains pages in multiple languages; only `/en/` entries are relevant for this project.

**Impact on conclusions:**
- Conclusion #2 changes from "Do NOT build" to "Build an automated fetcher" — the same `llms.txt`-based approach used by `scripts/fetch_claude_code_docs.py` is now viable
- Conclusion #3 remains valid (URL references work) but is supplemented by the option of local copies for offline/fast access
- The gap analysis and relevance assessments in the Findings section remain accurate and unchanged

## Conclusions

1. **The API Docs contain substantial unique content** not present in the Claude Code Docs. The most plugin-relevant gaps are: prompt engineering depth, Agent SDK builder reference, structured outputs, and MCP connector details.

2. **~~Do NOT build an automated fetch script.~~ Build an automated fetcher (revised 2026-02-21).** The `platform.claude.com` site exposes `llms.txt` with ~725 English pages, making a fetcher feasible using the same approach as `scripts/fetch_claude_code_docs.py`. See [Addendum: 2026-02-21](#addendum-2026-02-21).

3. **Reference API Docs by URL in relevant Skills, supplemented by local copies.** When a Skill teaches prompt writing, link to the API Docs prompt engineering guide. When a Skill covers Connectors, link to the MCP connector and structured outputs docs. URL references remain the primary mechanism, but `scripts/fetch_api_docs.py` can now fetch local copies for offline access and faster lookups (revised 2026-02-21).

4. **The Agent SDK docs are the single most plugin-relevant API-only resource.** They describe the programmatic interface to all five primitives from a builder perspective — exactly the audience Grand Bazaar serves. These should be linked prominently in the plugin-authoring plugin.
