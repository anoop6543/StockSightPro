# VSCode Setup Guide for Financial Learning Platform

## Required Extensions

Install these extensions for optimal development experience:

1. **Python** (ms-python.python)
   - Essential for Python development
   - Includes IntelliSense, linting, debugging

2. **Streamlit** (streamlit.streamlit-vscode)
   - Streamlit-specific features
   - Live preview support

3. **Pylance** (ms-python.vscode-pylance)
   - Enhanced type checking
   - Better code navigation

4. **PostgreSQL** (ckolkman.vscode-postgres)
   - Database integration
   - SQL syntax highlighting

5. **GitLens** (eamodio.gitlens)
   - Enhanced Git integration
   - Code authorship at a glance

## Workspace Settings

Create `.vscode/settings.json` with these recommended settings:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "python.analysis.typeCheckingMode": "basic",
    "editor.formatOnSave": true,
    "editor.rulers": [88],
    "files.trimTrailingWhitespace": true,
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    },
    "files.exclude": {
        "**/__pycache__": true,
        "**/.pytest_cache": true
    }
}
```

## Launch Configuration

Create `.vscode/launch.json` for debugging:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Streamlit: Run App",
            "type": "python",
            "request": "launch",
            "module": "streamlit",
            "args": [
                "run",
                "main.py",
                "--server.port",
                "5000",
                "--server.address",
                "0.0.0.0"
            ],
            "justMyCode": true
        }
    ]
}
```

## Environment Setup

1. Open the integrated terminal (Ctrl+`)
2. Create virtual environment:
   ```bash
   python -m venv .venv
   ```
3. Activate the environment:
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure Navigation

The workspace is organized as follows:
```
financial-learning-platform/
├── .streamlit/          # Streamlit configuration
├── components/          # Reusable UI components
├── pages/              # Application pages
├── static/             # Static assets
└── main.py             # Application entry point
```

Use the VSCode file explorer (Ctrl+Shift+E) to navigate the project structure.

## Useful Keyboard Shortcuts

### General
- **Ctrl+P**: Quick file navigation
- **Ctrl+Shift+P**: Command palette
- **Ctrl+Space**: Trigger suggestions
- **F5**: Start debugging
- **Ctrl+`**: Toggle terminal

### Python-specific
- **F12**: Go to definition
- **Alt+Shift+F**: Format document
- **Ctrl+K Ctrl+I**: Show hover information

## Theme Configuration

For optimal viewing of this project's dark/light mode features:

1. Install "GitHub Theme" extension
2. Set color theme:
   - Light: GitHub Light Default
   - Dark: GitHub Dark Default

This matches our application's theme and provides good contrast for both modes.

## Code Navigation Tips

1. **Symbol Navigation**:
   - Ctrl+T to search symbols
   - Use breadcrumbs at top of editor

2. **Smart Selection**:
   - Alt+Click for multiple cursors
   - Ctrl+D to select next occurrence

3. **Code Folding**:
   - Ctrl+Shift+[ to fold
   - Ctrl+Shift+] to unfold

## Debugging Tips

1. **Breakpoints**:
   - Click left margin to set
   - F9 to toggle breakpoint
   - Ctrl+Shift+F9 to clear all

2. **Debug Console**:
   - View variables
   - Evaluate expressions

3. **Watch Window**:
   - Add variables to monitor
   - Track value changes

## Git Integration

1. **Source Control** (Ctrl+Shift+G):
   - Stage changes
   - Commit
   - Push/Pull

2. **GitLens Features**:
   - Blame annotations
   - File history
   - Line history

## Recommended Extensions for Development Experience

### Code Quality
- **Black Formatter** (ms-python.black-formatter)
- **isort** (ms-python.isort)
- **Pylint** (ms-python.pylint)

### Productivity
- **IntelliCode** (visualstudioexptteam.vscodeintellicode)
- **Path Intellisense** (christian-kohler.path-intellisense)
- **Todo Tree** (gruntfuggly.todo-tree)

### Database
- **SQLTools** (mtxr.sqltools)
- **Database Client** (cweijan.vscode-database-client2)

## Troubleshooting

Common issues and solutions:

1. **Python Interpreter Not Found**:
   - Ctrl+Shift+P → Python: Select Interpreter
   - Choose .venv/bin/python

2. **Linting Not Working**:
   - Ensure pylint is installed
   - Check workspace settings
   - Reload VSCode

3. **Debugger Issues**:
   - Verify launch.json configuration
   - Check if debugpy is installed
   - Try restarting VSCode

## Updates and Maintenance

1. **Extension Updates**:
   - Check regularly for updates
   - Update all extensions monthly

2. **Settings Sync**:
   - Enable Settings Sync
   - Back up configurations

## Additional Resources

- [Official VSCode Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial)
- [Streamlit Documentation](https://docs.streamlit.io)
- [VSCode Keyboard Shortcuts](https://code.visualstudio.com/docs/getstarted/keybindings)
