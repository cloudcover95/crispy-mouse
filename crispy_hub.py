import serial
import serial.tools.list_ports
import time
import sys
import pyautogui
import tobii_research as tr
from screeninfo import get_monitors

# ==============================================================================
# SENSOR FUSION TENSORS
# ==============================================================================
SACCADE_THRESHOLD = 180  # Pixels to move before Tobii "warps" the cursor
GAZE_ALPHA = 0.75        # Smoothing for eye tracking (0.1 = Raw, 0.9 = High Lag)

MONITOR = get_monitors()[0]
current_x, current_y = MONITOR.width / 2, MONITOR.height / 2

def gaze_data_callback(gaze_data):
    global current_x, current_y
    left = gaze_data['left_gaze_point_on_display_area']
    right = gaze_data['right_gaze_point_on_display_area']
    
    if left[0] and right[0]:
        # Calculate screen coordinates from normalized gaze
        raw_x = ((left[0] + right[0]) / 2) * MONITOR.width
        raw_y = ((left[1] + right[1]) / 2) * MONITOR.height
        
        # Exponential Moving Average (EMA) for optical stability
        current_x = (GAZE_ALPHA * current_x) + ((1 - GAZE_ALPHA) * raw_x)
        current_y = (GAZE_ALPHA * current_y) + ((1 - GAZE_ALPHA) * raw_y)

        # Macro-Navigation: Only warp if gaze distance exceeds threshold
        mouse_x, mouse_y = pyautogui.position()
        if abs(mouse_x - current_x) > SACCADE_THRESHOLD:
            pyautogui.moveTo(current_x, current_y, _pause=False)

def main():
    print("=== Crispy Mouse: Windows 11 Sovereign Hub ===")
    
    # 1. Initialize Tobii Optical Pipeline
    trackers = tr.find_all_eyetrackers()
    if not trackers:
        print("[!] Tobii hardware not detected.")
        tracker = None
    else:
        tracker = trackers[0]
        tracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
        print(f"[*] Tobii Optical Lock: {tracker.device_name}")

    # 2. Initialize Serial Manifold
    ports = serial.tools.list_ports.comports()
    mcu_port = next((p.device for p in ports if "USB" in p.description or "COM" in p.device), None)
    
    if mcu_port:
        ser = serial.Serial(mcu_port, 115200, timeout=1)
        print(f"[*] Hardware Link established on {mcu_port}")
    else:
        print("[!] ATmega32U4 not found. Check USB connection.")
        sys.exit(1)

    try:
        while True:
            # You can inject live tuning commands here
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n--- Powering Down Hub ---")
        if tracker: tracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
        ser.close()

if __name__ == "__main__":
    main()