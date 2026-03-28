import tkinter as tk
from tkinter import ttk
import json
import subprocess
import threading
import time
import serial
import serial.tools.list_ports
import tobii_research as tr
from crispy_model_manager import get_model

# ==============================================================================
# SOVEREIGN HUB GUI: Configuration & Deployment Manifold
# ==============================================================================
class SovereignHub(tk.Tk):
    """
    Primary entry point for crispy-mouse configuration and deployment.
    Manages model selection, parameter tuning, config persistence, and system launch.
    """
    
    def __init__(self):
        super().__init__()
        self.title("JuniorCloud | Crispy Hub")
        self.geometry("500x650")
        self.configure(bg="#1A1B26")
        self.attributes('-alpha', 0.95)
        
        # Load Config Tensors from persistence layer
        try:
            with open('config.json', 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            print("[HUB] config.json not found. Using defaults.")
            self.config = {
                "model_choice": "phi-3-mini",
                "sensitivity": 2.2,
                "latency_alpha": 0.15,
                "pressure_threshold": 550,
                "saccade_limit": 250
            }
        
        self.current_task = None
        self.create_widgets()

    def create_widgets(self):
        """Build GUI widget manifold"""
        # Configure theme
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background="#1A1B26", foreground="#C0F010", font=("Verdana", 10))
        style.configure("TOptionMenu", background="#2A2B3C", foreground="#C0F010")
        
        # === 1. HEADER ===
        header = tk.Label(self, text="JuniorCloud | CRISPY MOUSE HUB", 
                         bg="#1A1B26", fg="#C0F010", font=("Verdana", 14, "bold"))
        header.pack(pady=15)
        
        # === 2. MODEL SELECTION MANIFOLD ===
        tk.Label(self, text="LLM TENSOR SELECTION", bg="#1A1B26", fg="#C0F010", 
                font=("Verdana", 11, "bold")).pack(pady=10)
        
        self.model_var = tk.StringVar(value=self.config.get('model_choice', 'phi-3-mini'))
        self.model_drop = ttk.OptionMenu(self, self.model_var, 
                                        self.config.get('model_choice', 'phi-3-mini'), 
                                        "phi-3-mini", "bitnet-7b", 
                                        command=self.save_config)
        self.model_drop.pack(pady=5)
        
        # === 3. TUNING TENSORS (Sliders) ===
        self.add_slider("SENSITIVITY (Gyro Multiplier)", "sensitivity", 1.0, 5.0, 0.1)
        self.add_slider("LATENCY (Damper Alpha)", "latency_alpha", 0.05, 0.5, 0.01)
        self.add_slider("PRESSURE THRESHOLD (ADC)", "pressure_threshold", 300, 800, 10)
        self.add_slider("SACCADE LIMIT (Pixels)", "saccade_limit", 100, 500, 10)
        
        # === 4. STATUS LOG ===
        self.status_label = tk.Label(self, text="System: Ready", bg="#1A1B26", 
                                    fg="#FFFFFF", font=("Verdana", 9), wraplength=450)
        self.status_label.pack(side=tk.BOTTOM, pady=20)
        
        # === 5. DIAGNOSTIC MANIFOLD ===
        diag_frame = tk.LabelFrame(self, text=" HARDWARE DIAGNOSTICS ", bg="#1A1B26", fg="#C0F010")
        diag_frame.pack(fill=tk.X, padx=20, pady=10)

        self.mcu_status = tk.Label(diag_frame, text="● MCU: DISCONNECTED", bg="#1A1B26", fg="#FF4444")
        self.mcu_status.pack(side=tk.LEFT, padx=10, pady=5)

        self.tobii_status = tk.Label(diag_frame, text="● TOBII: DISCONNECTED", bg="#1A1B26", fg="#FF4444")
        self.tobii_status.pack(side=tk.LEFT, padx=10, pady=5)

        threading.Thread(target=self.hardware_heartbeat, daemon=True).start()

        # === 6. ACTION MANIFOLD ===
        btn_frame = tk.Frame(self, bg="#1A1B26")
        btn_frame.pack(side=tk.BOTTOM, pady=10)
        
        tk.Button(btn_frame, text="CALIBRATE & START", command=self.deploy_system, 
                 bg="#2A2B3C", fg="#C0F010", width=25, font=("Verdana", 10, "bold")).pack(pady=5)
        tk.Button(btn_frame, text="OPEN KEYBOARD UI", command=self.launch_keyboard, 
                 bg="#2A2B3C", fg="#E0E0E0", width=25, font=("Verdana", 9)).pack(pady=3)

    def add_slider(self, label, key, min_val, max_val, resolution):
        """Dynamically add parameter slider"""
        tk.Label(self, text=label, bg="#1A1B26", fg="#E0E0E0", 
                font=("Verdana", 9)).pack(anchor=tk.W, padx=40, pady=(10, 0))
        
        scale = tk.Scale(self, from_=min_val, to=max_val, resolution=resolution, 
                        orient=tk.HORIZONTAL, bg="#2A2B3C", fg="#FFFFFF", 
                        highlightthickness=0, command=lambda v: self.update_param(key, v))
        scale.set(self.config.get(key, min_val))
        scale.pack(fill=tk.X, padx=40, pady=(0, 5))

    def update_param(self, key, value):
        """Update parameter and persist to config"""
        self.config[key] = float(value)
        self.save_config()

    def save_config(self, *args):
        """Persist configuration to JSON"""
        self.config['model_choice'] = self.model_var.get()
        try:
            with open('config.json', 'w') as f:
                json.dump(self.config, f, indent=4)
            print("[HUB] Configuration persisted")
        except Exception as e:
            print(f"[HUB] Config Save Error: {e}")

    def deploy_system(self):
        """
        Initiate full system deployment (non-blocking via threading)
        1. Validate/fetch model
        2. Launch calibration manifold
        3. Signal keyboard UI activation
        """
        if self.current_task and self.current_task.is_alive():
            self.update_status("Deployment already in progress...")
            return
        
        self.current_task = threading.Thread(target=self._run_deployment, daemon=True)
        self.current_task.start()

    def _run_deployment(self):
        """Async deployment thread (prevents UI freeze)"""
        # Step 1: Check/Download Model Weights
        model_choice = self.model_var.get()
        self.update_status(f"Validating {model_choice} tensor engine...")
        
        model_path = get_model(model_choice, self.update_status)
        if not model_path:
            self.update_status("ERROR: Model fetch failed. Check internet connection.")
            return
        
        self.update_status(f"Model ready: {model_path}")
        
        # Step 2: Launch Calibration (which chains to keyboard)
        self.update_status("Deploying calibration manifold...")
        try:
            subprocess.Popen(["python", "crispy_calibrate.py"])
            self.update_status("Calibration launched. Follow on-screen prompts.")
        except Exception as e:
            self.update_status(f"ERROR: Failed to launch calibration: {e}")

    def launch_keyboard(self):
        """Launch keyboard UI directly"""
        self.update_status("Launching Liquid Glass keyboard...")
        try:
            subprocess.Popen(["python", "crispy_keyboard.py"])
            self.update_status("Keyboard UI active.")
        except Exception as e:
            self.update_status(f"ERROR: Keyboard launch failed: {e}")

    def hardware_heartbeat(self):
        """Infinite loop verifying hardware link integrity every 2 seconds."""
        while True:
            # MCU (Pro Micro) check
            ports = [p.device for p in serial.tools.list_ports.comports()]
            mcu_online = any("USB" in p or "COM" in p for p in ports)
            self.mcu_status.config(
                text="● MCU: ONLINE" if mcu_online else "● MCU: DISCONNECTED",
                fg="#C0F010" if mcu_online else "#FF4444"
            )

            # Tobii 5 check
            try:
                trackers = tr.find_all_eyetrackers()
                tobii_online = len(trackers) > 0
                self.tobii_status.config(
                    text="● TOBII: ONLINE" if tobii_online else "● TOBII: DISCONNECTED",
                    fg="#C0F010" if tobii_online else "#FF4444"
                )
            except Exception:
                self.tobii_status.config(text="● TOBII: ERROR", fg="#FF4444")

            time.sleep(2)

    def update_status(self, msg):
        """Update status label (thread-safe)"""
        self.status_label.config(text=f"System: {msg}")
        self.update_idletasks()

if __name__ == "__main__":
    SovereignHub().mainloop()
