# KumbuK Backend & Frontend Integration
# Quick Start Script for Windows PowerShell
# Updated for new directory structure (frontend/ and backend/ separated)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   KumbuK - Quick Start Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$projectRoot = $PSScriptRoot | Split-Path
Set-Location $projectRoot

# Function to check if a command exists
function Test-Command {
    param($command)
    try {
        if (Get-Command $command -ErrorAction Stop) {
            return $true
        }
    } catch {
        return $false
    }
}

# Check Python
Write-Host "[1/5] Checking Python..." -ForegroundColor Yellow
if (Test-Command python) {
    $pythonVersion = python --version
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Python not found! Please install Python 3.9+" -ForegroundColor Red
    exit 1
}

# Check Node.js
Write-Host "[2/5] Checking Node.js..." -ForegroundColor Yellow
if (Test-Command node) {
    $nodeVersion = node --version
    Write-Host "✓ Node.js found: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Node.js not found! Please install Node.js 16+" -ForegroundColor Red
    exit 1
}

# Setup Backend
Write-Host "[3/5] Setting up Backend..." -ForegroundColor Yellow
Set-Location "$projectRoot\backend"

# Check if virtual environment exists
if (-Not (Test-Path "venv")) {
    Write-Host "  Creating virtual environment..." -ForegroundColor Cyan
    python -m venv venv
}

# Activate virtual environment and install dependencies
Write-Host "  Installing Python dependencies..." -ForegroundColor Cyan
& "$projectRoot\backend\venv\Scripts\Activate.ps1"
pip install -r requirements.txt --quiet --disable-pip-version-check

Write-Host "✓ Backend setup complete!" -ForegroundColor Green

# Return to root
Set-Location $projectRoot

# Setup Frontend
Write-Host "[4/5] Setting up Frontend..." -ForegroundColor Yellow
Set-Location "$projectRoot\frontend"

if (-Not (Test-Path "node_modules")) {
    Write-Host "  Installing npm dependencies..." -ForegroundColor Cyan
    npm install --silent
} else {
    Write-Host "  Dependencies already installed" -ForegroundColor Cyan
}
Write-Host "✓ Frontend setup complete!" -ForegroundColor Green

# Return to root
Set-Location $projectRoot

# Final instructions
Write-Host ""
Write-Host "[5/5] Setup Complete! 🎉" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Next Steps:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Start the Backend (Terminal 1):" -ForegroundColor Yellow
Write-Host "   cd backend" -ForegroundColor White
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "   python -m uvicorn app.main:app --reload" -ForegroundColor White
Write-Host ""
Write-Host "2. Start the Frontend (Terminal 2):" -ForegroundColor Yellow
Write-Host "   cd frontend" -ForegroundColor White
Write-Host "   npx nx start consumer-app" -ForegroundColor White
Write-Host ""
Write-Host "3. Open on Mobile:" -ForegroundColor Yellow
Write-Host "   - Install Expo Go app" -ForegroundColor White
Write-Host "   - Scan QR code" -ForegroundColor White
Write-Host "   - Tap 'Open Chat' button in app" -ForegroundColor White
Write-Host ""
Write-Host "4. API Documentation:" -ForegroundColor Yellow
Write-Host "   http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "For detailed instructions, see:" -ForegroundColor Cyan
Write-Host "  - docs/README_INTEGRATION.md" -ForegroundColor White
Write-Host "  - docs/QUICK_REFERENCE.md" -ForegroundColor White
Write-Host ""
