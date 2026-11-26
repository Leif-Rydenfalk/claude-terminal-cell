"""selftest: forwarding works against a fake `ce`, and only read-only ops are forwarded (no Start*/Turn)."""
import os, stat, sys, tempfile
import main

d = tempfile.mkdtemp()
fake = os.path.join(d, "ce")
open(fake, "w").write('#!/bin/sh\necho "$@" >> %s/log\ncase "$4" in HealthOp) echo \'{"ok":true,"version":"9","uptime_s":1}\';; *) echo \'[{"n":3}]\';; esac\n' % d)
os.chmod(fake, 0o755)
main.CE = fake
h = main.op_health({})
assert h["ok"] and h["provider"]["version"] == "9", h
assert main.op_count({})["sources"] == [{"n": 3}]
try:
    main.forward("Turn"); raise SystemExit("Turn was forwarded")
except ValueError:
    pass
assert "ai.provider#claude.terminal" in open(os.path.join(d, "log")).read()
print("claude.terminal selftest ok")
