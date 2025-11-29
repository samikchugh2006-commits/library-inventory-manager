# run.py — ALWAYS run THIS file, not cli/main.py

import sys
from pathlib import Path

# ensure project root is on sys.path
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# import and run the CLI entrypoint
from cli.main import main_menu

if __name__ == "__main__":
    main_menu()
