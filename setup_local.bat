@echo off
echo --- JuniorCloud LLC: Crispy Mouse Sovereign Release v1.1 ---

:: 1. Verify Python Installation Manifold
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] ERROR: Python 3 not found.
    echo [!] Download Python 3.10 from python.org ^(Check "Add to PATH"^).
    pause
    exit /b
)

:: 2. Instantiate Sovereign Virtual Environment
if not exist .venv (
    echo [*] Instantiating Sovereign VENV...
    python -m venv .venv
)

:: Activate VENV
call .venv\Scripts\activate

:: 3. Driver and HID Tensor Injections (Windows 11 Local)
echo [*] Injecting Optical ^& HID Tensors...
echo [*] Upgrading pip...
pip install --upgrade pip

:: Install dependencies from requirements
echo [*] Installing Tobii ^& PyAutoGUI manifold...
pip install tobii-research pyautogui screeninfo pyserial

echo [*] Liquid Glass UI ^& PoE Cursor Ready.
echo --------------------------------------------------
echo [!] TO RUN CALIBRATION (Auto-launches keyboard):
echo [!]    call .venv\Scripts\activate
echo [!]    python crispy_calibrate.py
echo --------------------------------------------------
echo [!] TO START SENSOR FUSION HUB (Head Tracking):
echo [!]    call .venv\Scripts\activate
echo [!]    python crispy_hub.py
echo --------------------------------------------------
echo [!] TO START SOVEREIGN HUB V3 (Tobii + Head Tracking):
echo [!]    call .venv\Scripts\activate
echo [!]    python crispy_hub_v3.py
echo --------------------------------------------------
echo [!] TO LAUNCH LIQUID GLASS KEYBOARD:
echo [!]    call .venv\Scripts\activate
echo [!]    python crispy_keyboard.py
echo --------------------------------------------------
echo [!] Run 'python crispy_calibrate.py' to launch the manifold.
pause
