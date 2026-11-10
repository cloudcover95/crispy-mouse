#!/usr/bin/env python3
"""Offline self-check: trit pack at rate 0.05, layer tier pick, close-hash chain.
Stdlib only. No network, no server, no model pull, no bench/LUT/GGUF."""
import hashlib, os, sys

RATE = 0.05
FLAGS = {"mint": False, "socket": False, "layer_one": False, "fetch": False, "ue5_launch": False}
BIND_HOST = "127.0.0.1"  # any server must bind here only; none is started


def weights(n, seed=7):
    x, out = seed, []
    for _ in range(n):
        x = (x * 1103515245 + 12345) & 0x7FFFFFFF
        out.append((x / 0x7FFFFFFF) * 2 - 1)
    return out


def trit_pack(w, rate=RATE):
    """Ternary quantize: |v| below threshold -> 0 else sign. Threshold = rate-scaled mean abs."""
    thr = rate * (sum(abs(v) for v in w) / len(w)) * 10
    return bytes((0 if abs(v) <= thr else (1 if v > 0 else 2)) for v in w)


def pick_tier(n, so_path="libtrit.so"):
    if n < 512 * 512:
        return "T0"
    if n < 1024 * 1024:
        return "T1"
    return "T2" if os.path.exists(so_path) else "T1"


def close_hash(prev, pack, text):
    return hashlib.sha256(prev + pack + text.encode()).hexdigest()[:16]


def main():
    w = weights(256)
    pack = trit_pack(w)
    assert set(pack) <= {0, 1, 2} and len(pack) == len(w)
    assert RATE == 0.05
    assert pick_tier(256) == "T0"
    assert pick_tier(512 * 512) == "T1"
    assert pick_tier(1024 * 1024, "/nonexistent.so") == "T1"
    prev, chain = b"genesis", []
    for t in ("open", "pack", "close"):
        h = close_hash(prev, pack, t)
        assert len(h) == 16 and h == hashlib.sha256(prev + pack + t.encode()).hexdigest()[:16]
        chain.append(h)
        prev = h.encode()
    assert len(set(chain)) == 3
    assert not any(FLAGS.values()) and BIND_HOST == "127.0.0.1"
    print("OK rate=%s tier=%s chain=%s" % (RATE, pick_tier(len(w)), ",".join(chain)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
