@echo off
title Air Attack Game - Check & Run
color 0A

:: ============================================
:: CONFIGURABLE VARIABLES
:: ============================================
set "PYTHON_VERSION=3.12.8"
set "PYTHON_INSTALLER=python-%PYTHON_VERSION%-amd64.exe"
set "PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe"
set "PYGAME_VERSION=2.6.1"
:: ============================================

echo ================================================
echo        AIR ATTACK GAME - CHECK & RUN
echo ================================================
echo.

:: Check if running as administrator (only needed for Python installation)
net session >nul 2>&1
set "IS_ADMIN=%errorlevel%"

:: Step 1: Check Python
echo [1/4] Checking Python...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python not found!
    goto :install_python
)

:: Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set "PY_VER=%%i"
for /f "tokens=1,2 delims=." %%a in ("%PY_VER%") do (
    set "PY_MAJOR=%%a"
    set "PY_MINOR=%%b"
)

if %PY_MAJOR% EQU 3 (
    if %PY_MINOR% GTR 12 (
        echo [!] Python %PY_VER% detected (pygame only supports up to 3.12)
        goto :install_python
    ) else (
        echo [OK] Python %PY_VER% found
        set "PYTHON_CMD=python"
        goto :check_uv
    )
) else (
    echo [!] Python 3.x required
    goto :install_python
)

:install_python
echo.
echo [!] Need to install Python %PYTHON_VERSION%
if %IS_ADMIN% neq 0 (
    echo.
    echo Requesting administrator privileges...
    timeout /t 2 /nobreak >nul
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo Downloading Python %PYTHON_VERSION%...
powershell -Command "Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_INSTALLER%'"

if exist "%PYTHON_INSTALLER%" (
    echo Installing Python (this may take a minute)...
    start /wait %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_launcher=0
    del %PYTHON_INSTALLER%
    echo [OK] Python installed
    set "PYTHON_CMD=python"
) else (
    echo [ERROR] Failed to download Python
    echo Please install manually from: %PYTHON_URL%
    pause
    exit /b 1
)

:check_uv
echo.
echo [2/4] Checking uv package manager...

uv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] uv not found, installing...
    %PYTHON_CMD% -m pip install --user uv --quiet
    if %errorlevel% equ 0 (
        echo [OK] uv installed
        :: Add to PATH
        set "PATH=%USERPROFILE%\AppData\Local\Programs\Python\Python312\Scripts;%PATH%"
        set "PATH=%APPDATA%\Python\Scripts;%PATH%"
    ) else (
        echo [WARNING] pip install failed, trying alternative...
        powershell -Command "Invoke-WebRequest -Uri 'https://astral.sh/uv/install.ps1' -OutFile 'install_uv.ps1'"
        powershell -ExecutionPolicy Bypass -File "install_uv.ps1"
        del install_uv.ps1 2>nul
        echo [OK] uv installed via PowerShell
    )
) else (
    uv --version
    echo [OK] uv found
)

:check_venv
echo.
echo [3/4] Checking virtual environment...

if exist "game_env\Scripts\python.exe" (
    echo [OK] Virtual environment exists
) else (
    echo [!] Creating virtual environment...
    %PYTHON_CMD% -m uv venv game_env --python %PYTHON_VERSION%
    if %errorlevel% equ 0 (
        echo [OK] Virtual environment created
    ) else (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
)

:check_pygame
echo.
echo [4/4] Checking pygame...

:: Activate virtual environment
call game_env\Scripts\activate.bat

python -c "import pygame" >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Installing pygame...
    pip install pygame==%PYGAME_VERSION% --quiet
    if %errorlevel% equ 0 (
        echo [OK] Pygame installed
    ) else (
        echo Installing latest pygame version...
        pip install pygame --quiet
        echo [OK] Pygame installed
    )
) else (
    python -c "import pygame; print(f'[OK] Pygame {pygame.version.ver} found')"
)

echo.
echo ================================================
echo        STARTING GAME...
echo ================================================
echo.

:: Run the game
uv run main.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Game failed to start
    echo.
    echo Try running: uv run main.py manually
    echo.
    pause
    exit /b 1
)

pause