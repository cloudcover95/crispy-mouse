import tkinter as tk
import pyautogui
import ctypes
from crispy_llm import initialize_predictor, get_predictor

# ==============================================================================
# STATIC SOVEREIGN DESIGN: LIQUID GLASS (Zero Animation)
# ==============================================================================
COLOR_GLASS = "#1A1B26" # Deep Sea-Foam Hue
COLOR_FOG   = "#E0E0E0" # Static White Fog Text
ALPHA_VAL   = 0.70      # 70% Translucency 

def deploy_large_cursor():
    # Forces Windows to refresh the cursor size manifold
    ctypes.windll.user32.SystemParametersInfoW(0x2029, 0, None, 0x01 | 0x02)

class SovereignKeyboard(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Crispy Glass UI - BitNet LLM Inference")
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.attributes('-alpha', ALPHA_VAL)
        self.configure(bg=COLOR_GLASS)
        
        # Lock to bottom center of screen
        screen_w, screen_h = pyautogui.size()
        self.geometry(f"1000x450+{int(screen_w/2 - 500)}+{int(screen_h - 480)}")
        
        self.current_word_buffer = ""
        
        # Initialize LLM Predictor (non-blocking)
        self.predictor = None
        self.init_predictor_async()
        
        self.create_glass_manifold()

    def create_glass_manifold(self):
        # 1. LLM PREDICTION ROW (The Macro-Word Targets)
        pred_frame = tk.Frame(self, bg=COLOR_GLASS)
        pred_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        self.pred_buttons = []
        for i in range(3):
            btn = tk.Button(pred_frame, text=f"[ LOADING... ]", width=15, height=2,
                            bg="#2A2B3C", fg="#C0F010", font=("Verdana", 14, "bold"),
                            relief=tk.FLAT, activebackground="#404060")
            btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
            # Bind prediction injection
            btn.config(command=lambda b=btn, idx=i: self.inject_prediction(b.cget("text"), idx))
            self.pred_buttons.append(btn)

        # 2. STATIC QWERTY MANIFOLD
        keys = [
            ['1','2','3','4','5','6','7','8','9','0','BACK'],
            ['Q','W','E','R','T','Y','U','I','O','P'],
            ['A','S','D','F','G','H','J','K','L','ENTER'],
            ['Z','X','C','V','B','N','M',',','.','?'],
            ['SPACE', 'CLOSE']
        ]

        for row in keys:
            frame = tk.Frame(self, bg=COLOR_GLASS)
            frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            for k in row:
                width = 15 if k == 'SPACE' else 4
                btn = tk.Button(frame, text=k, width=width, height=2,
                                bg=COLOR_GLASS, fg=COLOR_FOG, font=("Verdana", 18, "bold"),
                                relief=tk.FLAT, activebackground="#303040", activeforeground="#FFFFFF")
                btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=1, pady=1)
                btn.config(command=lambda char=k: self.press_key(char))

    def inject_prediction(self, word, idx=0):
        """Inject predicted word into active window"""
        if word.startswith("[") or word == "[ ... ]": 
            return # Ignore placeholder
        
        word = word.strip()
        if word:
            pyautogui.typewrite(word, interval=0.02)
            pyautogui.press('space')
            self.current_word_buffer = ""
            self.clear_predictions()

    def clear_predictions(self):
        """Clear all prediction buttons"""
        for btn in self.pred_buttons:
            btn.config(text="[ ... ]", state=tk.DISABLED)

    def init_predictor_async(self):
        """Initialize Sovereign Predictor asynchronously"""
        try:
            # Initialize with Phi-3 Mini (1.4B) model
            self.predictor = initialize_predictor(
                model_path="./models/phi-3-mini-4k-instruct-q4.gguf",
                n_threads=6  # Adjust based on CPU cores
            )
            print("[LLM] Predictor initialized")
        except Exception as e:
            print(f"[LLM] Initialization error: {e}")

    def request_llm_prediction(self):
        """Trigger async LLM prediction for current word buffer"""
        if not self.predictor or not self.predictor.is_loaded:
            return
        
        # Build context from word buffer
        context = self.current_word_buffer.strip()
        if len(context) < 2:
            return
        
        def update_predictions(predictions):
            """Callback to update UI with predictions"""
            for idx, pred in enumerate(predictions[:3]):
                if idx < len(self.pred_buttons):
                    # Truncate long predictions
                    text = str(pred)[:18] if pred and pred != "..." else "..."
                    self.pred_buttons[idx].config(text=f"[ {text} ]")
        
        # Non-blocking prediction (kills previous thread if active)
        self.predictor.request_completion(
            context_buffer=context,
            callback=update_predictions
        )

    def press_key(self, char):
        if char == 'CLOSE': 
            self.master.destroy()
            return
        
        if char == 'BACK':
            pyautogui.press('backspace')
            self.current_word_buffer = self.current_word_buffer[:-1]
        elif char == 'SPACE':
            pyautogui.press('space')
            self.current_word_buffer = ""
            self.clear_predictions()
        elif char == 'ENTER':
            pyautogui.press('enter')
            self.current_word_buffer = ""
        else:
            pyautogui.press(char.lower())
            self.current_word_buffer += char.lower()
            self.request_llm_prediction() # Trigger async LLM call

if __name__ == "__main__":
    deploy_large_cursor()
    root = tk.Tk()
    root.withdraw()
    ui = SovereignKeyboard(root)
    root.mainloop()