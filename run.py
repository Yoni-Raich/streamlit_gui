import os
import sys
import subprocess
from pathlib import Path

def run_app():
    """Run the CodeAce application."""
    # Check if virtual environment exists
    if not os.path.exists("venv"):
        print("Virtual environment not found. Please run install script first.")
        sys.exit(1)
    
    # Get the path to the virtual environment's Python executable
    if sys.platform == "win32":
        venv_python = os.path.join("venv", "Scripts", "python.exe")
    else:
        venv_python = os.path.join("venv", "bin", "python")
    
    print("Starting CodeAce application...")
    subprocess.run([venv_python, "-m", "streamlit", "run", "streamlit_gui.py"], check=True)

if __name__ == "__main__":
    run_app() 