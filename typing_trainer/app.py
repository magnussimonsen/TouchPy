"""Main application for the touch typing trainer."""

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
        
        # Set up exercises directory
        self.exercises_dir = Path(__file__).parent / "exercises"
        self.loader = ExerciseLoader(self.exercises_dir)
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
    app = TypingTrainerApp()
    app.run()


if __name__ == "__main__":
    main()
