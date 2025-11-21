#!/bin/bash

# Simple script to run the bot

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create a .env file from .env.example:"
    echo "  cp .env.example .env"
    echo "Then edit .env and add your BOT_TOKEN"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Run the bot
echo "🚀 Starting bot..."
python main.py
