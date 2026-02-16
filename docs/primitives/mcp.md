---
title: MCP Servers
description: "MCP servers connect. They provide external reach to tools, APIs, and systems outside Claude's native capabilities."
---

# MCP Servers

> MCP servers connect. They provide external reach — connections to tools, APIs, and systems outside Claude's native capabilities.

## What It Is

MCP (Model Context Protocol) servers extend Claude's toolkit with external integrations. They expose tools that Claude can invoke like native tools, but connect to databases, APIs, third-party services, and other systems outside Claude's native capabilities. An MCP server turns an external API into a Claude tool.

MCP tools appear in Claude's toolkit with the naming convention `mcp__<server>__<tool>` — for example, `mcp__github__search_repositories` or `mcp__memory__create_entities`.

## When to Use (and When Not To)

| Situation | Use | Reason |
|-----------|-----|--------|
| Persistent connection to an external service | **MCP server** | Exposes service as native tools |
| One-off API call | Bash script or hook | Simpler, no server to maintain |
| Read from a database during tasks | **MCP server** | Structured access, consistent interface |
| Enforce rules about external operations | Hook targeting MCP tools | Hooks can block MCP tool invocations via matchers |
| Real-time code analysis | LSP server | LSP is for code intelligence, MCP is for external connections |

MCP servers are for persistent, tool-like connections. If a simple `curl` in a Bash command does the job, you don't need an MCP server.

## How It Works

An MCP server runs as a process that Claude Code communicates with via the Model Context Protocol. The server exposes tools (with names, descriptions, and input schemas) that Claude can discover and invoke. When Claude calls an MCP tool, Claude Code routes the request to the server, which handles the external communication and returns results.

The protocol supports multiple transport modes (stdio, HTTP) and handles tool discovery, invocation, and result marshalling.

## Configuration

### Plugin-Bundled MCP Servers

Plugins can bundle MCP servers using `.mcp.json` in the plugin root or the `mcpServers` field in `plugin.json`. Plugin MCP servers start automatically when the plugin is enabled.

Use `${CLAUDE_PLUGIN_ROOT}` for script paths to ensure portability:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/servers/my-server.js"],
      "env": {
        "API_BASE": "https://api.example.com"
      }
    }
  }
}
```

### Project and User MCP Servers

MCP servers can also be configured at project level (`.claude/settings.json`) or user level (`~/.claude/settings.json`) using the `mcpServers` key.

## Integration with Other Primitives

### Hooks Targeting MCP Tools

Hooks can target MCP tools using matchers with the `mcp__<server>__<tool>` naming pattern:

- `mcp__memory__.*` — matches all tools from the memory server
- `mcp__.*__write.*` — matches write operations across any MCP server

This enables security blocking, logging, and monitoring of external operations.

### Agents with MCP Access

Agents can specify MCP servers in their frontmatter via the `mcpServers` field. This gives the agent access to external tools within its isolated context. Note: MCP tools are unavailable in background subagents.

## Patterns

*To be expanded as we build plugins that use MCP servers.*

### API Client Server

Wraps an external API (GitHub, Jira, Slack) as a set of MCP tools. Handles authentication, rate limiting, and error formatting so Claude gets clean tool interfaces.

### Database Access Server

Provides structured read/write access to a database. Useful for plugins that need to query or update persistent state.

## Our Opinions

- **MCP servers should be self-contained.** Don't assume the user has specific services running unless the plugin explicitly documents the setup.
- **Use `${CLAUDE_PLUGIN_ROOT}` for all paths.** Never hardcode absolute paths in MCP server configurations.
- **Never bundle secrets.** If an MCP server needs credentials, document the setup clearly. Credentials belong in environment variables or user configuration, not in the plugin.
- **Prefer existing community MCP servers** over building custom ones when the functionality matches. Don't reinvent what exists.
- **Document the external dependency.** If a plugin bundles an MCP server, make it clear what external service it connects to, what permissions it needs, and what happens when the service is unavailable.

## References

- [Doctrine](../doctrine.md) § The Six Primitives
- Official Claude Code plugins reference: MCP servers section
- Official Claude Code MCP documentation: `code.claude.com/docs/mcp` (fetch locally via `scripts/fetch-claude-code-docs.py`)
- Model Context Protocol specification: `modelcontextprotocol.io`
