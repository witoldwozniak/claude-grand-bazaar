# Claude Code vs Cowork: plugin systems and Grand Bazaar fit

**Claude Code is the clear platform for building a curated plugin marketplace like Grand Bazaar.** It supports all five primitives the project requires (Skills, Hooks, Agents, MCP servers, LSP servers), has a mature GitHub-based marketplace system with `plugin.json` manifests and `marketplace.json` catalogs, and a thriving community ecosystem with dozens of existing marketplaces and thousands of plugins. Cowork, launched January 2026, shares the same plugin format but omits hooks and LSP servers from its plugin model — making it a viable secondary consumption target but not the primary development platform.

This matters because the plugin architecture decisions are now locked in: Claude Code's plugin system hit public beta in October 2025, Cowork adopted a compatible subset in January 2026, and the shared `claude.com/plugins` directory already serves both products. Anyone building a marketplace today is building on a foundation that reaches both audiences.

---

## Claude Code's plugin architecture is a full-featured packaging system

Claude Code plugins are **modular bundles** that combine up to six distinct primitive types into a single installable unit. The system, released as public beta on October 9, 2025, uses a straightforward file-based architecture:

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Required manifest
├── commands/                # Slash commands (user-invoked)
├── agents/                  # Subagents (delegated specialists)
├── skills/                  # SKILL.md files (model-invoked)
│   └── my-skill/
│       └── SKILL.md
├── hooks/                   # Lifecycle event handlers
│   └── hooks.json
├── .mcp.json                # MCP server connections
├── .lsp.json                # LSP server configuration
└── README.md
```

The **`plugin.json` manifest** declares metadata and component locations — name (kebab-case), version (semver), description, author, license, and paths to commands, agents, and inline MCP server definitions. A `${CLAUDE_PLUGIN_ROOT}` variable enables plugin-relative path references. The **`marketplace.json` catalog** lives in a Git repository and lists available plugins with names, source paths, and descriptions. Users add marketplaces via `/plugin marketplace add user/repo` and install plugins via `/plugin install plugin-name@marketplace-name`.

The **six plugin primitives** each serve distinct roles. **Skills** are markdown files with YAML frontmatter that Claude automatically invokes based on task context — they encode domain knowledge and best practices via progressive disclosure (only name/description loaded initially, full content on-demand). Agent Skills became an open standard in December 2025 at agentskills.io, adopted by both OpenAI's Codex CLI and ChatGPT. **Hooks** are event-driven shell commands, LLM prompts, or subagent invocations triggered at lifecycle points — `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `SessionStart`, `Stop`, and seven others. They support matchers (exact string, regex, wildcards) for targeted tool filtering and can modify, block, or approve tool executions via JSON output on exit code 0. **Subagents** are specialized AI personalities with custom system prompts, configurable tool access, and optional model overrides (Sonnet, Opus, Haiku). **MCP servers** connect to external services via stdio, HTTP, or SSE transports with OAuth 2.0 support. **Custom slash commands** are markdown files where the filename becomes the command name, with `$ARGUMENTS` and positional `$1`, `$2` variables. **LSP servers** provide real-time code intelligence (type checking, go-to-definition) configured in `.lsp.json`.

---

## Cowork's extensibility is a compatible subset focused on knowledge workers

Claude Cowork launched January 12, 2026 as a research preview — an **agentic desktop AI** that runs inside the Claude Desktop app as a tab alongside Chat and Code. It executes tasks autonomously against user-designated folders within an Apple VM sandbox (VZVirtualMachine on macOS). Plugin support arrived January 30, 2026 with **11 open-source plugins** covering Productivity, Sales, Finance, Legal, Marketing, Data Analysis, and more, hosted at `anthropics/knowledge-work-plugins` on GitHub.

Cowork plugins use the **same file-based format** as Claude Code plugins — `plugin.json` manifests, the same directory structure, and the same marketplace system. However, the plugin primitives Cowork emphasizes are a **four-component subset**: Skills, Connectors (MCP servers), Slash Commands, and Sub-agents. **Hooks are not a supported Cowork plugin component** — they remain a Claude Code-specific mechanism tied to the terminal lifecycle. **LSP servers are also absent** from Cowork's extensibility model, which makes sense given Cowork targets non-technical knowledge work rather than code editing.

Cowork adds unique extensibility features absent from Claude Code. Its **Connectors directory** (Settings → Connectors → Browse) offers a browsable catalog of hundreds of pre-configured MCP integrations — Salesforce, HubSpot, Slack, Notion, Jira, Linear, Microsoft 365, and more — with two categories: web connectors (browser-based APIs) and desktop extensions (local, deeper system access). **Global and folder-specific persistent instructions** let users configure preferred tone, formatting, and role context without plugins. The **Plugin Create meta-plugin** enables building custom plugins entirely through the GUI, with no CLI or coding required. Plugins can also be installed by uploading ZIP files directly into the Cowork interface.

The `claude.com/plugins` directory serves both products, with plugins filterable by "Cowork" or "Claude Code" target. The shared architecture means **any plugin containing only Skills, MCP servers, Slash Commands, and Subagents works on both platforms**. Plugins containing Hooks or LSP servers are Claude Code-only.

---

## Development workflows diverge sharply between the two platforms

**Claude Code plugin development** follows a CLI-native workflow. Developers create the directory structure, write `plugin.json` and component files, set up a local marketplace (a directory with `marketplace.json` pointing to the plugin), add it via `/plugin marketplace add ./dev-marketplace`, and iterate through uninstall-modify-reinstall cycles. Anthropic's official **`plugin-dev` meta-plugin** provides an 8-phase guided workflow for building plugins, with 7 expert skills covering architecture, component creation, testing, and documentation. Testing is hands-on: developers run plugins in Claude Code sessions, verify hook behavior via exit codes and JSON output, and validate MCP server connections. Distribution is Git-native — push a marketplace repo to GitHub and users add it with a single command.

**Cowork plugin development** is more accessible but less powerful. The Plugin Create meta-plugin inside Cowork walks users through building plugins via natural language conversation — describing what the plugin should do, then having Claude generate the skills, commands, and MCP configurations. No terminal, no JSON editing, no Git required. This lowers the barrier dramatically for knowledge workers but limits fine-grained control over hooks, LSP integration, and advanced lifecycle behaviors. For developers comfortable with both tools, the recommended workflow is to **develop and test in Claude Code** (where all primitives are available and debugging is direct) then **verify compatibility in Cowork** for the subset of components that work cross-platform.

Anthropic provides official example plugins at `anthropics/claude-code` on GitHub — including `feature-dev`, `code-review`, `pr-review-toolkit`, `security-guidance`, and `frontend-design` — plus the 11 knowledge-work plugins at `anthropics/knowledge-work-plugins`. The community has rapidly built an extensive ecosystem: **`jeremylongshore/claude-code-plugins-plus-skills`** (270+ plugins, 1,537 agent skills), **`affaan-m/everything-claude-code`** (Cerebral Valley hackathon winner, includes AgentShield security scanner), and marketplace directories like claudecodemarketplace.com and claudepluginhub.com (9,000+ plugins).

---

## Limitations reveal each platform's boundaries

**Claude Code's plugin system** has meaningful constraints. Context window consumption is a serious issue — community reports indicate that **even five default Anthropic plugins can consume 91% of the context window**, leaving little room for actual work. The skill description budget scales at just 2% of context, with a 16,000-character fallback. Hook timeouts default to 60 seconds (configurable up to 10 minutes in v2.1.3+), which constrains complex validation workflows. Security is a genuine concern: PromptArmor published research demonstrating how **malicious marketplace plugins can hijack Claude Code** through hooks that bypass human-in-the-loop approval, enabling data exfiltration via prompt injection and curl commands. There is no built-in monetization mechanism — all plugins are free and open-source. MCP output is capped at 25,000 tokens by default. And the marketplace system lacks automated quality assurance or dependency management.

**Cowork's limitations** are more fundamental. As a **research preview**, it lacks session memory persistence, sharing capabilities, and is desktop-only (though Windows support arrived February 10, 2026). The absence of hooks means plugins cannot implement automated guardrails, pre-flight checks, or tool execution filtering — the exact capabilities Grand Bazaar's "Hooks (automated guardrails)" primitive requires. No LSP support means no real-time code intelligence plugins. The sandboxed VM environment, while safer, restricts the kinds of system-level integrations possible. Enterprise features like organization-wide private marketplaces are announced but not shipped. And Cowork's Opus 4.6-only model coupling means no model flexibility for cost-sensitive plugin operations (Claude Code plugins can specify Haiku for lightweight subagents).

---

## Grand Bazaar belongs on Claude Code, with Cowork as a secondary target

The Grand Bazaar's architecture — **five primitives (Skills, Hooks, Agents, MCP servers, LSP servers), a 9-stage Plugin Development Life Cycle, and GitHub-based distribution via marketplace.json** — maps directly onto Claude Code's plugin system. Every primitive in Grand Bazaar has a first-class corresponding mechanism in Claude Code. The GitHub-based marketplace model with `marketplace.json` catalogs is exactly how Claude Code's marketplace system works. The development workflow (create → test → distribute via Git) aligns with Claude Code's CLI-native iteration cycle.

**Cowork cannot serve as the primary development platform** for three decisive reasons. First, it lacks hooks entirely — Grand Bazaar's "Hooks (automated guardrails)" primitive has no Cowork equivalent. Second, LSP servers are absent from Cowork's extensibility model. Third, the GUI-first development experience trades the precise control needed for a curated, research-grounded marketplace for accessibility. A marketplace built on "opinionated, research-grounded plugins" requires the kind of fine-grained lifecycle control that only Claude Code provides.

However, **Cowork is a viable secondary consumption target** for a meaningful subset of Grand Bazaar plugins. Any plugin built purely from Skills, Agents, MCP servers, and Slash Commands will work on Cowork without modification — the plugin format is shared, and `claude.com/plugins` already serves both platforms. Grand Bazaar could tag plugins as "Cowork-compatible" when they don't depend on hooks or LSP servers, expanding its reach to non-developer knowledge workers. The 11 official Cowork plugins demonstrate that sophisticated domain-specific plugin bundles (Sales, Finance, Legal) work well in the Cowork model when they rely on Skills + Connectors + Commands + Subagents.

The practical recommendation: **build Grand Bazaar targeting Claude Code's full six-primitive plugin system**, design a compatibility matrix that flags which plugins work on Cowork (those without hooks or LSP dependencies), and structure the 9-stage Plugin Development Life Cycle around Claude Code's `plugin-dev` workflow while adding a Cowork validation stage. The shared `marketplace.json` format means a single GitHub repository serves both audiences with no format translation needed.

## Conclusion

Claude Code and Cowork represent two expressions of the same underlying Claude Agent SDK, with Claude Code offering the full extensibility surface (six primitives, CLI workflow, lifecycle hooks, LSP support) and Cowork providing a GUI-accessible subset optimized for knowledge workers (four primitives, no hooks, no LSP). The plugin format compatibility between them is a strategic advantage for any marketplace builder: write once in Claude Code's full-featured environment, distribute to both audiences via the same `marketplace.json` catalog. Grand Bazaar's hook-centric guardrails and LSP-based code intelligence primitives make Claude Code the only viable development platform — but the ~30-40% of plugins that don't depend on those primitives can reach Cowork's growing knowledge-worker audience without additional engineering effort. The ecosystem is early (plugin system is still in beta) but moving fast, with thousands of community plugins already published and Anthropic actively expanding both platforms' capabilities.