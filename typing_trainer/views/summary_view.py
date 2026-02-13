"""Summary view showing results after exercise completion."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button
from textual.binding import Binding
from textual.containers import Container, Vertical


class SummaryView(Screen):
    """Summary screen showing exercise results."""
    
    BINDINGS = [
        Binding("escape", "back_to_menu", "Menu"),
        Binding("enter", "back_to_menu", "Menu"),
    ]
    
    CSS = """
    SummaryView {
        align: center middle;
    }
    
    #summary_container {
        width: 60;
        height: auto;
        background: $panel;
        border: double $success;
        padding: 2;
    }
    
    #title {
        width: 100%;
        content-align: center middle;
        text-style: bold;
        color: $success;
        margin: 1 0;
    }
    
    .stat {
        width: 100%;
        content-align: center middle;
        margin: 1 0;
        text-style: bold;
    }
    
    #message {
        width: 100%;
        content-align: center middle;
        color: $text-muted;
        margin: 2 0;
    }
    
    Button {
        width: 100%;
        margin: 1 0;
    }
    """
    
    def __init__(self, results: dict):
        """Initialize the summary view.
        
        Args:
            results: Dictionary containing exercise results
                - exercise: The completed exercise
                - wpm: Words per minute
                - accuracy: Accuracy percentage
                - elapsed_time: Time taken in seconds
                - mistakes: Number of typing mistakes
        """
        super().__init__()
        self.results = results
    
    def compose(self) -> ComposeResult:
        """Compose the summary view."""
        yield Header()
        
        with Vertical(id="summary_container"):
            yield Static("✅ Exercise Complete!", id="title")
            yield Static(f"📝 {self.results['exercise'].title}", classes="stat")
            yield Static("", classes="stat")  # Spacer
            yield Static(
                f"⚡ Speed: {self.results['wpm']:.1f} WPM",
                classes="stat"
            )
            yield Static(
                f"🎯 Accuracy: {self.results['accuracy']:.1f}%",
                classes="stat"
            )
            yield Static(
                f"⏱️  Time: {self.results['elapsed_time']:.1f}s",
                classes="stat"
            )
            yield Static(
                f"❌ Mistakes: {self.results.get('mistakes', 0)}",
                classes="stat"
            )
            yield Static("", classes="stat")  # Spacer
            yield Static(self._get_performance_message(), id="message")
            yield Button("Back to Menu", variant="success", id="menu_button")
        
        yield Footer()
    
    def _get_performance_message(self) -> str:
        """Get a performance message based on results."""
        wpm = self.results['wpm']
        accuracy = self.results['accuracy']
        
        if accuracy < 80:
            return "Focus on accuracy! Speed will come with practice."
        elif wpm < 20:
            return "Good start! Keep practicing to build speed."
        elif wpm < 40:
            return "Nice progress! You're building good habits."
        elif wpm < 60:
            return "Great job! You're typing with confidence."
        else:
            return "Excellent! You're a typing master! 🏆"
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        self.action_back_to_menu()
    
    def action_back_to_menu(self) -> None:
        """Return to the menu."""
        # Pop both summary and typing screens to return to menu
        self.app.pop_screen()  # Pop summary
        self.app.pop_screen()  # Pop typing
