import tkinter as tk
from tkinter import ttk
import json
import os
import sys
import ctypes
import pyautogui
import threading
import time
import subprocess

# ==============================================================================
# SOVEREIGN GLASS AESTHETICS (Liquid Glass UI Constants)
# ==============================================================================
C_GLASS = "#1A1B26"  # Deep Slate (primary background)
C_FOG   = "#E0E0E0"  # Static White (secondary text)
C_VOLT  = "#C0F010"  # Alert Green (accent/highlight)
F_FONT  = ("Verdana", 10)

# ==============================================================================
# WINDOWS 11 HARDWARE INTEGRATION LAYER
# ==============================================================================
def deploy_large_cursor_manifold():
    """Force Windows User32 SPI to reload large cursor tensors (high-visibility)"""
    try:
        ctypes.windll.user32.SystemParametersInfoW(0x2029, 0, None, 0x01 | 0x02)
        print("[CURSOR] Large cursor manifold deployed")
    except Exception as e:
        print(f"[CURSOR] Warning: Could not deploy large cursor: {e}")

# ==============================================================================
# SOVEREIGN HUB: MONOLITHIC CONTROLLER (Windows 11 Target)
# ==============================================================================
class SovereignHub(tk.Tk):
    """
    Unified configuration controller for crispy-mouse SDK.
    Manages kinematic tensors, LLM models, commandstroke binds, Windows 11 integration.
    """
    
    def __init__(self):
        super().__init__()
        self.title("JuniorCloud | Crispy Mouse SDK")
        self.geometry("600x750")
        self.configure(bg=C_GLASS)
        self.attributes('-alpha', 0.98)  # Slight alpha for Glass feel
        
        self.load_config()
        self.create_widgets()

    def load_config(self):
        """Load configuration manifesto from JSON"""
        if not os.path.exists('config.json'):
            sys.exit("ERROR: config.json missing.")
        with open('config.json', 'r') as f:
            self.config = json.load(f)
        print("[HUB] Configuration loaded")

    def save_config(self):
        """Persist configuration to JSON"""
        with open('config.json', 'w') as f:
            json.dump(self.config, f, indent=4)
        print("[HUB] Configuration saved")
        # TODO: In real deployment, send Serial updates (SENS, DAMP, THRE) to Pro Micro here

    def create_widgets(self):
        """Construct all UI elements"""
        self.create_glass_styles()

        # === MONOLITHIC LOG BAR (Status Display) ===
        self.log_var = tk.StringVar(value="[SYSTEM] Awaiting Kinematic Manifold.")
        self.log_bar = tk.Label(self, textvariable=self.log_var, bg=C_GLASS, fg=C_FOG, 
                               font=("Verdana", 9), wraplength=580, justify=tk.LEFT)
        self.log_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        # === MONOLITHIC TABBED MANIFOLD (Optimized Navigation) ===
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tab 1: KINEMATICS & LLM TENSORS
        self.tab_tuning = tk.Frame(self.tabs, bg=C_GLASS)
        self.tabs.add(self.tab_tuning, text=" TUNING TENSORS ")
        self.create_tuning_tab()

        # Tab 2: COMMANDSTROKE EDITOR (Corner Binds)
        self.tab_commands = tk.Frame(self.tabs, bg=C_GLASS)
        self.tabs.add(self.tab_commands, text=" COMMANDSTROKES ")
        self.create_commands_tab()

        # Tab 3: WINDOWS 11 CUSTOMIZATION
        self.tab_os = tk.Frame(self.tabs, bg=C_GLASS)
        self.tabs.add(self.tab_os, text=" WIN11 INTEGRATION ")
        self.create_os_tab()

        # === START MANIFOLD (Action Button) ===
        btn_frame = tk.Frame(self, bg=C_GLASS)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(btn_frame, text="RUN CALIBRATION & LAUNCH", command=self.deploy_system,
                  bg="#2A2B3C", fg=C_VOLT, font=("Verdana", 11, "bold"), relief=tk.FLAT).pack(pady=5, fill=tk.X)

    # ==========================================================================
    # TAB 1: TUNING TENSORS (Kinematic & LLM Parameter Manifold)
    # ==========================================================================
    def create_tuning_tab(self):
        """Construct kinematic sensitivity, latency, pressure, and model selection UI"""
        p = self.tab_tuning

        # 1. KINEMATIC TENSORS (Micro-Navigation Feel)
        self.add_section_header(p, "INERTIAL SENSOR TENSORS (MPU-6050)")
        self.add_tensor_slider(p, "KINEMATIC SENSITIVITY", "sensitivity", 1.0, 5.0, 0.1)
        self.add_tensor_slider(p, "LATENCY (α Smoothing)", "latency_alpha", 0.01, 0.40, 0.01)
        self.add_tensor_slider(p, "PNEUMATIC THRESHOLD", "pressure_threshold", 400, 900, 10)

        # 2. LLM MODEL TENSORS (Prediction Engine Selection)
        self.add_section_header(p, "BITNET / LOCAL LLM TENSORS")
        tk.Label(p, text="Autoregressive Model", bg=C_GLASS, fg=C_FOG, font=F_FONT).pack(anchor="w", padx=30)
        self.model_var = tk.StringVar(value=self.config['model_choice'])
        self.model_drop = ttk.OptionMenu(p, self.model_var, self.config['model_choice'], 
                                         "phi-3-mini", "bitnet-7b")
        self.model_drop.pack(fill=tk.X, padx=30, pady=5)
        # Bind change to save automatically
        self.model_var.trace("w", lambda *a: self.update_tensor_raw("model_choice", self.model_var.get()))

    # ==========================================================================
    # TAB 2: COMMANDSTROKE EDITOR (Corner Macro Bindings)
    # ==========================================================================
    def create_commands_tab(self):
        """Construct gaze dwell commandstroke editor for corner-based macros"""
        p = self.tab_commands
        self.add_section_header(p, "GAZE DWELL COMMANDSTROKES (Macros)")
        tk.Label(p, text="Looking at a corner for 1.5s triggers these Windows shortcuts.", 
                 bg=C_GLASS, fg="#8080A0", font=("Verdana", 9), wraplength=500, justify=tk.LEFT).pack(pady=10, padx=30)

        # Store Entry widgets for retrieval
        self.cmd_entries = {}
        
        # Grid Manifold for visual mapping (4 corners)
        grid_f = tk.Frame(p, bg=C_GLASS)
        grid_f.pack(pady=20, fill=tk.BOTH, expand=True, padx=10)
        
        # Optimized layout: Mapping physical screen corners
        corners = [
            ("TOP_LEFT", 0, 0, "↖"),
            ("TOP_RIGHT", 0, 1, "↗"),
            ("BOTTOM_LEFT", 1, 0, "↙"),
            ("BOTTOM_RIGHT", 1, 1, "↘")
        ]

        for zone, r, c, arrow in corners:
            frame = tk.LabelFrame(grid_f, text=f" {arrow} {zone} ", bg=C_GLASS, fg=C_FOG, font=F_FONT)
            frame.grid(row=r, column=c, sticky="nsew", padx=10, pady=10)
            
            grid_f.grid_columnconfigure(c, weight=1)
            grid_f.grid_rowconfigure(r, weight=1)

            keys_str = ",".join(self.config['commands'][zone])
            entry = tk.Entry(frame, bg="#202030", fg=C_VOLT, font=("Verdana", 11), 
                           relief=tk.FLAT, insertbackground=C_VOLT)
            entry.insert(0, keys_str)
            entry.pack(fill=tk.X, padx=10, pady=10)
            self.cmd_entries[zone] = entry

        tk.Button(p, text="SAVE COMMANDS", command=self.save_commandstrokes,
                  bg="#2A2B3C", fg=C_VOLT, font=F_FONT, relief=tk.FLAT).pack(pady=20, padx=30, fill=tk.X)

    def save_commandstrokes(self):
        """Parse and persist commandstroke entries to config"""
        for zone, entry in self.cmd_entries.items():
            # Clean and parse the input into a list manifold
            keys = [k.strip().lower() for k in entry.get().split(',') if k.strip()]
            self.config['commands'][zone] = keys
        self.save_config()
        self.update_log("[MACROS] Commandstrokes synchronized.")

    # ==========================================================================
    # TAB 3: WINDOWS 11 INTEGRATION (Accessibility & OS Customizations)
    # ==========================================================================
    def create_os_tab(self):
        """Construct Windows 11 accessibility and system integration controls"""
        p = self.tab_os
        self.add_section_header(p, "WINDOWS 11 NATIVE CUSTOMIZATIONS")
        
        # Toggle: Force PoE-style Large Cursor
        self.add_win_toggle(p, "FORCE LARGE HIGH-VISIBILITY CURSOR (SPI_SETCURSORS)", 
                          "cursor_scale_force")

        # Toggle: UI Transparency
        self.add_tensor_slider(p, "UI ALPHA (Glass Opacity)", "ui_alpha", 0.5, 1.0, 0.05)

        # Gaze Saccade Warp Threshold
        self.add_section_header(p, "TOBII GAZE OPTIMIZATIONS")
        self.add_tensor_slider(p, "SACCADE WARP THRESHOLD (Pixels)", "saccade_warp_threshold", 100, 500, 10)
        
        # Access: Windows 11 Accessibility Manifold
        self.add_section_header(p, "WINDOWS 11 NATIVE SETTINGS QUICK-LINK")
        tk.Label(p, text="Open native Accessibility settings for Pointer Size and Contrast.",
                 bg=C_GLASS, fg="#8080A0", font=("Verdana", 9)).pack(pady=5)
        tk.Button(p, text="OPEN WIN11 ACCESSIBILITY SETTINGS", 
                  command=lambda: os.system("start ms-settings:easeofaccess-mouse"),
                  bg="#2A2B3C", fg=C_FOG, font=F_FONT, relief=tk.FLAT).pack(pady=10, padx=30, fill=tk.X)

    # ==========================================================================
    # HELPER METHODS & UI UTILITIES
    # ==========================================================================
    def add_section_header(self, p, text):
        """Add a visual section header to UI"""
        tk.Label(p, text=text, bg=C_GLASS, fg=C_VOLT, 
                font=("Verdana", 11, "bold")).pack(anchor="w", padx=20, pady=(20, 10))

    def add_tensor_slider(self, p, label, key, min_val, max_val, res):
        """Add a parameter slider with label"""
        tk.Label(p, text=f"{label}:", bg=C_GLASS, fg=C_FOG, font=F_FONT).pack(anchor="w", padx=30)
        scale = tk.Scale(p, from_=min_val, to=max_val, resolution=res, orient=tk.HORIZONTAL, 
                         bg=C_GLASS, fg="#FFFFFF", highlightthickness=0, troughcolor="#2A2B3C", 
                         command=lambda v: self.update_tensor_raw(key, v))
        scale.set(self.config[key])
        scale.pack(fill=tk.X, padx=40, pady=(0, 10))

    def add_win_toggle(self, p, label, key):
        """Add a boolean toggle checkbox"""
        frame = tk.Frame(p, bg=C_GLASS)
        frame.pack(fill=tk.X, padx=30, pady=10)
        
        tk.Label(frame, text=label, bg=C_GLASS, fg=C_FOG, font=F_FONT).pack(side=tk.LEFT)
        
        var = tk.BooleanVar(value=self.config[key])
        btn = tk.Checkbutton(frame, variable=var, bg=C_GLASS, activebackground=C_GLASS, 
                             selectcolor="#2A2B3C",
                             command=lambda: self.update_tensor_raw(key, var.get()))
        btn.pack(side=tk.RIGHT)

    def update_tensor_raw(self, key, value):
        """Update a configuration parameter with type coercion"""
        # Convert Tkinter string values to correct JSON types
        if isinstance(self.config[key], float):
            value = float(value)
        elif isinstance(self.config[key], int):
            value = int(value)
        elif isinstance(self.config[key], bool):
            value = bool(value)
        
        self.config[key] = value
        self.save_config()
        self.update_log(f"[CONFIG] {key} → {value}")

    def update_log(self, msg):
        """Update status log message"""
        self.log_var.set(msg)
        print(msg)

    def deploy_system(self):
        """Initiate full system deployment (calibration + launch)"""
        self.save_config()
        self.update_log("[SYSTEM] Model deploying... launching calibration...")
        # Launch calibration subprocess
        try:
            subprocess.Popen([sys.executable, "crispy_calibrate.py"])
        except Exception as e:
            self.update_log(f"[ERROR] Calibration launch failed: {e}")

    def create_glass_styles(self):
        """Configure ttk theme for Liquid Glass aesthetics"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Notebook (Tab Container)
        style.configure("TNotebook", background=C_GLASS, borderwidth=0)
        style.configure("TNotebook.Tab", background="#2A2B3C", foreground=C_FOG, 
                       font=F_FONT, padding=[10, 5], relief=tk.FLAT)
        style.map("TNotebook.Tab", 
                 background=[("selected", C_GLASS)], 
                 foreground=[("selected", C_VOLT)])
        style.configure("TNotebook", background=C_GLASS, tabmargins=[2, 5, 2, 0])
        
        # OptionMenu / Dropdown
        style.configure("TCombobox", fieldbackground="#2A2B3C", background="#2A2B3C", 
                       foreground=C_FOG, arrowcolor=C_FOG)

if __name__ == "__main__":
    if os.name != 'nt':
        sys.exit("ERROR: Windows 11 target required.")
    
    deploy_large_cursor_manifold()  # Launch with high-vis cursor
    root = SovereignHub()
    root.mainloop()