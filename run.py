#!/usr/bin/env python3
"""Run the touch typing trainer."""

import sys
import os
from pathlib import Path

# Add typing_trainer to the path
sys.path.insert(0, str(Path(__file__).parent))

# Ensure stdout/stderr are properly configured for Windows console
if sys.platform == "win32":
    import io
    # Force UTF-8 encoding for console
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from typing_trainer.app import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # User pressed Ctrl+C - exit gracefully
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        print("\n")
        input("Press Enter to close...")
        sys.exit(1)
