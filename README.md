# crispy-mouse

**Sov.PIO — Sovereign Input + Deterministic Macro Execution Layer**

A high-fidelity, edge-native interface for **user-controlled operating systems**, AI robotics, assistive technology, and deterministic automation.

Originally developed for locked-in-syndrome applications, `crispy-mouse` has evolved into a universal low-level input and execution bus that works across human-computer interaction, robotics, quant trading execution, and imaging systems — all while remaining fully local and sovereign.

## Core Philosophy

- **User-controlled operating systems** — Direct, low-latency control of macOS, Linux, Windows, and embedded systems
- **Deterministic macro-automata** — Reliable, auditable action execution (no probabilistic drift)
- **Edge-native & air-gapped** — Runs entirely locally on Apple Silicon, Raspberry Pi, microcontrollers (ATmega32u4), etc.
- **Sensor fusion input** — IMU, optical, eye-tracking, LiDAR, pneumatic, sip-and-puff, and custom sensors

## Use Cases

### 1. User-Controlled Operating Systems
- Full keyboard/mouse/HID macro execution
- System automation and workflow orchestration
- Accessibility layer for locked-in users
- Sovereign desktop control without cloud dependencies

### 2. AI Robotics & Autonomous Systems
- Low-latency action execution for robotic arms, mobile robots, and drones
- Sensor-to-action pipelines (eye-tracking → robot control)
- Deterministic safety layers for human-robot interaction
- Integration with edge AI models (BitNet-mlx, MLX)

### 3. Extraneous Imaging & Computer Vision
- Real-time visual input processing pipelines
- Eye-tracking + external camera fusion ("extraneous imaging")
- Integration with JuniorClimbs / JuniorCoach for sports performance vision systems
- LiDAR / TrueDepth / optical flow input for spatial computing and robotics

### 4. Quant Trading Execution (JuniorStock)
- High-speed, deterministic trade execution via Unix Domain Socket
- Kinematic dampening for smooth order placement
- Used by `SovereignExecutionBus` in JuniorStock V6.4+

## Ecosystem Integration (JuniorCloud LLC)

| Project              | Role of crispy-mouse                          |
|----------------------|-----------------------------------------------|
| **JuniorStock**      | Low-latency execution bus via Unix socket     |
| **BitNet-mlx**       | Final deterministic action layer              |
| **JuniorMemSys**     | Persist macro history into topological memory |
| **JuniorFetch**      | Context-aware macro triggering                |
| **JuniorClimbs**     | Vision + biometric input layer for performance imaging |
| **JuniorOmega**      | Spatial computing / fabrication input         |

## Technical Foundation

- Deterministic macro engine (Python + C firmware)
- Kinematic dampening & autoregressive prediction
- Unix Domain Socket + HID interfaces
- Full MLX / Metal acceleration support on Apple Silicon
- Cross-platform (macOS, Linux, embedded)

## Getting Started

```bash
# From JuniorStock
python -c "from src.juniorstock.engines.swarm.execution_bus import SovereignExecutionBus; ..."

# Direct hardware macro example
# (See examples/ in future releases)
```

`crispy-mouse` remains the reliable, sovereign execution foundation for the entire JuniorCloud LLC edge stack.