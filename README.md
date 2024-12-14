# CodeAce GUI

A streamlit-based graphical interface for the CodeAce package, designed to help developers efficiently map and query large codebases using AI.

## Overview

CodeAce GUI provides an intuitive interface for the CodeAce package, enabling users to:
- Map and analyze large codebases
- Ask questions about code functionality and implementation
- Handle multiple source directories
- Integrate dependency analysis
- Include custom documentation context

### Key Features

1. **Multiple Source Management**
   - Add multiple source directories or GitHub repositories
   - Save and manage source paths for future sessions
   - Switch between different codebases seamlessly

2. **Dependency Analysis**
   - Add secondary source paths for dependency analysis
   - Pre-analyze dependencies before querying main codebase
   - Integrate insights from both sources

3. **Documentation Integration**
   - Add documentation files to the `Documentations` folder
   - Selectively include documentation context for specific queries
   - Support for markdown documentation format

4. **Flexible Context Management**
   - Toggle summary context inclusion
   - Select specific documentation files for context
   - Add custom context text on-the-fly

5. **Conversation Management**
   - Save and load conversation history
   - Start new conversations
   - Track relevant files for each query

## Installation

### Prerequisites
- Python 3.8 or higher
- Git

### Installation Steps

1. **Using Installation Script**

   ```bash
   python install.py
   ```

   The script will:
   - Check and request required environment variables
   - Clone the repository
   - Create a virtual environment
   - Install required dependencies
   - Set up the CodeAce package

2. **Running the Application**

   After installation, run the application using:

   ```bash
   python run.py
   ```

   Or if prompted during installation, you can choose to run it immediately.

## Usage

1. **Adding Source Code**
   - Use the "Source Management" expander in the sidebar
   - Enter a local path or GitHub URL
   - Click "Add Source" to include it in your sources

2. **Running Code Mapping**
   - Select a source from your saved sources
   - Click "Run Mapping" to analyze the codebase
   - Wait for the mapping process to complete

3. **Adding Documentation**
   - Place your documentation files in the `Documentations` folder
   - Files should be in markdown format
   - Select relevant documentation from the sidebar when asking questions

4. **Asking Questions**
   - Type your question in the chat interface
   - Select any additional context from the sidebar
   - View relevant files and AI responses

## Contributing

Contributions are welcome! Please feel free to submit pull requests or create issues for bugs and feature requests.
