@echo off
echo ============================================
echo RAG Knowledge Analyst - Setup Script
echo ============================================
echo.

echo Step 1: Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please download Python from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✓ Python found

echo.
echo Step 2: Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

echo.
echo Step 3: Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Step 4: Installing dependencies...
pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed

echo.
echo Step 5: Checking for .env file...
if not exist .env (
    echo WARNING: .env file not found
    echo Creating .env from template...
    copy .env.example .env
    echo ✓ .env file created - PLEASE EDIT AND ADD YOUR GROQ_API_KEY
) else (
    echo ✓ .env file exists
)

echo.
echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo Next steps:
echo 1. Edit .env file and add your GROQ_API_KEY
echo    - Get one from https://console.groq.com
echo.
echo 2. Run the application:
echo    streamlit run app.py
echo.
echo ============================================
pause
