# Stop on error
$ErrorActionPreference = "Stop"

# Check if virtual environment exists
if (!(Test-Path "venv")) {
    Write-Host "Virtual environment not found. Please run install script first."
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..."
.\venv\Scripts\Activate.ps1

# Run the application
Write-Host "Starting CodeAce application..."
streamlit run streamlit_gui.py 