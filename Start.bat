@echo off
title Air Attack Game
color 0A

:: Check for Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    cls
    echo.
    echo =======================================================
    echo           PYTHON NOT FOUND!
    echo =======================================================
    echo.
    echo This game requires Python to run.
    echo.
    set /p install_python="Do you want to install Python? (Y/N): "
    
    if /i "%install_python%"=="Y" (
        echo.
        echo Launching setup...
        timeout /t 2 >nul
        call setup.bat
        exit /b
    ) else (
        echo.
        echo Returning to menu...
        timeout /t 2 >nul
        goto MENU
    )
)

call :SHOW_FOOTER
goto MENU

:SHOW_FOOTER
echo.
echo =======================================================
echo    (c) 2026 Air Attack Game - For Personal Use Only
echo    THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY
echo =======================================================
echo.
exit /b

:MENU
cls
echo.
echo =======================================================
echo                 AIR ATTACK GAME
echo =======================================================
echo.
echo               1. Launch Game
echo               2. Credits
echo               3. Help
echo               4. Exit
echo.
call :SHOW_FOOTER
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto LAUNCH
if "%choice%"=="2" goto CREDITS
if "%choice%"=="3" goto HELP
if "%choice%"=="4" goto EXIT

echo.
echo [ERROR] Invalid choice! Please enter 1, 2, 3, or 4.
timeout /t 2 >nul
goto MENU

:LAUNCH
cls
echo.
echo =======================================================
echo                 STARTING GAME...
echo =======================================================
echo.

uv run main.py 2>nul
if %errorlevel% neq 0 (
    echo.
    echo [INFO] uv not found, trying python directly...
    timeout /t 1 >nul
    python main.py
    if %errorlevel% neq 0 (
        echo.
        echo [ERROR] Game failed to start
        echo.
        echo Try running: python main.py manually
        echo.
        pause
        goto MENU
    )
)

echo.
echo Game exited successfully.
echo.
pause
goto MENU

:CREDITS
cls
echo.
echo =======================================================
echo                     CREDITS
echo =======================================================
echo.
echo    Game Title: Air Attack Game
echo    Version: 1.0
echo.
echo    Developed by: M. Dallen Shelly
echo    Programming Language: Python
echo    Package Manager: uv
echo.
echo    Special Thanks:
echo    - All playtesters and contributors
echo    - Open source community
echo    - Pygame community
echo    - DeepSeek
echo.
echo.
echo.
echo ========== REQUEST TO ALL PLAYERS =====================
echo [ Please do NOT copy or distribute this game.         ]
echo [ This game is made with hard work by a SINGLE person.]
echo [ Contains nearly 5,000 to 12,000 lines of code.      ] 
echo [ Please use it with respect.                         ]
echo =======================================================
echo.
call :SHOW_FOOTER
echo.
echo        Press any key to return to menu...
pause >nul
goto MENU

:HELP
cls
echo.
echo =======================================================
echo                      HELP
echo =======================================================
echo.
echo              CONTACT INFORMATION
echo =======================================================
echo.
echo    Developer: M. Dallen Shelly
echo    Email: dallenshelly@proton.me
echo.
echo =======================================================
echo              SYSTEM REQUIREMENTS
echo =======================================================
echo.
echo    [Hardware Requirements]
echo    - OS(Windows only)
echo    - RAM: 2 GB (Minimum), 6 GB (Recommended)
echo    - Processer: 0.79 GHz (Minimum), 2.0GHz (Recommended)
echo    - Storage: 30MB (Minimum), 100MB (Recommended)
echo    - Drive Type: HDD (Minimum), SSD (Recommended)
echo.
echo    [Required Software]
echo    - Python 3.12 or higher
echo    - uv (Python package manager)
echo    - venv (Virtual Environment)
echo.
echo    [Required Python Packages]
echo    - pygame
echo    - numpy
echo.
echo =======================================================
echo              INSTALLATION GUIDE
echo =======================================================
echo.
echo    1. Install Python 3.12 from python.org
echo    2. Install uv: pip install uv
echo    3. Run setup.bat to create venv and install packages
echo    4. Launch the game from this menu
echo.
echo =======================================================
echo              SUPPORT
echo =======================================================
echo.
echo    For issues, questions, or feedback:
echo    Email: dallenshelly@proton.me
echo.
echo    Please include:
echo    - Error messages (if any)
echo    - Your system specs
echo    - Steps to reproduce the issue
echo.
echo =======================================================
echo.
call :SHOW_FOOTER
echo.
echo        Press any key to return to menu...
pause >nul
goto MENU

:EXIT
cls
echo.
echo =======================================================
echo       Thank you for playing Air Attack Game!
echo =======================================================
echo.
call :SHOW_FOOTER
echo.
echo    Press any key to exit...
pause >nul
exit /b 0
