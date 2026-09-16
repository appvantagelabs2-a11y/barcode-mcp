# Quickstart — raw JSON-RPC

Protocol: MCP `2026-07-28` (2025-era clients also work unchanged). Every request is a
`POST /mcp` with both headers:

```
Content-Type: application/json
Accept: application/json, text/event-stream
```

The reply is one SSE event: `event: message` + `data: {json}` — parse the line after `data: `.
`list_formats` and `validate_gtin` are free; `render_barcode` / `decode_barcode` return HTTP
`402` with x402 payment instructions unless paid.

## 1. List tools / formats

```bash
curl -sS -X POST https://mcp.casuyi.com/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

## 2. Validate a product code (free)

```bash
curl -sS -X POST https://mcp.casuyi.com/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"validate_gtin","arguments":{"code":"4006381333931"}}}'
```

## 3. Render a barcode (paid — trial key shown; or pay via x402)

```bash
curl -sS -X POST https://mcp.casuyi.com/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H 'X-API-Key: ***' \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"render_barcode","arguments":{"text":"HELLO","format":"qrCode","scale":4}}}'
```

Returns `image_base64` (PNG), the decoded self-check, and `X-Trial-Remaining: N` header.
Format names come from `list_formats` (camelCase: `qrCode`, `ean13`, `code128`, `dataMatrix`, …).

## 4. Decode from an image (paid)

```bash
B64=$(base64 -w0 my_qr.png)
curl -sS -X POST https://mcp.casuyi.com/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H 'X-API-Key: ***' \
  -d "{\"jsonrpc\":\"2.0\",\"id\":4,\"method\":\"tools/call\",\"params\":{\"name\":\"decode_barcode\",\"arguments\":{\"image_base64\":\"$B64\"}}}"
```

Keep the JSON under the body limit (~4 MB base64); resize large photos first.

## 5. Unpaid paid-tool call → HTTP 402

The 402 body is an [x402](https://docs.x402.org) payment schedule (network, amount, receiver).
An x402-capable client signs it and retries automatically.

## 6. Health / current prices

```bash
curl -sS https://mcp.casuyi.com/health
```
