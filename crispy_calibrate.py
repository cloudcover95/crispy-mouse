import tobii_research as tr
import tkinter as tk
import time
import subprocess
import sys

def calibrate():
    print("--- JuniorCloud LLC: Crispy Mouse Calibration Protocol ---")
    trackers = tr.find_all_eyetrackers()
    if not trackers:
        print("ERROR: Tobii Hardware not found.")
        return
    
    tracker = trackers[0]
    calibration = tr.ScreenBasedCalibration(tracker)
    calibration.enter_calibration_mode()

    # Define the 5-point manifold: (x, y) in normalized 0.0-1.0
    points = [
        (0.5, 0.5), # Center (Zero Point)
        (0.1, 0.1), # Top-Left Manifold
        (0.9, 0.1), # Top-Right Manifold
        (0.1, 0.9), # Bottom-Left Manifold
        (0.9, 0.9)  # Bottom-Right Manifold
    ]

    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.configure(background='black')
    canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), bg='black', highlightthickness=0)
    canvas.pack()

    # Sovereignty text over calibration
    canvas.create_text(root.winfo_screenwidth()/2, 50, text="CRISPY MOUSE CALIBRATION: FOCUS ON RED TARGET", fill="#C0F010", font=("Verdana", 16))

    def run_points(idx=0):
        if idx >= len(points):
            root.destroy()
            return

        p = points[idx]
        px, py = p[0] * root.winfo_screenwidth(), p[1] * root.winfo_screenheight()
        
        # Render Calibration Target (Volt Green on Black for contrast)
        dot = canvas.create_oval(px-30, py-30, px+30, py+30, fill='#202030', outline='#C0F010', width=5)
        root.update()
        
        # 1.2s Gaze Dwell to compute vector
        time.sleep(1.2)
        print(f"[*] Analyzing point vector: {p}")
        calibration.collect_data(p[0], p[1])
        
        canvas.delete(dot)
        # 0.3s phase shift before next point
        root.after(300, lambda: run_points(idx + 1))

    # Initiating sequence
    root.after(1000, run_points)
    root.mainloop()

    # Compute and Apply Resulting Calibration Tensor Matrix
    print("[*] Computing Sovereign Gaze Tensor...")
    result = calibration.compute_and_apply()
    print(f"[*] Calibration Complete. Status: {result.status}")
    calibration.leave_calibration_mode()

    # ==============================================================================
    # 4. AUTONOMOUS LAUNCH: SOVEREIGN KEYBOARD MANIFOLD
    # ==============================================================================
    if result.status == tr.CALIBRATION_STATUS_SUCCESS:
        print("[*] Launching Sovereign Virtual Keyboard Manifold...")
        # Use Popen to launch asynchronously, allowing this script to exit
        subprocess.Popen([sys.executable, "crispy_keyboard.py"])
    else:
        print("[!] Calibration failure. Gaze tensor is invalid. Retrying.")

if __name__ == "__main__":
    calibrate()
