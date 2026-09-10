@echo off
title SwarSatya - Automated Test Suite
cd /d "%~dp0"

echo ===================================================
echo   SwarSatya Test Suite (Pytest Verification)
echo ===================================================
echo Directory: %CD%
echo.

if exist "%~dp0venv\Scripts\python.exe" (
    set "PYTHON_EXEC=%~dp0venv\Scripts\python.exe"
) else (
    set "PYTHON_EXEC=python"
)

"%PYTHON_EXEC%" -m pytest -v

echo.
echo Test suite execution completed.
pause
