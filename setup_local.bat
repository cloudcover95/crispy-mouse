@echo off
echo --- JuniorCloud LLC: Crispy Mouse Sovereign Release v2.0 ---
setlocal enabledelayedexpansion

:: 1. Verify Python Installation Manifold
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] ERROR: Python 3 not found.
    echo [!] Download Python 3.11+ from python.org ^(Check "Add to PATH"^).
    pause
    exit /b
)

:: 2. Ensure Fresh Virtual Environment for Clean Dependency Tree
if exist .venv (
    echo [*] Removing existing .venv for clean dependency tree...
    rmdir /s /q .venv
)

echo [*] Creating clean virtual environment...
python -m venv .venv

:: 3. Activate VENV
call .venv\Scripts\activate

:: 4. Upstream Packaging Toolchain
echo [*] Upgrading pip/setuptools/wheel...
pip install --upgrade pip setuptools wheel

:: 5. Install from generated wheel artifact (preferred)
if exist dist\*.whl (
    set "WHEELPATH="
    for %%F in (dist\*.whl) do set "WHEELPATH=%%F"
    if defined WHEELPATH (
        echo [*] Uninstalling old crispy-mouse package (if installed)...
        pip uninstall -y crispy-mouse
        echo [*] Installing crispy-mouse SDK directly from wheel: !WHEELPATH!
        pip install --upgrade --force-reinstall "!WHEELPATH!"
    ) else (
        echo [!] No wheel found in dist\; skipping direct wheel install.
    )
) else (
    echo [!] No dist\*.whl found. Run 'python -m build' first to generate wheel.
)

:: 6. Enforce runtime dependency graph (fast path)
echo [*] Ensuring required runtime dependencies are present by installing from pyproject extras.
pip install pyserial pyautogui screeninfo tobii-research

:: 7. Optional local LLM engine as explicit fallback
echo [*] Installing local LLM inference engine (llama-cpp-python)...
pip install llama-cpp-python

echo [*] Setup complete. To run:
echo    call .venv\Scripts\activate && python crispy_calibrate.py
echo    call .venv\Scripts\activate && python crispy_hub.py
echo    call .venv\Scripts\activate && python crispy_hub_v3.py
echo    call .venv\Scripts\activate && python crispy_keyboard.py
echo --------------------------------------------------
   
pause
