"""Menu view for exercise selection."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, ListItem, ListView
from textual.binding import Binding
from typing import List
from ..models import Exercise
from .typing_view import TypingView


class MenuView(Screen):
    """Main menu screen for selecting exercises."""
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("enter", "select_exercise", "Select", show=True),
    ]
    
    CSS = """
    MenuView {
        align: center middle;
    }
    
    #title {
        width: 100%;
        content-align: center middle;
        text-style: bold;
        color: $accent;
        margin: 1 0;
    }
    
    #instructions {
        width: 100%;
        content-align: center middle;
        color: $text-muted;
        margin: 1 0;
    }
    
    ListView {
        width: 80;
        height: auto;
        max-height: 20;
        border: solid $primary;
        margin: 1 0;
    }
    
    ListItem {
        padding: 1 2;
    }
    """
    
    def __init__(self, exercises: List[Exercise]):
        """Initialize the menu view.
        
        Args:
            exercises: List of available exercises
        """
        super().__init__()
        self.exercises = exercises
    
    def compose(self) -> ComposeResult:
        """Compose the menu view."""
        yield Header()
        yield Static("🎯 Touch Typing Trainer", id="title")
        yield Static("Select an exercise to begin", id="instructions")
        yield ListView(id="exercise_list")
        yield Footer()
    
    def on_mount(self) -> None:
        """Populate the list view and focus it when the screen is mounted."""
        list_view = self.query_one(ListView)
        
        # Add exercise items
        for exercise in self.exercises:
            item = ListItem(Static(f"📝 {exercise.title}"))
            item.exercise = exercise  # Store exercise reference
            list_view.append(item)
        
        # Focus the list view
        list_view.focus()
    
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle ListView selection (Enter key or click)."""
        selected_item = event.item
        if hasattr(selected_item, 'exercise'):
            exercise = selected_item.exercise
            # Switch to typing view with the selected exercise
            typing_screen = TypingView(exercise)
            self.app.push_screen(typing_screen)
    
    def action_select_exercise(self) -> None:
        """Handle exercise selection via key binding."""
        list_view = self.query_one(ListView)
        
        if list_view.highlighted_child:
            selected_item = list_view.highlighted_child
            if hasattr(selected_item, 'exercise'):
                exercise = selected_item.exercise
                # Switch to typing view with the selected exercise
                typing_screen = TypingView(exercise)
                self.app.push_screen(typing_screen)
    
    def action_quit(self) -> None:
        """Quit the application."""
        self.app.exit()
