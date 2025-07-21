@echo off
REM =============================================================================
REM © 2025 Kashif Ali Siddiqui, Pakistan
REM Developed by: Kashif Ali Siddiqui 
REM
REM Github: https://github.com/ksiddiqui
REM LinkedIn: https://www.linkedin.com/in/ksiddiqui
REM Email: kashif.ali.siddiqui@gmail.com
REM Dated: July, 2025 
REM -----------------------------------------------------------------------------
REM This source code is the property of Kashif Ali Siddiqui and is confidential.
REM Unauthorized copying or distribution of this file, via any medium, is strictly prohibited.
REM =============================================================================
REM
REM ChatBot Document Search - Startup Script
REM This batch file activates the virtual environment and starts the API server
REM Usage: run.bat [--install]
REM   --install: Activate venv, install dependencies from requirements.txt, and exit
REM =============================================================================

REM Check for --install argument
if "%1"=="--install" (
    echo.
    echo ========================================
    echo   Installing Dependencies
    echo ========================================
    echo.
    goto :install_mode
)

echo.
echo ========================================
echo   ChatBot Document Search Server
echo ========================================
echo.
echo Starting application...
echo.

REM Step 1: Activate virtual environment
echo [STEP 1] Activating virtual environment...
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    echo ✓ Virtual environment activated successfully
) else (
    echo ✗ Virtual environment not found at '.venv\Scripts\activate.bat'
    echo Please ensure the virtual environment is created in the '.venv' directory
    pause
    exit /b 1
)

echo.
echo [STEP 2] Starting API server...
echo Running: python src\api_server.py
echo.

REM Step 2: Run the API server
python src\api_server.py

REM Check if the server exited with an error
if %ERRORLEVEL% neq 0 (
    echo.
    echo ✗ API server exited with error code: %ERRORLEVEL%
    echo Please check the error messages above
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ✓ API server stopped successfully
echo.
echo Thank you for using ChatBot Document Search!
echo.
pause
exit /b 0

REM =============================================================================
REM Install Mode - Activated with --install argument
REM =============================================================================
:install_mode
echo [STEP 1] Activating virtual environment...
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    echo ✓ Virtual environment activated successfully
) else (
    echo ✗ Virtual environment not found at '.venv\Scripts\activate.bat'
    echo Please ensure the virtual environment is created in the '.venv' directory
    pause
    exit /b 1
)

echo.
echo [STEP 2] Installing dependencies from requirements.txt...
if exist "requirements.txt" (
    pip install -r requirements.txt
    if %ERRORLEVEL% equ 0 (
        echo ✓ Dependencies installed successfully
    ) else (
        echo ✗ Failed to install dependencies
        echo Error code: %ERRORLEVEL%
        pause
        exit /b %ERRORLEVEL%
    )
) else (
    echo ✗ requirements.txt not found
    echo Please ensure requirements.txt exists in the current directory
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo All dependencies have been installed successfully.
echo You can now run 'run.bat' without arguments to start the server.
echo.
pause
exit /b 0