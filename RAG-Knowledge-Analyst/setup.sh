#!/bin/bash

echo "============================================"
echo "RAG Knowledge Analyst - Setup Script"
echo "============================================"
echo ""

echo "Step 1: Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed"
    echo "Please install Python3 from https://www.python.org/downloads/"
    exit 1
fi
echo "✓ Python found: $(python3 --version)"

echo ""
echo "Step 2: Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

echo ""
echo "Step 3: Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Step 4: Installing dependencies..."
pip install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed"

echo ""
echo "Step 5: Checking for .env file..."
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found"
    echo "Creating .env from template..."
    cp .env.example .env
    echo "✓ .env file created - PLEASE EDIT AND ADD YOUR GROQ_API_KEY"
else
    echo "✓ .env file exists"
fi

echo ""
echo "============================================"
echo "Setup Complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your GROQ_API_KEY"
echo "   - Get one from https://console.groq.com"
echo ""
echo "2. Run the application:"
echo "   streamlit run app.py"
echo ""
echo "============================================"
