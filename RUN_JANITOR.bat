@echo off
set "SCRIPT_DIR=%~dp0"
set "PYTHON_EXE=%SCRIPT_DIR%_portable_runtimes\windows_python\python.exe"
set "SCRIPT=%SCRIPT_DIR%janitor.py"

echo Checking for Portable Python...
if exist "%PYTHON_EXE%" (
    echo Found Portable Python. Launching...
    "%PYTHON_EXE%" "%SCRIPT%"
) else (
    echo [WARNING] Portable Python not found at:
    echo %PYTHON_EXE%
    echo.
    echo Attempting to use system-installed Python...
    python "%SCRIPT%"
    if errorlevel 1 (
        echo.
        echo [ERROR] No Python runtime found.
        echo Please ensure _portable_runtimes folder is set up correctly.
    )
)

pause
