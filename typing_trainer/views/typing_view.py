"""Typing practice view."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, TextArea
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
    
    TextArea {
        width: 100%;
        height: 12;
        border: solid $primary;
        background: $surface;
    }
    """
    
    # Reactive attributes
    elapsed_time = reactive(0.0)
    wpm = reactive(0.0)
    mistakes = reactive(0)
    
    def __init__(self, exercise: Exercise):
        """Initialize the typing view.
        
        Args:
            exercise: The exercise to practice
        """
        super().__init__()
        self.exercise = exercise
        self.start_time: float = None
        self.typed_text = ""
        self.previous_typed_text = ""
        self.timer_started = False
        self.exercise_completed = False
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
        
        # Text area for typing (supports multi-line)
        text_area = TextArea(id="typing_input")
        text_area.show_line_numbers = False
        yield text_area
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Focus the text area when the screen is mounted."""
        self.query_one("#typing_input", TextArea).focus()
    
    def _format_stats(self) -> str:
        """Format the stats display."""
        return f"⏱️  Time: {self.elapsed_time:.1f}s  |  ⚡ WPM: {self.wpm:.1f}  |  ❌ Mistakes: {self.mistakes}  |  ESC: Quit"
    
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
            self.update_timer_callback = self.set_interval(0.1, self._update_metrics_timer)
    
    def _update_metrics_timer(self) -> None:
        """Update the elapsed time and WPM."""
        if self.start_time:
            self.elapsed_time = time.time() - self.start_time
            self.wpm = self.metrics_calculator.calculate_wpm(
                len(self.typed_text), 
                self.elapsed_time
            )
            self._update_display()
    
    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        """Handle text area changes."""
        # Don't process if exercise is already completed
        if self.exercise_completed:
            return
        
        # Get the text area content
        text_area = event.text_area
        new_text = text_area.text
        
        # Start timer on first character
        if new_text and not self.timer_started:
            self._start_timer()
        
        # Track mistakes: count when a character is added that doesn't match
        if len(new_text) > len(self.previous_typed_text):
            # User typed a new character
            char_position = len(self.previous_typed_text)
            if char_position < len(self.exercise.text):
                expected_char = self.exercise.text[char_position]
                typed_char = new_text[char_position]
                if expected_char != typed_char:
                    self.mistakes += 1
        
        self.previous_typed_text = new_text
        self.typed_text = new_text
        
        # Check if exercise is complete
        # Complete when user has typed the same number of characters as the exercise
        # (regardless of whether they're correct or not)
        exercise_length = len(self.exercise.text.rstrip())
        typed_length = len(self.typed_text.rstrip())
        
        if typed_length >= exercise_length and exercise_length > 0:
            self._complete_exercise()
        
        self._update_display()
    
    def _complete_exercise(self) -> None:
        """Handle exercise completion."""
        # Mark as completed to prevent multiple completions
        self.exercise_completed = True
        
        # Stop the timer immediately
        if self.update_timer_callback:
            self.update_timer_callback.stop()
            self.update_timer_callback = None
        
        # Calculate final metrics using the stripped text
        final_text = self.typed_text.rstrip()
        exercise_text = self.exercise.text.rstrip()
        
        accuracy = self.metrics_calculator.calculate_accuracy(
            exercise_text,
            final_text
        )
        
        # Switch to summary view
        results = {
            "exercise": self.exercise,
            "wpm": self.wpm,
            "accuracy": accuracy,
            "elapsed_time": self.elapsed_time,
            "mistakes": self.mistakes
        }
        summary_screen = SummaryView(results)
        self.app.push_screen(summary_screen)
    
    def action_back_to_menu(self) -> None:
        """Return to the menu."""
        if self.update_timer_callback:
            self.update_timer_callback.stop()
        self.app.pop_screen()
