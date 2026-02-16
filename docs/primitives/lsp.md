---
title: LSP Servers
description: "LSP servers perceive. Real-time code intelligence with diagnostics, type awareness, and navigation."
---

# LSP Servers

> LSP servers perceive. They provide real-time code intelligence — diagnostics after every edit, type awareness, navigation through definitions and references.

> **Platform note:** LSP servers are a Claude Code feature. Cowork does not support LSP integration. Plugins that rely on LSP for real-time code intelligence are Claude Code-only.

## What It Is

LSP (Language Server Protocol) integrations give Claude live awareness of code state. Where skills carry static knowledge about how a language works, LSP servers see the living code as it changes — surfacing type errors immediately after edits, providing navigation through definitions and references, and offering hover information for code symbols.

Claude Code acts as the LSP client. Language servers run as external processes providing continuous intelligence.

## When to Use (and When Not To)

| Situation | Use | Reason |
|-----------|-----|--------|
| Real-time diagnostics (errors, warnings) | **LSP server** | Instant feedback after every edit |
| Code navigation (go-to-definition, references) | **LSP server** | Live awareness of code structure |
| Teaching Claude about a language's idioms | Skill | Static knowledge, not real-time analysis |
| Enforcing code style rules | Hook (PostToolUse) | Deterministic enforcement, not perception |
| Connecting to external APIs | MCP server | LSP is for code intelligence, MCP is for external connections |

LSP is perception — making Claude aware of what's happening in the code right now. If you want to enforce rules based on that perception, pair it with hooks.

## How It Works

The Language Server Protocol defines a client-server architecture where:

1. **The language server** analyzes code and provides intelligence (diagnostics, completions, navigation)
2. **Claude Code** acts as the client, receiving and acting on that intelligence
3. **Communication** happens over stdio or other transports defined by the protocol

### What LSP Provides to Claude

- **Instant diagnostics** — errors and warnings after each edit, without running a build
- **Code navigation** — go to definition, find all references, hover for type information
- **Language awareness** — type information and documentation for code symbols
- **Workspace intelligence** — understanding of project structure and dependencies

## Configuration

### Plugin-Bundled LSP Servers

Plugins can bundle LSP servers using `.lsp.json` in the plugin root or the `lspServers` field in `plugin.json`.

```json
{
  "lspServers": {
    "my-language": {
      "command": "my-language-server",
      "args": ["--stdio"],
      "extensionToLanguage": {
        ".mylang": "mylanguage"
      }
    }
  }
}
```

**Key configuration fields:**

| Field | Required | Description |
|-------|----------|-------------|
| `command` | Yes | Language server binary to execute |
| `extensionToLanguage` | Yes | Maps file extensions to language IDs |
| `args` | No | Arguments passed to the server |
| `transport` | No | Communication transport (default: stdio) |
| `env` | No | Environment variables for the server process |
| `initializationOptions` | No | Options passed during LSP initialization |
| `settings` | No | Server-specific configuration |
| `maxRestarts` | No | Maximum restart attempts on crash |

### Official LSP Plugins

For common languages, use the pre-built official LSP plugins rather than creating custom ones:

| Plugin | Language | Server |
|--------|----------|--------|
| `pyright-lsp` | Python | Pyright |
| `typescript-lsp` | TypeScript/JavaScript | TypeScript language server |
| `rust-lsp` | Rust | rust-analyzer |

Users must install the language server binary separately — plugins don't bundle it.

## Patterns

*To be expanded as we build plugins that use LSP servers.*

### Custom Language Support

When the official marketplace doesn't cover your language, create a custom `.lsp.json` pointing to a language server binary. The binary must be installed separately — document the install command in the plugin README.

## Our Opinions

- **Prefer official LSP plugins for common languages.** Only create custom LSP plugins for languages not already covered by the marketplace.
- **Don't bundle the language server binary.** Document the install command and trust the user to install it. Binaries are platform-specific and version-sensitive.
- **LSP is perception, not enforcement.** LSP makes Claude aware of errors. If you want to block actions based on diagnostics, pair LSP with hooks. LSP sees; hooks act.
- **Keep LSP configuration minimal.** Let the language server's defaults work. Only override settings when you have a specific reason.

## References

- [Doctrine](../doctrine.md) § The Six Primitives
- Official Claude Code plugins reference: LSP servers section
- Official Claude Code plugins documentation: `code.claude.com/docs/plugins` (fetch locally via `scripts/fetch-claude-code-docs.py`)
- Language Server Protocol specification: `microsoft.github.io/language-server-protocol`
