# claude.terminal

The cell name for the Claude Code provider that already runs on a node as `ai.provider#claude.terminal` (repo `claude-terminal`, Rust). This small ce-py cell answers `HealthOp` and forwards the read-only ops `Describe` and `Count` to it through the door. It never starts a Claude turn, so calling it costs nothing.

## Use when
You want to ask whether the Claude provider on a node is up, what it offers, or how many sessions it can see.

```
ce cell call claude.terminal HealthOp '{"json":"{}"}'
ce cell call claude.terminal Count '{"json":"{}"}'
```

Test: `PYTHONPATH=~/dev/ce-py python3 selftest.py`. `provider.descriptor.json` is the ai.provider@1 wire descriptor (made with `ce-wire-gen --lang json` on ai-session) used to call the instance.
