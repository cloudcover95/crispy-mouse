# Crispy Mouse - Sovereign Predictor Setup Guide

## Overview

The Crispy Mouse SDK includes **Sovereign Predictor** — an ultra-optimized local LLM inference engine powered by **Phi-3 Mini** (1.4B parameters). This enables on-device word prediction without requiring cloud services or GPUs.

### Features

✓ **Phi-3 Mini (1.4B)** - Smallest quantized LLM with high quality  
✓ **512 Context Window** - Ultra-fast inference (~100ms)  
✓ **Thread Cancellation** - Kill old predictions instantly when user types  
✓ **Deterministic Output** - Temperature 0.2 for consistent, logical completions  
✓ **CPU-Optimized** - Runs on any Windows 11 machine  
✓ **3-Word Predictions** - Engineered prompt for discrete options  

---

## Setup Instructions

### 1. Install Dependencies

Run `setup_local.bat` (Windows 11):
```batch
setup_local.bat
```

This will install:
- `llama-cpp-python` - Core inference engine
- `pyserial`, `pyautogui`, `tobii-research` - Existing dependencies

### 2. Download Phi-3 Mini Model

You need a quantized `.gguf` model file. **Recommended: Phi-3 Mini (1.4B)**

```
Model:  phi-3-mini-4k-instruct-q4.gguf
Source: https://huggingface.co/TheBloke/phi-3-mini-4k-instruct-GGUF
Size:   ~2.3GB
Type:   Q4 quantization (excellent quality/speed tradeoff)
```

**Alternative Models:**

| Model | Size | Speed | Quality | Recommended |
|-------|------|-------|---------|------------|
| TinyLlama-1.1B-Q4 | 0.4GB | ⚡⚡⚡ | ⭐⭐ | Fast testing |
| Phi-3-Mini-Q4 | 2.3GB | ⚡⚡ | ⭐⭐⭐⭐⭐ | **Best choice** |
| Mistral-7B-Q4 | 4.2GB | ⚡ | ⭐⭐⭐⭐ | High quality |

### 3. Create Models Directory & Place File

```powershell
# PowerShell (Windows 11)
mkdir models
cd models

# Download phi-3-mini-4k-instruct-q4.gguf from HuggingFace
# Place file as: models/phi-3-mini-4k-instruct-q4.gguf
```

### 4. Launch Keyboard with Predictions

```powershell
# Activate environment
.venv\Scripts\activate

# Run with Sovereign Predictor
python crispy_keyboard.py
```

The keyboard will:
1. Load Phi-3 Mini in foreground (quick with 512 ctx window)
2. Display "[ Loading... ]" briefly
3. Show "[ Ready ]" when predictions are active
4. Display word suggestions as you type

---

## Usage

### Prediction Buttons

As you type on the virtual keyboard:

```
[ hello  ] [ world  ] [ everyone ]
QWERTY Keyboard
```

Click any button to inject that word + space into the active window.

### How It Works

```
User types: "hel"
    ↓
Keyboard buffers "hel"
    ↓
request_completion("hel") called
    ↓
Old predictions killed (thread cancellation)
    ↓
New inference spawned in background thread
    ↓
Phi-3 Mini generates: "hello, help, helmet"
    ↓
UI updates buttons (NO LAG)
    ↓
User clicks "hello" → text injected
```

### Performance Tips

**Ultra-Fast Predictions:**
- Phi-3 Mini with 512 context = ~100-150ms per prediction
- Thread cancellation prevents wasted computation
- Low temperature (0.2) avoids random tokens
- n_threads should match your CPU core count

**Better Quality:**
- Use Q5 quantization instead of Q4 (~3GB)
- Increase max_tokens to 20 (slower but longer words)
- Lower temperature further (0.1) for safety

---

## Architecture

### SovereignPredictor Class

```python
# Initialize
predictor = SovereignPredictor(
    model_path="./models/phi-3-mini-4k-instruct-q4.gguf",
    n_threads=6  # Match your CPU cores
)

# Request predictions (kills old threads)
predictor.request_completion(
    context_buffer="hello w",
    callback=update_ui_buttons
)
```

### Key Features

**Thread Cancellation:**
```python
# If user types "he" → "hel" → "hell" very quickly
# Only the LAST request generates predictions
# Previous threads are killed via cancel_flag
if self.current_task and self.current_task.is_alive():
    self.cancel_flag.set()
    self.current_task.join(timeout=0.1)
```

**Engineered Prompt:**
```python
prompt = "Complete this text naturally. Reply ONLY with 3 single-word options separated by commas.\nText: hello w"
# Forces output like: "world, window, whisper"
```

**Low Temperature:**
```python
temperature=0.2  # Deterministic, logical completions
# Not 0.7 which could produce: "world, xyzzzzz, pizza"
```

---

## Customization

### Adjust CPU Threads

Edit `crispy_keyboard.py`:
```python
self.predictor = initialize_predictor(
    model_path="./models/phi-3-mini-4k-instruct-q4.gguf",
    n_threads=8  # Change based on your CPU
)
```

**CPU Core Count Reference:**
- Dual-core (16-bit CPU): `n_threads=2`
- Quad-core (i5): `n_threads=4`
- 6-core (R5 5600X): `n_threads=6`
- 8-core (R7): `n_threads=8`

### Change Model Path

Edit `crispy_keyboard.py`:
```python
self.predictor = initialize_predictor(
    model_path="./models/my-mistral-model.gguf",
    n_threads=6
)
```

### Tweak Inference Parameters

Edit `crispy_llm.py`:
```python
def _generate_predictions(self, context_buffer, callback):
    # Adjust these:
    response = self.llm(
        prompt,
        max_tokens=15,       # Longer completions (slower)
        temperature=0.2,     # Lower = more consistent
        stop=["\n", ".", "!"],
    )
```

---

## Troubleshooting

### "Model not found"
- Check `models/phi-3-mini-4k-instruct-q4.gguf` exists
- Verify file path (should be relative to project root)
- Confirm file downloaded completely (2.3GB)

### Predictions are slow (>500ms)
- First prediction is loaded + inference (2-3s normal)
- Subsequent predictions should be <200ms
- Reduce `n_threads` if CPU throttling
- Use smaller model (TinyLlama) for testing

### High CPU usage
- Phi-3 Mini uses ~1-2 cores during inference
- Other threads are killed (not accumulating)
- Normal behavior — predictions complete quickly
- Close other apps if needed

### Keyboard won't start
- Check Python version: `python --version` (need 3.8+)
- Verify llama-cpp-python installed: `pip list`
- Try running from project directory: `cd /workspaces/crispy-mouse`

### Nonsensical predictions
- Temperature too high (change 0.2 → 0.1)
- Model too small (upgrade to Phi-3 Standard or Mistral)
- Prompt context needs more examples

---

## Files Modified

```
crispy-mouse/
├── crispy_llm.py              # SovereignPredictor class
├── crispy_keyboard.py         # Integration + callbacks
├── models/
│   └── phi-3-mini-4k-instruct-q4.gguf  # Downloaded model
├── setup_local.bat            # Installation script
├── requirements.txt           # llama-cpp-python
└── LLM_SETUP.md              # This guide
```

---

## References

- **Llama.cpp**: https://github.com/ggerganov/llama.cpp
- **Llama-cpp-python**: https://github.com/abetlen/llama-cpp-python
- **Phi-3 Models**: https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf
- **TheBloke GGUF**: https://huggingface.co/TheBloke (quantized models)

---

**Last Updated:** March 28, 2026  
**Version:** Crispy Mouse v1.1 Sovereign Release  
**Predictor:** SovereignPredictor (Phi-3 Mini Optimized)
