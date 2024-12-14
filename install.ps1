# Stop on error
$ErrorActionPreference = "Stop"

Write-Host "Starting CodeAce installation..."

# Check if Python is installed
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python is not installed. Please install Python first."
    exit 1
}

# Clone the repository
$REPO_URL = "https://github.com/your-repo/codeace.git"  # Replace with your actual repo URL
$INSTALL_DIR = "codeace_app"

Write-Host "Cloning repository..."
git clone $REPO_URL $INSTALL_DIR
Set-Location $INSTALL_DIR

# Create and activate virtual environment
Write-Host "Creating virtual environment..."
python -m venv venv
.\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..."
python -m pip install --upgrade pip

# Install requirements
Write-Host "Installing requirements..."
pip install -r requirements.txt

# Install CodeAce package
Write-Host "Installing CodeAce package..."
if (Test-Path "codeace_pkg") {
    Set-Location codeace_pkg
    $pkg = Get-ChildItem -Filter "*.gz" | Select-Object -First 1
    if ($pkg) {
        pip install $pkg.FullName
    }
    Set-Location ..
} else {
    Write-Host "Warning: codeace_pkg directory not found"
}

Write-Host "Installation completed successfully!"
Write-Host "To run the application:"
Write-Host "1. Activate the virtual environment: .\venv\Scripts\Activate.ps1"
Write-Host "2. Run: streamlit run streamlit_gui.py" 