#!/usr/bin/env python3
"""Minimal barcode-mcp client — stdlib only (stateless; list_formats + validate_gtin free, decode/render paid — see README).

Usage:
  python3 python.py validate_gtin code=4006381333931
  python3 python.py render_barcode text=HELLO format=QR_CODE scale=4
  python3 python.py decode_barcode image_base64=$(base64 -w0 qr.png)
"""
import json
import os
import sys
import urllib.error
import urllib.request

URL = os.environ.get("BARCODE_URL", "https://mcp.casuyi.com/mcp")


def rpc(method, params=None, req_id=1):
    body = json.dumps(
        {"jsonrpc": "2.0", "id": req_id, "method": method, "params": params or {}}
    ).encode()
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "mcp-example-client/1.0",
        "Accept": "application/json, text/event-stream",
    }
    api_key = os.environ.get("BARCODE_API_KEY")  # optional trial key (see README)
    if api_key:
        headers["X-API-Key"] = api_key
    req = urllib.request.Request(URL, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode()
    except urllib.error.HTTPError as e:
        if e.code == 402:
            print("HTTP 402 — this tool is pay-per-call. Options:", file=sys.stderr)
            print("  1) trial key: BARCODE_API_KEY=*** (ask via GitHub issue)", file=sys.stderr)
            print("  2) x402: an x402-capable client pays + retries automatically", file=sys.stderr)
            print("Schedule:", e.read().decode()[:400], file=sys.stderr)
            sys.exit(402)
        raise
    for line in raw.splitlines():  # SSE: one `data: {json}` line
        if line.startswith("data: "):
            return json.loads(line[6:])
    return json.loads(raw)


def parse_args(pairs):
    args = {}
    for p in pairs:
        k, _, v = p.partition("=")
        args[k] = int(v) if (v.isdigit() and k == "scale") else v
    return args


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    tool, targs = sys.argv[1], parse_args(sys.argv[2:])
    rpc("initialize", {
        "protocolVersion": "2025-11-25",
        "clientInfo": {"name": "python-client", "version": "0"},
        "capabilities": {},
    })
    result = rpc("tools/call", {"name": tool, "arguments": targs}, req_id=2)
    if "error" in result:
        print(json.dumps(result["error"], indent=2))
        sys.exit(1)
    for block in result["result"].get("content", []):
        if block.get("type") == "text":
            try:
                print(json.dumps(json.loads(block["text"]), indent=2, ensure_ascii=False))
            except json.JSONDecodeError:
                print(block["text"])
        elif block.get("type") == "image":
            out = "barcode.png"
            import base64
            with open(out, "wb") as fh:
                fh.write(base64.b64decode(block["data"]))
            print(f"[image saved to {out}]")


if __name__ == "__main__":
    main()
