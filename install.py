import os
import sys
import subprocess
import venv
from pathlib import Path

def check_python():
    """Check if Python is installed."""
    try:
        subprocess.run([sys.executable, "--version"], check=True)
        return True
    except subprocess.CalledProcessError:
        print("Python is not installed. Please install Python first.")
        return False

def check_git():
    """Check if Git is installed."""
    try:
        subprocess.run(["git", "--version"], check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Git is not installed. Please install Git first.")
        return False

def get_env_vars():
    """Check and collect environment variables."""
    required_vars = [
        "AZURE_OPENAI_ENDPOINT",
        "AZ_OPENAI_API_KEY",
        "AZ_OPENAI_API_VERSION",
        "AZ_OPENAI_LLM_4_O_MINI",
        "AZ_OPENAI_LLM_4_O"
    ]
    
    env_content = ""
    for var in required_vars:
        value = os.environ.get(var)
        if not value:
            value = input(f"Enter value for {var}: ")
            os.environ[var] = value
        env_content += f"{var}={value}\n"
    
    # Save to .env file in the installation directory
    env_path = os.path.join(os.getcwd(), ".env")
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(env_content)
    print(f"Environment variables have been saved to {env_path}")

def clone_repository(repo_url, install_dir):
    """Clone the repository."""
    print(f"Cloning repository from {repo_url}...")
    try:
        if os.path.exists(install_dir):
            print(f"Directory {install_dir} already exists. Checking if it's a git repository...")
            if os.path.exists(os.path.join(install_dir, ".git")):
                print("Repository already cloned. Pulling latest changes...")
                subprocess.run(["git", "-C", install_dir, "pull"], check=True)
                return True
            else:
                print(f"Directory {install_dir} exists but is not a git repository.")
                return False
        subprocess.run(["git", "clone", repo_url, install_dir], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
        return False

def install():
    """Main installation function."""
    print("Starting CodeAce installation...")
    
    if not check_python() or not check_git():
        sys.exit(1)
    
    # Clone repository
    REPO_URL = "https://github.com/Yoni-Raich/streamlit_gui"  # Replace with actual repo URL
    INSTALL_DIR = "codeace_app"
    
    if not clone_repository(REPO_URL, INSTALL_DIR):
        print("Failed to clone repository. Installation aborted.")
        sys.exit(1)
    
    # Change to installation directory
    os.chdir(INSTALL_DIR)
    
    # Get environment variables after changing to installation directory
    get_env_vars()
    
    # Create virtual environment
    print("Creating virtual environment...")
    venv.create("venv", with_pip=True)
    
    # Get the path to the virtual environment's Python executable
    if sys.platform == "win32":
        venv_python = os.path.join("venv", "Scripts", "python.exe")
        venv_pip = os.path.join("venv", "Scripts", "pip.exe")
    else:
        venv_python = os.path.join("venv", "bin", "python")
        venv_pip = os.path.join("venv", "bin", "pip")
    
    # Upgrade pip
    print("Upgrading pip...")
    subprocess.run([venv_python, "-m", "pip", "install", "--upgrade", "pip"], check=True)
    
    # Install requirements
    print("Installing requirements...")
    if os.path.exists("requirements.txt"):
        subprocess.run([venv_pip, "install", "-r", "requirements.txt"], check=True)
    else:
        print("Warning: requirements.txt not found")
    
    # Install CodeAce package if available (now looking in the cloned repository)
    print("Checking for CodeAce package...")
    codeace_pkg_path = os.path.join(os.getcwd(), "codeace_pkg")
    if os.path.exists(codeace_pkg_path):
        print(f"Found codeace_pkg directory at: {codeace_pkg_path}")
        gz_files = list(Path(codeace_pkg_path).glob("*.gz"))
        if gz_files:
            try:
                pkg_path = str(gz_files[0])
                print(f"Installing package: {pkg_path}")
                subprocess.run([venv_pip, "install", pkg_path], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error installing package: {e}")
            except Exception as e:
                print(f"Unexpected error installing package: {e}")
        else:
            print("No .gz package files found in codeace_pkg directory")
    else:
        print(f"Note: codeace_pkg directory not found at {codeace_pkg_path}, skipping package installation")
    
    print("\nInstallation completed!")
    
    # Ask to run the application
    run_now = input("\nWould you like to run the application now? (Y/N): ")
    if run_now.upper() == 'Y':
        print("\nStarting CodeAce application...")
        if os.path.exists("run.py"):
            subprocess.run([venv_python, "run.py"], check=True)
        else:
            print("Running streamlit directly...")
            subprocess.run([venv_python, "-m", "streamlit", "run", "streamlit_gui.py"], check=True)

if __name__ == "__main__":
    install() 