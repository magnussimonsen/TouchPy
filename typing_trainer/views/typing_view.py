"""Typing practice view."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Input
from textual.binding import Binding
from textual.reactive import reactive
from rich.text import Text
import time
from ..models import Exercise
from ..services.metrics import MetricsCalculator
from .summary_view import SummaryView


class TypingView(Screen):
    """Typing practice screen."""
    
    BINDINGS = [
        Binding("escape", "back_to_menu", "Menu"),
    ]
    
    CSS = """
    TypingView {
        align: center middle;
    }
    
    #stats {
        width: 100%;
        height: 3;
        content-align: center middle;
        background: $panel;
        border: solid $primary;
        margin: 1 0;
    }
    
    #target_text_container {
        width: 90%;
        height: auto;
        padding: 2;
        background: $surface;
        border: solid $accent;
        margin: 1 0;
    }
    
    #target_text {
        width: 100%;
    }
    
    #input_container {
        width: 90%;
        margin: 1 0;
    }
    
    Input {
        width: 100%;
    }
    """
    
    # Reactive attributes
    elapsed_time = reactive(0.0)
    wpm = reactive(0.0)
    
    def __init__(self, exercise: Exercise):
        """Initialize the typing view.
        
        Args:
            exercise: The exercise to practice
        """
        super().__init__()
        self.exercise = exercise
        self.start_time: float = None
        self.typed_text = ""
        self.timer_started = False
        self.metrics_calculator = MetricsCalculator()
        self.update_timer_callback = None
    
    def compose(self) -> ComposeResult:
        """Compose the typing view."""
        yield Header()
        
        # Stats display
        stats_text = self._format_stats()
        yield Static(stats_text, id="stats")
        
        # Target text with highlighting
        target_text = self._render_target_text()
        yield Static(target_text, id="target_text_container")
        
        # Input field
        input_widget = Input(placeholder="Start typing here...")
        input_widget.id = "typing_input"
        yield input_widget
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Focus the input when the screen is mounted."""
        self.query_one("#typing_input", Input).focus()
    
    def _format_stats(self) -> str:
        """Format the stats display."""
        return f"⏱️  Time: {self.elapsed_time:.1f}s  |  ⚡ WPM: {self.wpm:.1f}"
    
    def _render_target_text(self) -> Text:
        """Render the target text with highlighting."""
        text = Text()
        
        for i, char in enumerate(self.exercise.text):
            status = self.metrics_calculator.get_character_status(
                self.exercise.text, 
                self.typed_text, 
                i
            )
            
            if status == 'correct':
                text.append(char, style="bold green")
            elif status == 'incorrect':
                text.append(char, style="bold red underline")
            else:  # pending
                text.append(char, style="dim")
        
        return text
    
    def _update_display(self) -> None:
        """Update the display elements."""
        # Update stats
        stats_widget = self.query_one("#stats", Static)
        stats_widget.update(self._format_stats())
        
        # Update target text with highlighting
        target_widget = self.query_one("#target_text_container", Static)
        target_widget.update(self._render_target_text())
    
    def _start_timer(self) -> None:
        """Start the timer when first character is typed."""
        if not self.timer_started:
            self.timer_started = True
            self.start_time = time.time()
            self.update_timer_callback = self.set_interval(0.1, self._update_timer)
    
    def _update_timer(self) -> None:
        """Update the elapsed time and WPM."""
        if self.start_time:
            self.elapsed_time = time.time() - self.start_time
            self.wpm = self.metrics_calculator.calculate_wpm(
                len(self.typed_text), 
                self.elapsed_time
            )
            self._update_display()
    
    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes."""
        # Start timer on first character
        if event.value and not self.timer_started:
            self._start_timer()
        
        self.typed_text = event.value
        
        # Check if exercise is complete
        if self.typed_text == self.exercise.text:
            self._complete_exercise()
        
        self._update_display()
    
    def _complete_exercise(self) -> None:
        """Handle exercise completion."""
        # Stop the timer
        if self.update_timer_callback:
            self.update_timer_callback.stop()
        
        # Calculate final metrics
        accuracy = self.metrics_calculator.calculate_accuracy(
            self.exercise.text,
            self.typed_text
        )
        
        # Switch to summary view
        results = {
            "exercise": self.exercise,
            "wpm": self.wpm,
            "accuracy": accuracy,
            "elapsed_time": self.elapsed_time
        }
        summary_screen = SummaryView(results)
        self.app.push_screen(summary_screen)
    
    def action_back_to_menu(self) -> None:
        """Return to the menu."""
        if self.update_timer_callback:
            self.update_timer_callback.stop()
        self.app.pop_screen()
