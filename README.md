# crispy-mouse

**Sovereign PIO Input + Deterministic Execution Layer**

crispy-mouse is the low-level input and execution foundation for the JuniorCloud LLC sovereign edge stack. It handles kinematic dampening, sensor fusion, and deterministic macro automation.

## Current State

- Full integration with BitNet-mlx ternary pipeline via `TernaryTelemetryAdapter`
- Telemetry and kinematic data can now be projected into discrete 1.58-bit space before execution
- Production scaffolding for multi-modal sensing (optical + WiFi CSI)
- Designed for both assistive technology and advanced robotics / performance use cases

## Integration

- **JuniorHome** → Central orchestrator
- **BitNet-mlx** → Ternary projection of sensor data
- **JuniorClimbs** → Performance imaging and movement analysis
- **JuniorOmega** → Spatial sensing and fabrication

We have come a long way from the original assistive-only scope. crispy-mouse is now a core execution and sensing layer in a full sovereign technology stack.

Part of the JuniorCloud LLC ecosystem.