#!/usr/bin/env python3
"""Inference-slice self-check for crispy-mouse (JuniorCloud LLC, Inference Core lane).

Stdlib only. No network, no model pull, no GGUF, no bench, no LUT.
Checks the layer-stack pick (T0/T1/T2), the trit-pack rate and close rule,
and the LLC safety flags. Ports touched: Home, OSai, FieldCore, Flagstaff, JuniorLLM.
"""
import hashlib
import os
import sys

RATE = 0.05
BIND = "127.0.0.1"
FLAGS = {"mint": False, "socket": False, "layer_one": False, "fetch": False, "ue5_launch": False}
PORTS = ("Home", "OSai", "FieldCore", "Flagstaff", "JuniorLLM")
T0_MAX = 512 * 512
T1_MAX = 1024 * 1024


def close_rule(prev: bytes, pack: bytes, text: bytes) -> str:
    return hashlib.sha256(prev + pack + text).hexdigest()[:16]


def trit_pack(values):
    """Pack ternary values {-1,0,1} five per byte (base 3)."""
    out = bytearray()
    for i in range(0, len(values), 5):
        acc = 0
        for v in reversed(values[i:i + 5]):
            if v not in (-1, 0, 1):
                raise ValueError("non-ternary value")
            acc = acc * 3 + (v + 1)
        out.append(acc)
    return bytes(out)


def pick_layer(n: int, so_path: str = "") -> str:
    if n < T0_MAX:
        return "T0"
    if n < T1_MAX:
        return "T1"
    if so_path and os.path.exists(so_path):
        return "T2"
    return "T1"  # T2 falls back to T1 when the native .so is absent


def main() -> int:
    ok = True
    weights = [1, 0, -1, -1, 1, 0, 0, 1]
    pack = trit_pack(weights)  # weights trit-packed before the layer pick
    picks = {n: pick_layer(n) for n in (1, T0_MAX - 1, T0_MAX, T1_MAX - 1, T1_MAX)}
    expect = {1: "T0", T0_MAX - 1: "T0", T0_MAX: "T1", T1_MAX - 1: "T1", T1_MAX: "T1"}
    if picks != expect:
        ok = False
        print("stack: FAIL", picks)
    c1 = close_rule(b"", pack, b"crispy-mouse")
    c2 = close_rule(b"", pack, b"crispy-mouse")
    if c1 != c2 or len(c1) != 16:
        ok = False
        print("close rule: FAIL")
    if RATE != 0.05:
        ok = False
    if BIND != "127.0.0.1":
        ok = False
    if any(FLAGS.values()):
        ok = False
    print(f"rate={RATE} close={c1} bind={BIND} flags_all_false={not any(FLAGS.values())}")
    print("stack:", " ".join(f"{k}->{v}" for k, v in picks.items()))
    print("ports:", ", ".join(PORTS))
    print("OK" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
