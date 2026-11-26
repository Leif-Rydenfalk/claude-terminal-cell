#!/usr/bin/env python3
"""claude.terminal: the registered cell front of the Rust provider ai.provider#claude.terminal.

The provider (repo claude-terminal, Rust) already runs on this node as an ai.provider@1 instance. This small
ce-py cell gives it a plain cell name, `claude.terminal`, with Health and read-only forwarded ops. It never starts
a Claude turn: only HealthOp, Describe and Count are forwarded (no Start*/Turn), so it costs nothing to call.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import ce

SERVICE, TOPIC, VERSION = "claude.terminal", "claude-terminal/ctl", "0.1.0"
TARGET = "ai.provider#claude.terminal"
DESC = Path(os.environ.get("CLAUDE_TERMINAL_DESC", Path(__file__).with_name("provider.descriptor.json")))
CE = os.environ.get("CE_BIN") or shutil.which("ce") or str(Path.home() / ".local/bin/ce")
READ_OPS = {"HealthOp", "Describe", "Count"}


def forward(op: str, args: dict | None = None, timeout: int = 30):
    """Call one read-only op of ai.provider#claude.terminal through the door with `ce cell call`."""
    if op not in READ_OPS:
        raise ValueError(f"op {op} is not forwarded (read-only: {sorted(READ_OPS)})")
    done = subprocess.run([CE, "cell", "call", TARGET, op, json.dumps(args or {}), "--descriptor", str(DESC),
                           "--abilities", "ai.provider:*"], capture_output=True, text=True, timeout=timeout)
    if done.returncode != 0:
        raise RuntimeError((done.stderr or done.stdout).strip()[:400])
    return json.loads(done.stdout)


def op_health(args):
    """HealthOp: ok when the cell is up and the provider ai.provider#claude.terminal answers its own HealthOp."""
    try:
        prov = forward("HealthOp")
        return {"ok": bool(prov.get("ok")), "api": SERVICE, "version": VERSION, "provider": prov}
    except Exception as e:
        return {"ok": False, "api": SERVICE, "version": VERSION, "error": str(e)}


def op_describe(args):
    """Describe: what the provider ai.provider#claude.terminal is (family, modes, models, harness). Read-only."""
    return forward("Describe")


def op_count(args):
    """Count: how many Claude Code transcripts / panes the provider would scan, per source. Read-only."""
    return {"sources": forward("Count")}


def main():
    return ce.serve_app(SERVICE, TOPIC, {"HealthOp": op_health, "Describe": op_describe, "Count": op_count},
                        summary="Cell front of the Claude Code provider ai.provider#claude.terminal: health, describe, count. Never runs a paid turn.",
                        workers=2)


if __name__ == "__main__":
    raise SystemExit(main())
