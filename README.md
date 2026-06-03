# crispy-mouse

**Sov.PIO (Pneumatic-Inertial-Optical) Input SDK**

High-fidelity, edge-native assistive + deterministic macro execution interface.
Originally built for locked-in-syndrome applications, now serving as the low-latency hardware execution layer for the JuniorCloud LLC sovereign quant stack.

## Current Role in JuniorCloud LLC Ecosystem

`crispy-mouse` acts as the final deterministic execution boundary:

- Receives macro commands via Unix Domain Socket from `JuniorStock`
- Executes hardware-level actions with kinematic dampening and autoregressive prediction
- Maintains strict sovereignty (local-only, no cloud dependency)

## Integration Points

### JuniorStock (V6.4+)
- Communicates via Unix Domain Socket (`/tmp/crispy_mouse_gateway.sock`)
- Used by `SovereignExecutionBus` for low-latency trade execution
- Supports maker/taker limit orders and position management macros

### BitNet-mlx
- Provides the reasoning layer that generates high-conviction consensus
- `crispy-mouse` executes the final deterministic actions derived from BitNet inference

### JuniorMemSys-Suite
- Long-term topological memory for agent state
- `crispy-mouse` can persist macro history into the memory palace

### JuniorFetch
- Local RAG / semantic search over research documents
- Can feed contextual knowledge into macro decision making

### JuniorClimbs & JuniorCoach
- Sports performance tracking and coaching platform
- `crispy-mouse` provides low-latency input layer for real-time athlete biometric / eye-tracking data

## Architecture Principles

- **Deterministic macro-automata** (ATmega32u4 + Python layer)
- **Kinematic dampening** for smooth execution
- **Autoregressive LLM prediction** for intent forecasting
- **Zero cloud dependency** — fully local on Apple Silicon / edge hardware

## Quick Integration (from JuniorStock)

```python
from src.juniorstock.engines.swarm.execution_bus import SovereignExecutionBus

bus = SovereignExecutionBus()
receipt = bus.process_execution_payload(ticker, consensus, risk)
# Internally dispatches to crispy-mouse via Unix socket
```

## Original Mission (Preserved)

Still fully functional as a high-precision Human-Machine Interface for locked-in-syndrome users via:
- Eye tracking (Tobii)
- Sip-and-puff
- IMU + optical fusion
- Custom HID macros

## Repository

Part of the JuniorCloud LLC sovereign edge stack under `cloudcover95`.