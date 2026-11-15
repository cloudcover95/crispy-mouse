#!/usr/bin/env python3
"""Self-check: rate and close rule for crispy-mouse (LLC guards 3,4,5,7).

Local only. Ports touched: none (no sockets). Host pinned to 127.0.0.1.
Close rule: sha256(prev || pack || text)[:16]. Rate: 0.05.
"""
import hashlib

RATE = 0.05
HOST = "127.0.0.1"
FLAGS = {"mint": False, "socket": False, "layer_one": False, "fetch": False, "ue5_launch": False}


def close(prev: bytes, pack: bytes, text: bytes) -> str:
    return hashlib.sha256(prev + pack + text).hexdigest()[:16]


def pick_layer(n: int, native_so: bool = False) -> str:
    if n < 512 * 512:
        return "T0"
    if n < 1024 * 1024:
        return "T1"
    return "T2" if native_so else "T1"


def main() -> int:
    assert HOST == "127.0.0.1"
    assert not any(FLAGS.values())
    assert RATE == 0.05
    a = close(b"", b"\x01\x00\xff", b"hello")
    assert a == close(b"", b"\x01\x00\xff", b"hello") and len(a) == 16
    assert a != close(b"x", b"\x01\x00\xff", b"hello")
    assert [pick_layer(1000), pick_layer(600000), pick_layer(2**21), pick_layer(2**21, True)] == ["T0", "T1", "T1", "T2"]
    print("ok rate=%s close=%s" % (RATE, a))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
