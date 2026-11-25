#!/usr/bin/env python3
"""Close-rule check for crispy-mouse (v4). Offline, stdlib only.
Rule: close = sha256(prev || pack || text)[:16]; trit rate 0.05; bind 127.0.0.1.
Guard flags stay false: mint, socket, layer_one, fetch, ue5_launch.
Ports touched: none (no quant ports)."""
import hashlib, sys

RATE = 0.05
HOST = "127.0.0.1"
FLAGS = {"mint": False, "socket": False, "layer_one": False, "fetch": False, "ue5_launch": False}


def close(prev: bytes, pack: bytes, text: bytes) -> str:
    return hashlib.sha256(prev + pack + text).hexdigest()[:16]


def close_alt(prev: bytes, pack: bytes, text: bytes) -> str:
    h = hashlib.sha256()
    for part in (prev, pack, text):
        h.update(part)
    return h.hexdigest()[:16]


def selftest() -> int:
    prev = b""
    for i in range(200):
        pack = bytes((i * 7 + j) % 3 for j in range(16))
        text = ("row-%d" % i).encode()
        a, b = close(prev, pack, text), close_alt(prev, pack, text)
        assert a == b and len(a) == 16, "engines disagree"
        prev = a.encode()
    assert RATE == 0.05 and HOST == "127.0.0.1" and not any(FLAGS.values())
    print("ok close_rule=sha256(prev||pack||text)[:16] rate=%s host=%s tip=%s" % (RATE, HOST, prev.decode()))
    return 0


if __name__ == "__main__":
    sys.exit(selftest())
