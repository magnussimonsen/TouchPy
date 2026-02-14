#!/usr/bin/env python3
"""Run the touch typing trainer."""

import sys
from pathlib import Path

# Add typing_trainer to the path
sys.path.insert(0, str(Path(__file__).parent))

from typing_trainer.app import main

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to close...")
        sys.exit(1)
