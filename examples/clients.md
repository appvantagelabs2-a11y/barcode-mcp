# Connecting from MCP clients

The hosted server is a remote Streamable-HTTP MCP endpoint — no install, no local process,
no API key, all tools free.

## Claude Code

```bash
claude mcp add barcode --transport http https://barcode.casuyi.com/mcp
```

Verify: `claude mcp list` → `barcode: ... ✔ connected`. Inside a session, `/mcp` shows the 4 tools.

## Claude Desktop

Settings → Connectors → **Add custom connector** → URL `https://barcode.casuyi.com/mcp`.

## Cursor / VS Code (Copilot) / Windsurf / any `mcpServers` JSON client

```json
{
  "mcpServers": {
    "barcode": {
      "type": "http",
      "url": "https://barcode.casuyi.com/mcp"
    }
  }
}
```

## Python

See [`../clients/python.py`](../clients/python.py) — zero-dependency client (stdlib `urllib`).
