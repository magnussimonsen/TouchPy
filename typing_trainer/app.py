"""Main application for the touch typing trainer."""

import sys
from pathlib import Path
from textual.app import App
from .views.menu_view import MenuView
from .views.typing_view import TypingView
from .views.summary_view import SummaryView
from .services.loader import ExerciseLoader


class TypingTrainerApp(App):
    """A terminal-based touch typing trainer application."""
    
    CSS = """
    Screen {
        background: $background;
    }
    """
    
    def __init__(self):
        """Initialize the typing trainer app."""
        super().__init__()
        self.title = "Touch Typing Trainer"
        
        # Set up exercises directories
        if getattr(sys, 'frozen', False):
            # Running as compiled .exe
            if hasattr(sys, '_MEIPASS'):
                # One-file mode
                base_path = Path(sys._MEIPASS)
            else:
                # One-dir mode (TouchPy.spec uses this)
                # In one-dir mode, sys.executable points to the exe
                # The bundled files are relative to the exe directory
                # But wait, PyInstaller structure for imports...
                # Usually: dist/TouchPy/typing_trainer/exercises
                base_path = Path(sys.executable).parent

            internal_dir = base_path / "typing_trainer" / "exercises"
            
            # External exercises next to the .exe
            app_dir = Path(sys.executable).parent
            external_dir = app_dir / "exercises"
        else:
            # Running in development mode
            internal_dir = Path(__file__).parent / "exercises"
            app_dir = Path(__file__).parent.parent
            external_dir = app_dir / "exercises"
        
        # Load exercises from both locations
        self.loader = ExerciseLoader([internal_dir, external_dir])
        self.exercises = []
    
    def on_mount(self) -> None:
        """Load exercises and show the menu when the app starts."""
        # Load exercises
        self.exercises = self.loader.load_exercises()
        
        if not self.exercises:
            self.exit(message="No exercises found! Please add .txt files to the exercises/ directory.")
            return
        
        # Create and push the menu screen
        menu_screen = MenuView(self.exercises)
        self.push_screen(menu_screen)


def main():
    """Entry point for the typing trainer application."""
    try:
        # Add a startup message to verify the app is at least trying to start
        print("Starting Touch Typing Trainer...")
        app = TypingTrainerApp()
        app.run()
    except Exception as e:
        print(f"\nFailed to start application: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        raise


if __name__ == "__main__":
    main()
