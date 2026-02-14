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
from ..keyboard_layouts import get_layout


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

    #keyboard_layout {
        width: 100%;
        height: auto;
        content-align: center middle;
        margin: 1 0;
    }
    
    #target_text_container {
        width: 90%;
        height: auto;
        padding: 1;
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
        width: 90%;
        height: 3;
        border: solid $primary;
        background: $surface;
    }
    """
    
    # Reactive attributes
    elapsed_time = reactive(0.0)
    wpm = reactive(0.0)
    mistakes = reactive(0)
    lines_left = reactive(0)
    
    def __init__(self, exercise: Exercise):
        """Initialize the typing view.
        
        Args:
            exercise: The exercise to practice
        """
        super().__init__()
        self.exercise = exercise
        self.start_time: float = None
        
        # Split text into lines for display and tracking
        raw_lines = self.exercise.text.splitlines()
        # Filter out empty lines if any, though usually we want to preserve paragraph structure
        # But for typing tests, empty lines might be confusing if we force typing them.
        # Let's keep them but user just hits Enter.
        self.lines = [line for line in raw_lines if line.strip()] 
        if not self.lines:
            self.lines = ["Error: No text found"]

        self.current_line_idx = 0
        self.lines_left = len(self.lines)
        
        # Track text typed for completed lines
        self.completed_text = ""
        
        # Track character mistakes
        self.char_mistakes = {}
        
        # Current line typing state
        self.current_typed_text = ""
        self.previous_current_typed_text = ""
        
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
        
        # Keyboard Layout
        layout_text = get_layout(self.exercise.layout)
        yield Static(layout_text, id="keyboard_layout")

        # Target text with highlighting (Current Line Only)
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
        self._update_display()
    
    def _format_stats(self) -> str:
        """Format the stats display."""
        return f"⏱️  Time: {self.elapsed_time:.1f}s  |  ⚡ WPM: {self.wpm:.1f}  |  ❌ Mistakes: {self.mistakes}  |  📝 Lines Left: {self.lines_left}  |  ESC: Quit"
    
    def _render_target_text(self) -> Text:
        """Render the target text with highlighting."""
        # Only render the current line
        if self.current_line_idx >= len(self.lines):
            return Text("Exercise Completed!", style="bold green")

        current_target_line = self.lines[self.current_line_idx]
        text = Text()
        
        for i, char in enumerate(current_target_line):
            status = 'pending'
            
            # Check against currently typed text for this line
            if i < len(self.current_typed_text):
                typed_char = self.current_typed_text[i]
                if typed_char == char:
                    status = 'correct'
                else:
                    status = 'incorrect'
            
            if status == 'correct':
                text.append(char, style="bold green")
            elif status == 'incorrect':
                text.append(char, style="bold red underline")
            else:  # pending
                if i == len(self.current_typed_text):
                    # This is the next character to type - highlight it!
                    text.append(char, style="bold white on blue")
                else:
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
        
        # Update keyboard layout highlighting
        self._update_keyboard_layout()
        
    def _update_keyboard_layout(self) -> None:
        """Update the keyboard layout with the next character highlighted."""
        next_char = None
        
        # Determine the next character expected
        if self.current_line_idx < len(self.lines):
            current_line = self.lines[self.current_line_idx]
            typed_len = len(self.current_typed_text)
            
            if typed_len < len(current_line):
                next_char = current_line[typed_len]
        
<<<<<<< HEAD
        # Get top 3 mistakes (allowing space but excluding other whitespace like newline)
        sorted_mistakes = sorted(self.char_mistakes.items(), key=lambda x: x[1], reverse=True)
        error_keys = []
        for char, _ in sorted_mistakes:
            if char and (char == ' ' or char.strip()):
=======
        # Get top 3 mistakes (excluding whitespace)
        sorted_mistakes = sorted(self.char_mistakes.items(), key=lambda x: x[1], reverse=True)
        error_keys = []
        for char, _ in sorted_mistakes:
            if char and char.strip():
>>>>>>> 029f98bb93dbf9ff3540bc42783bb13ec868b76d
                error_keys.append(char)
                if len(error_keys) >= 3:
                    break

        # Update the layout widget
        layout_widget = self.query_one("#keyboard_layout", Static)
        layout_text = get_layout(self.exercise.layout, highlight_key=next_char, error_keys=error_keys)
        layout_widget.update(layout_text)
    
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
            
            # Total chars = completed lines chars + current line chars
            total_chars = len(self.completed_text) + len(self.current_typed_text)
            
            self.wpm = self.metrics_calculator.calculate_wpm(
                total_chars, 
                self.elapsed_time
            )
            self._update_display()
    
    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        """Handle text area changes."""
        # Don't process if exercise is already completed
        if self.exercise_completed or self.current_line_idx >= len(self.lines):
            return
        
        # Get the text area content
        text_area = event.text_area
        new_text = text_area.text
        
        # For simplicity in this line-based mode, prevent newlines in input if they aren't finishing the line?
        # Actually, let's treat newlines as "submit line" or just ignore them until line is full?
        # The prompt says: "when the colored letters are at the end of that line, a new line is inserted"
        # This implies auto-advance when length is reached.
        
        # Start timer on first character
        if new_text and not self.timer_started:
            self._start_timer()
        
        current_target_line = self.lines[self.current_line_idx]

        # Handle mistakes counting
        if len(new_text) > len(self.previous_current_typed_text):
             # User typed a new character
            char_position = len(self.previous_current_typed_text)
            
            # Only check if within bounds of target line
            if char_position < len(current_target_line):
                expected_char = current_target_line[char_position]
                typed_char = new_text[char_position]
                if expected_char != typed_char:
                    self.mistakes += 1
                    # Track specific character mistake
                    self.char_mistakes[expected_char] = self.char_mistakes.get(expected_char, 0) + 1
        
        self.previous_current_typed_text = new_text
        self.current_typed_text = new_text
        
        # Check if current line is complete
        # We check if length >= target length.
        if len(self.current_typed_text) >= len(current_target_line):
            # Check accuracy of the line? 
            # Usually typing trainers block you if you are wrong, or let you pass with errors.
            # We will assume passing with errors is allowed, similar to original logic.
            
            # Move to next line
            self._advance_line()
        else:
            self._update_display()

    def _advance_line(self):
        """Advance to the next line."""
        # Add current input to completed text
        self.completed_text += self.current_typed_text
        
        # Move index
        self.current_line_idx += 1
        self.lines_left = len(self.lines) - self.current_line_idx
        
        # Clear input for next line
        text_area = self.query_one("#typing_input", TextArea)
        text_area.text = "" # This might trigger on_text_area_changed again with empty text
        
        # Reset current tracking
        self.current_typed_text = ""
        self.previous_current_typed_text = ""
        
        if self.current_line_idx >= len(self.lines):
            self._complete_exercise()
        else:
             self._update_display()
    
    def _complete_exercise(self) -> None:
        """Handle exercise completion."""
        # Mark as completed to prevent multiple completions
        self.exercise_completed = True
        self.lines_left = 0
        
        # Stop the timer immediately
        if self.update_timer_callback:
            self.update_timer_callback.stop()
            self.update_timer_callback = None
        
        # Reconstruct full exercise text for accuracy calc
        # Note: self.completed_text contains what user typed. 
        # But we skipped spaces/newlines between lines?
        # Let's reconstruct target text from lines.
        exercise_text = "".join(self.lines)
        final_text = self.completed_text # This corresponds to joined lines
        
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
