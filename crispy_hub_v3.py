import serial
import serial.tools.list_ports
import time
import sys
import pyautogui
import json
import tobii_research as tr
from screeninfo import get_monitors

# ==============================================================================
# 1. USER-DEFINED COMMANDSTROKES & BINDS (Configuration Hub)
# ==============================================================================
# Users can modify these strings to bind any Windows shortcut
CONFIG = {
    "LATENCY": 0.15,      # Lower = smoother/laggier, Higher = raw/jittery
    "SENSITIVITY": 2.2,   # MPU Multiplier
    "SACCADE_LIMIT": 250, # Pixels to look before Tobii warps
    "DWELL_TIME": 1.5,    # Seconds to trigger macro
    "BINDS": {
        "TOP_LEFT":     ["alt", "tab"],
        "TOP_RIGHT":    ["win", "d"],
        "BOTTOM_LEFT":  ["esc"],
        "BOTTOM_RIGHT": ["win", "s"]
    }
}

MONITOR = get_monitors()[0]
W, H = MONITOR.width, MONITOR.height
active_zone = None
start_time = 0

# ==============================================================================
# 2. MACRO EXECUTION ENGINE
# ==============================================================================
def execute_bind(zone):
    """Execute keyboard hotkey sequence for specified gaze zone"""
    keys = CONFIG["BINDS"].get(zone)
    if keys:
        print(f"[MACRO] Executing Bind for {zone}: {keys}")
        if len(keys) > 1: 
            pyautogui.hotkey(*keys)
        else: 
            pyautogui.press(keys[0])

# ==============================================================================
# 3. MODEL SWAP MANIFOLD (LLM Engine Selection)
# ==============================================================================
def change_llm_model():
    """Swap between Phi-3-Mini and BitNet quantized engines"""
    print("\n--- Model Swap Manifold ---")
    print("[1] Phi-3-Mini (High Accuracy)")
    print("[2] BitNet 1.58-bit (Max Speed/Low Power)")
    choice = input("Select: ").strip()
    
    if choice == '1':
        selected = "phi-3-mini"
        model_file = "phi-3-mini-4k-instruct-q4.gguf"
    elif choice == '2':
        selected = "bitnet-7b"
        model_file = "bitnet-7b-q4.gguf"
    else:
        print("[ERROR] Invalid selection")
        return
    
    print(f"[LLM] Model set to {selected}.")
    print(f"[LLM] Model file: {model_file}")
    print(f"[*] Restart the Keyboard to apply changes.")

# ==============================================================================
# 4. TOBII GAZE PROCESSOR (Real-time Eye Tracking)
# ==============================================================================
def gaze_processor(data):
    """Process Tobii eye tracking data in real-time"""
    global active_zone, start_time
    
    l, r = data['left_gaze_point_on_display_area'], data['right_gaze_point_on_display_area']
    
    if l[0] and r[0]:
        # Calculate geometric center of gaze
        gx, gy = ((l[0] + r[0]) / 2) * W, ((l[1] + r[1]) / 2) * H
        
        # SACCADE LOGIC: Macro-Warp only if outside the precision threshold
        # Prevents fighting with MPU-6050 head tracking
        mx, my = pyautogui.position()
        dist = ((mx - gx)**2 + (my - gy)**2)**0.5
        if dist > CONFIG["SACCADE_LIMIT"]:
            pyautogui.moveTo(gx, gy, _pause=False)

        # COMMANDSTROKE DWELL LOGIC (Gaze-activated macros)
        z = None
        if gx < 100 and gy < 100: 
            z = "TOP_LEFT"
        elif gx > W-100 and gy < 100: 
            z = "TOP_RIGHT"
        elif gx < 100 and gy > H-100: 
            z = "BOTTOM_LEFT"
        elif gx > W-100 and gy > H-100: 
            z = "BOTTOM_RIGHT"

        if z and z == active_zone:
            if (time.time() - start_time) > CONFIG["DWELL_TIME"]:
                execute_bind(z)
                active_zone = None # Lockout after execution
        else:
            active_zone, start_time = z, time.time()

# ==============================================================================
# 5. MAIN CONFIGURATION INTERFACE
# ==============================================================================

def main():
    print("\n=== CRISPY MOUSE: SOVEREIGN HUB V3 (Tobii + Head Tracking) ===\n")
    
    # Initialize Tobii Eye Tracker
    print("[TOBII] Scanning optical interfaces...")
    trackers = tr.find_all_eyetrackers()
    if trackers: 
        trackers[0].subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_processor, as_dictionary=True)
        print(f"[TOBII] Eye tracker initialized: {trackers[0].device_name}")
    else:
        print("[WARNING] No Tobii tracker found. Eye tracking disabled.")
    
    # Initialize Serial Connection to MCU
    ports = serial.tools.list_ports.comports()
    mcu = next((p.device for p in ports if "USB" in p.description or "COM" in p.device), None)
    if not mcu: 
        print("[ERROR] Hardware Manifold Not Found.")
        sys.exit(1)

    try:
        ser = serial.Serial(mcu, 115200, timeout=0.1)
        print(f"[SERIAL] Connected to {mcu}")
    except Exception as e:
        print(f"[ERROR] Serial connection failed: {e}")
        sys.exit(1)
    
    # Interactive Configuration Loop
    while True:
        print(f"\n[CURRENT CONFIG]")
        print(f"  Latency (Smoothing): {CONFIG['LATENCY']}")
        print(f"  Sensitivity (MPU):   {CONFIG['SENSITIVITY']}")
        print(f"  Saccade Limit:       {CONFIG['SACCADE_LIMIT']} px")
        print(f"  Dwell Time:          {CONFIG['DWELL_TIME']}s")
        print(f"\n[1] Adjust Latency (Smoothing)")
        print("[2] Adjust Sensitivity")
        print("[3] Set Saccade Limit")
        print("[4] Change Gaze-Zone Binds")
        print("[5] Save Config to File")
        print("[6] Swap LLM Model")
        print("[0] Exit")
        
        choice = input("\nSelect Segment: ").strip()

        if choice == '1':
            try:
                val = float(input("New Latency Alpha (0.01 - 1.0): "))
                if 0.01 <= val <= 1.0:
                    CONFIG["LATENCY"] = val
                    ser.write(f"DAMP:{val}\n".encode())
                    print(f"[ACK] Latency set to {val}")
            except ValueError:
                print("[ERROR] Invalid input")
                
        elif choice == '2':
            try:
                val = float(input("New Sensitivity (1.0 - 5.0): "))
                if 1.0 <= val <= 5.0:
                    CONFIG["SENSITIVITY"] = val
                    ser.write(f"SENS:{val}\n".encode())
                    print(f"[ACK] Sensitivity set to {val}")
            except ValueError:
                print("[ERROR] Invalid input")
                
        elif choice == '3':
            try:
                val = int(input("New Saccade Limit (100-500 pixels): "))
                if 100 <= val <= 500:
                    CONFIG["SACCADE_LIMIT"] = val
                    print(f"[ACK] Saccade limit set to {val}px")
            except ValueError:
                print("[ERROR] Invalid input")
                
        elif choice == '4':
            zone = input("Which zone? (TOP_LEFT/TOP_RIGHT/BOTTOM_LEFT/BOTTOM_RIGHT): ").upper().strip()
            if zone in CONFIG["BINDS"]:
                keys_str = input("Keys (comma separated, e.g. win,d): ").strip()
                keys = [k.strip() for k in keys_str.split(',')]
                CONFIG["BINDS"][zone] = keys
                print(f"[ACK] Bind updated: {zone} -> {keys}")
            else:
                print("[ERROR] Unknown zone")
                
        elif choice == '5':
            try:
                with open('crispy_config.json', 'w') as f:
                    json.dump(CONFIG, f, indent=2)
                print("[ACK] Configuration saved to crispy_config.json")
            except Exception as e:
                print(f"[ERROR] Failed to save config: {e}")
                
        elif choice == '6':
            change_llm_model()
                
        elif choice == '0':
            ser.close()
            print("[SYSTEM] Exiting. Goodbye!")
            break
        else:
            print("[ERROR] Invalid selection")

if __name__ == "__main__":
    main()
