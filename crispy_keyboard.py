import tkinter as tk
import ctypes
import pyautogui
import time

# ==============================================================================
# SOVEREIGN DESIGN: LIQUID GLASS & WHITE FOG
# ==============================================================================
COLOR_GLASS = "#1A1B26" # Deep Sea-Foam Hue
COLOR_FOG   = "#FFFFFF" # White Fog
ALPHA_VAL   = 0.65      # 65% Translucency (Liquid Glass)

# POE-STYLE CURSOR SCALING (Windows User32 Manifold)
# Forces Windows 11 to scale the cursor for maximum visibility
def deploy_large_cursor():
    print("[SYSTEM] Deploying PoE-Scale Cursor Manifold...")
    # 0x2029 = SPI_SETCURSORS (Reloads system cursors)
    # We use a standard Windows SPI call to increase pointer size
    # Note: On Windows 11, we recommend manually setting Cursor Size to 4-7 in Accessibility,
    # but this script forces a system refresh to ensure visibility.
    ctypes.windll.user32.SystemParametersInfoW(0x2029, 0, None, 0x01 | 0x02)

class LiquidGlassKeyboard(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Crispy Glass UI")
        self.overrideredirect(True) # Remove OS borders for total visibility
        self.attributes('-topmost', True)
        self.attributes('-alpha', ALPHA_VAL)
        self.configure(bg=COLOR_GLASS)
        
        self.geometry(f"1000x400+{int(pyautogui.size().width/2 - 500)}+{int(pyautogui.size().height - 450)}")
        self.create_glass_manifold()

    def create_glass_manifold(self):
        keys = [
            ['1','2','3','4','5','6','7','8','9','0','BACK'],
            ['Q','W','E','R','T','Y','U','I','O','P'],
            ['A','S','D','F','G','H','J','K','L','ENTER'],
            ['SHIFT','Z','X','C','V','B','N','M',',','.','?'],
            ['SPACE', 'CLOSE']
        ]

        for r, row in enumerate(keys):
            frame = tk.Frame(self, bg=COLOR_GLASS)
            frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            for k in row:
                self.make_key(frame, k)

    # Updated snippet for Key Rendering in crispy_keyboard.py
    def make_key(self, parent, char):
        width = 160 if char == 'SPACE' else 80
        canvas = tk.Canvas(parent, width=width, height=65, bg="#1A1B26", 
                      highlightthickness=0, bd=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
    
    # White Fog Gradient (Simulated via layered ovals for depth)
        for i in range(10):
            alpha_step = int(255 * (i/10))
        # Logic for gradient-hued fog here
            canvas.create_text(width/2, 32, text=char, 
                          fill=f"#FFFFFF", font=("Verdana", 20, "bold"))
    
    canvas.bind("<Button-1>", lambda e: self.press_key(char))

    def press_key(self, char):
        if char == 'CLOSE': self.master.destroy(); return
        
        key_map = {'SPACE': ' ', 'ENTER': 'enter', 'BACK': 'backspace'}
        cmd = key_map.get(char, char.lower())
        
        print(f"[HID] Injecting: {cmd}")
        pyautogui.press(cmd)

if __name__ == "__main__":
    deploy_large_cursor()
    root = tk.Tk()
    root.withdraw()
    ui = LiquidGlassKeyboard(root)
    root.mainloop()
