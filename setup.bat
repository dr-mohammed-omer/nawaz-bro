@echo off
setlocal

set PYTHON_PATH="C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe"

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating Python virtual environment...
    %PYTHON_PATH% -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
venv\Scripts\pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

REM Start Flask application
echo Starting Flask application...
venv\Scripts\python app.py

pause