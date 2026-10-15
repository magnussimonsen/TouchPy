#!/usr/bin/env python3
"""Create the project virtual environment and install its requirements."""

import os
from pathlib import Path
import subprocess
import sys


def main() -> None:
    project_dir = Path(__file__).resolve().parent
    venv_dir = project_dir / ".venv"
    requirements_file = project_dir / "requirements.txt"

    if not requirements_file.is_file():
        raise FileNotFoundError(f"Requirements file not found: {requirements_file}")

    print(f"Creating virtual environment at {venv_dir}")
    subprocess.run(
        [sys.executable, "-m", "venv", str(venv_dir)],
        check=True,
    )

    if os.name == "nt":
        venv_python = venv_dir / "Scripts" / "python.exe"
    else:
        venv_python = venv_dir / "bin" / "python"

    print("Installing project requirements")
    subprocess.run(
        [str(venv_python), "-m", "pip", "install", "-r", str(requirements_file)],
        check=True,
    )

    print("\nEnvironment ready. Run the app with:")
    if os.name == "nt":
        print(r".\.venv\Scripts\python.exe run.py")
    else:
        print("./.venv/bin/python run.py")


if __name__ == "__main__":
    main()
