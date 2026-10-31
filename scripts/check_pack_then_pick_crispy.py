#!/usr/bin/env python3
"""Inference slice check for crispy-mouse (JuniorCloud LLC, Inference Core lane).

Order under test: weights are trit-packed first, then the layer pick runs.
Tiers: T0 Python trit for n < 512*512, T1 bit-plane numpy for n < 1024*1024,
T2 native C when the .so exists, else fall back to T1.
No bench, no LUT, no GGUF, no network. Standard library only.
"""
import hashlib
import os

RATE = 0.05
BIND = "127.0.0.1"
FLAGS = {"mint": False, "socket": False, "layer_one": False, "fetch": False, "ue5_launch": False}
T0_MAX = 512 * 512
T1_MAX = 1024 * 1024


def trit_pack(weights):
    """Map floats to trits {-1, 0, 1} and pack 5 trits per byte (base 3)."""
    trits = [0 if abs(w) < RATE else (1 if w > 0 else -1) for w in weights]
    out = bytearray()
    for i in range(0, len(trits), 5):
        v = 0
        for t in reversed(trits[i:i + 5]):
            v = v * 3 + (t + 1)
        out.append(v)
    return bytes(out), len(trits)


def trit_unpack(packed, n):
    trits = []
    for b in packed:
        for _ in range(5):
            trits.append(b % 3 - 1)
            b //= 3
    return trits[:n]


def close_rule(prev, pack, text):
    return hashlib.sha256(prev + pack + text).hexdigest()[:16]


def layer_pick(n, so_path=None):
    if n < T0_MAX:
        return "T0"
    if n < T1_MAX:
        return "T1"
    if so_path and os.path.exists(so_path):
        return "T2"
    return "T1"


def pack_then_pick(weights, so_path=None):
    packed, n = trit_pack(weights)
    return packed, n, layer_pick(n, so_path)


def main():
    w = [0.3, -0.02, -0.7, 0.04, 0.9, -0.06, 0.0]
    packed, n, tier = pack_then_pick(w)
    assert trit_unpack(packed, n) == [1, 0, -1, 0, 1, -1, 0]
    assert tier == "T0"
    assert layer_pick(T0_MAX - 1) == "T0"
    assert layer_pick(T0_MAX) == "T1"
    assert layer_pick(T1_MAX - 1) == "T1"
    assert layer_pick(T1_MAX) == "T1"
    assert layer_pick(T1_MAX, "/nonexistent/kernel.so") == "T1"
    assert layer_pick(T1_MAX, __file__) == "T2"
    a = close_rule(b"prev", packed, b"text")
    b = hashlib.sha256(b"prev" + packed + b"text").hexdigest()[:16]
    assert a == b and len(a) == 16
    assert RATE == 0.05 and BIND == "127.0.0.1"
    assert not any(FLAGS.values())
    print("ok pack_then_pick crispy rate=%s close=%s tier=%s" % (RATE, a, tier))


if __name__ == "__main__":
    main()
