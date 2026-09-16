# barcode — barcode & QR tools MCP server

Barcode/QR decode, render and product-code (GTIN) validation for AI agents over the
[Model Context Protocol](https://modelcontextprotocol.io). One WASM engine
(zxing-cpp via [`zxing-wasm`](https://www.npmjs.com/package/zxing-wasm)) does both render and
decode — fully headless.

**Use the hosted endpoint — no install, no local process:**

```
https://mcp.casuyi.com/mcp
```

MCP `2026-07-28` (2025-era clients supported too), stateless Streamable HTTP, works with
Claude Code, Claude Desktop, Cursor, VS Code, and any MCP client.

## Tools

| Tool | Price | What it does |
|---|---|---|
| `list_formats()` | **free** | Table of supported symbologies and their capabilities |
| `validate_gtin(code)` | **free** | Product-code rules: length + mod-10 checksum → `{valid, type, normalized}` (EAN-13/8, UPC-A/E, ITF…) |
| `render_barcode(text, format, scale?)` | paid | Render any supported symbology as base64 PNG. Every render is decoded back before returning — failures come with a `warning`, never silently |
| `decode_barcode(image_base64, formats?)` | paid | Detect + decode all barcodes in an image → `[{format, text}]` — QR, Aztec, DataMatrix, Code128/39/93, EAN-13/8, UPC-A/E, ITF, PDF417, Codabar |

## Connect

**Claude Code**

```bash
claude mcp add barcode --transport http https://mcp.casuyi.com/mcp
```

**Claude Desktop** — Settings → Connectors → *Add custom connector* → URL above.

**Cursor / VS Code (Copilot) / Windsurf / any `mcpServers` JSON client**

```json
{
  "mcpServers": {
    "barcode": { "type": "http", "url": "https://mcp.casuyi.com/mcp" }
  }
}
```

## Pricing — two ways to use paid tools

1. **Free trial key (easiest, self-serve)** — one curl, no account:
   ```bash
   curl -s -X POST https://czid.casuyi.com/trial -H 'content-type: application/json' -d '{"email":"you@example.com"}'
   # -> {"key":"trial-…","quota":50,"validDays":90}
   ```
   50 free paid calls, 90 days, **works on both mcp.casuyi.com and czid.casuyi.com**.
   Send it as `X-API-Key: *** header; responses carry `X-Trial-Remaining: N`.
2. **x402 (permissionless, no account)** — an unpaid decode/render call returns HTTP `402`
   with USDC payment instructions; an x402-capable agent client signs and retries automatically.
   Network: `base-sepolia` today (mainnet on request). Price per call: `GET https://mcp.casuyi.com/health`.

`list_formats` and `validate_gtin` are free and never gated.

## Try it right now (curl, no client needed)

```bash
curl -sS -X POST https://mcp.casuyi.com/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"validate_gtin","arguments":{"code":"4006381333931"}}}'
```

→ `{"valid": true, "type": "ean13", ...}` (reply is one SSE `data:` line — see [examples](examples/quickstart.md)).

## Docs

- [examples/quickstart.md](examples/quickstart.md) — every call shape: list tools, render, decode, 402 challenge, trial key
- [examples/clients.md](examples/clients.md) — connect from Claude Code / Desktop / Cursor / any MCP client
- [clients/python.py](clients/python.py) — minimal Python client (stdlib only)

## Status / support

Open an [issue](../../issues) for: trial keys, mainnet x402, a symbology you need, size limits
(images are accepted up to ~4 MB base64), uptime questions.
