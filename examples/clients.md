# Connecting from MCP clients

The hosted server is a remote Streamable-HTTP MCP endpoint — no install, no local process,
no API key for free tools.

## Claude Code

```bash
claude mcp add barcode --transport http https://mcp.casuyi.com/mcp
```

With a trial key (extra header, forwarded on every request):

```bash
claude mcp add barcode --transport http https://mcp.casuyi.com/mcp \
  --header "X-API-Key: ***"
```

Verify: `claude mcp list` → `barcode: ... ✔ connected`. Inside a session, `/mcp` shows the 4 tools.

## Claude Desktop

Settings → Connectors → **Add custom connector** → URL `https://mcp.casuyi.com/mcp`.
(Desktop cannot send custom headers — use x402 for paid tools there.)

## Cursor / VS Code (Copilot) / Windsurf / any `mcpServers` JSON client

```json
{
  "mcpServers": {
    "barcode": {
      "type": "http",
      "url": "https://mcp.casuyi.com/mcp",
      "headers": { "X-API-Key": "<your-trial-key>" }
    }
  }
}
```

Drop `headers` if you only use `list_formats` / `validate_gtin` or pay via x402.

## Python

See [`../clients/python.py`](../clients/python.py) — zero-dependency client (stdlib `urllib`),
including trial-key and SSE handling.
