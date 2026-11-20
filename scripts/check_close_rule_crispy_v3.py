#!/usr/bin/env python3
"""Self-check: trit-pack rate and close rule for crispy-mouse (v3).

Close rule: sha256(prev || pack || text)[:16]. Rate: 0.05.
Ports named (quant context): Home, OSai, FieldCore, Flagstaff, JuniorLLM.
Local only; binds nothing (any server must use 127.0.0.1). No network, no model pull.
"""
import hashlib

RATE = 0.05
HOST = "127.0.0.1"
PORTS = ("Home", "OSai", "FieldCore", "Flagstaff", "JuniorLLM")
FLAGS = {"mint": False, "socket": False, "layer_one": False, "fetch": False, "ue5_launch": False}


def close(prev: bytes, pack: bytes, text: bytes) -> str:
    return hashlib.sha256(prev + pack + text).hexdigest()[:16]


def layer(n: int, has_so: bool = False) -> str:
    if n < 512 * 512:
        return "T0"
    if n < 1024 * 1024:
        return "T1"
    return "T2" if has_so else "T1"


def main() -> int:
    a = close(b"", b"pack", b"text")
    assert a == close(b"", b"pack", b"text") and len(a) == 16
    assert a != close(b"x", b"pack", b"text")
    assert RATE == 0.05 and HOST == "127.0.0.1" and not any(FLAGS.values())
    assert [layer(10), layer(600000), layer(2 << 20), layer(2 << 20, True)] == ["T0", "T1", "T1", "T2"]
    print("ok rate=%s host=%s close=%s ports=%s" % (RATE, HOST, a, ",".join(PORTS)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
