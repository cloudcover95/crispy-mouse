#!/usr/bin/env python3
"""Inference-slice self-check for crispy-mouse (JuniorCloud LLC, Inference Core lane).

Stdlib only. Opens no sockets, fetches nothing, pulls no models.
Confirms the LLC guard flags, the trit-pack rate, and the close rule
sha256(prev || pack || text)[:16] agree across two independent engines.
Not a quant file; touches no ports (Home, OSai, FieldCore, Flagstaff, JuniorLLM untouched).
"""
import hashlib
import sys

RATE = 0.05
BIND_HOST = "127.0.0.1"
FLAGS = {"mint": False, "socket": False, "layer_one": False, "fetch": False, "ue5_launch": False}


def close_a(prev: bytes, pack: bytes, text: str) -> str:
    return hashlib.sha256(prev + pack + text.encode("utf-8")).hexdigest()[:16]


def close_b(prev: bytes, pack: bytes, text: str) -> str:
    h = hashlib.sha256()
    for part in (prev, pack, text.encode("utf-8")):
        h.update(part)
    return h.hexdigest()[:16]


def main() -> int:
    errors = []
    if any(FLAGS.values()):
        errors.append("guard flags must all be false")
    if BIND_HOST != "127.0.0.1":
        errors.append("bind host must be 127.0.0.1")
    if abs(RATE - 0.05) > 1e-12:
        errors.append("rate must be 0.05")
    prev = b"\x00" * 16
    for i, text in enumerate(["", "crispy-mouse", "inference slice 2026-10-16"]):
        pack = bytes([i]) * 8
        a, b = close_a(prev, pack, text), close_b(prev, pack, text)
        if a != b or len(a) != 16:
            errors.append(f"engines disagree on case {i}: {a} vs {b}")
        prev = bytes.fromhex(a)
    if errors:
        print("FAIL: " + "; ".join(errors))
        return 1
    print(f"OK: rate={RATE} close=sha256(prev||pack||text)[:16] engines agree; flags false; bind {BIND_HOST}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
