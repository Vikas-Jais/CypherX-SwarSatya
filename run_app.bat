@echo off
title SwarSatya - Voice Security Engine Launcher
cd /d "%~dp0"

echo ===================================================
echo   SwarSatya (स्वरसत्य) — Voice Security Engine
echo ===================================================
echo Application Directory: %CD%
echo.

if exist "%~dp0venv\Scripts\python.exe" (
    set "PYTHON_EXEC=%~dp0venv\Scripts\python.exe"
) else (
    set "PYTHON_EXEC=python"
)

echo Starting Native Desktop Application...
"%PYTHON_EXEC%" "%~dp0app.py"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] SwarSatya exited with error code %ERRORLEVEL%.
    pause
)
