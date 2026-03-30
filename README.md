# 🖱️ Crispy Mouse: Sovereign HID Manifold v2.0
**High-Fidelity Assistive Kinematics | JuniorCloud LLC**

## 🚀 Sovereign Deployment (Windows 11)
1. **Ignite Hardware:** Flash `firmware.hex` to the ATmega32U4 via XLoader.
2. **Initialize Manifold:** Run `setup_local.bat` to instantiate the `.venv` and inject the HID/Tobii driver stack.
3. **Calibrate:** Execute `python crispy_calibrate.py` to map the optical gaze to the liquid glass interface.

## 🧠 Kinematic Fusion Logic
The system resolves user intent by projecting disparate sensor streams into a unified topological manifold.

### ### 1. Macro-Navigation (Optical Saccade-Warp)
Utilizes the Tobii 5 IR stream to perform global coordinate teleportation. This is the "Jump" logic that identifies the coarse region of interest on the display manifold.

### ### 2. Micro-Navigation (Inertial Manifold Projection)
The MPU-6050 data is processed through a first-order recursive filter to isolate intentional kinematic vectors from physiological noise.

**State-Space Vector Update:**
$$v_t = \Gamma \cdot \omega_{raw} + (I - \Gamma) \cdot v_{t-1}$$

Where:
- $\Gamma$: The Gamma Signal Inference tensor (smoothing coefficient).
- $\omega_{raw}$: Raw angular velocity vector from the IMU.
- $v_t$: The projected velocity in the screen manifold.

### ### 3. Pneumatic State Machine
A barometric transducer ($0\text{--}40\text{ kPa}$) acts as the binary/ternary interrupt:
- **$\Delta P_{short}$:** Left-Click (Discrete Event).
- **$\Delta P_{double}$:** Right-Click (Sequenced Input).
- **$\Delta P_{sustained}$:** Topological Origin Reset (HOME).

## 🔧 System Architecture
- **L1 (Physical):** MPU-6050 (Gyro) + Pneumatic Transducer + Tobii IR.
- **L2 (Firmware):** 100Hz EMA Filter Matrix (Arduino C++ / ATmega32U4).
- **L3 (Middleware):** Python 3.11 Manifold + User32.dll injection.
- **L4 (UI):** Liquid Glass "White Fog" Alpha-Interface.

## 🛡️ Security & Integrity
This SDK is edge-native. No telemetry is transmitted to third-party cloud manifolds. All SVD mesh integrity checks are performed locally on the M4/ATmega hardware. 
**Note:** `01_Legal` and `02_Assets` directories are explicitly isolated from the build pipeline.

---
JuniorCloud LLC | Lead Architect: @cloudnjr
"First-principles mathematics. No bloated frameworks. No apologies."
