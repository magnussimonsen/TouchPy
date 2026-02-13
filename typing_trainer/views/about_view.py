"""About view showing license and credits."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button
from textual.binding import Binding
from textual.containers import Vertical, ScrollableContainer


class AboutView(Screen):
    """About screen showing app information, license, and credits."""
    
    BINDINGS = [
        Binding("escape", "close", "Back"),
        Binding("enter", "close", "Back"),
    ]
    
    CSS = """
    AboutView {
        align: center middle;
    }
    
    #about_container {
        width: 80;
        height: auto;
        max-height: 40;
        background: $panel;
        border: double $accent;
        padding: 1;
    }
    
    .about_section {
        width: 100%;
        margin: 0;
    }
    
    #title {
        width: 100%;
        content-align: center middle;
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
    }
    
    .section_header {
        width: 100%;
        text-style: bold;
        color: $primary;
        margin-top: 0;
        margin-bottom: 0;
    }
    
    .section_text {
        width: 100%;
        color: $text;
        margin-bottom: 0;
    }
    
    Button {
        width: 100%;
        margin-top: 1;
    }
    """
    
    def compose(self) -> ComposeResult:
        """Compose the about view."""
        yield Header()
        
        with ScrollableContainer(id="about_container"):
            yield Static("🎯 TouchPy - Touch Typing Trainer", id="title")
            
            # Authors section
            yield Static("👥 Authors", classes="section_header")
            yield Static(
                "Magnus Simonsen & Claude Sonnet\n"
                "GitHub: https://github.com/magnussimonsen/TouchPy",
                classes="section_text about_section"
            )
            
            # Description section
            yield Static("📖 About", classes="section_header")
            yield Static(
                "A terminal-based touch typing trainer built with Python, Textual, and Rich. "
                "Practice typing with real-time feedback on speed, accuracy, and mistakes.",
                classes="section_text about_section"
            )
            
            # License section
            yield Static("⚖️ License", classes="section_header")
            yield Static(
                "MIT License - Copyright (c) 2026 Magnus Simonsen\n"
                "Permission is granted to use, copy, modify, merge, publish, distribute, "
                "sublicense, and/or sell copies of the Software without restriction. "
                "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND.",
                classes="section_text about_section"
            )
            
            # Technology section
            yield Static("🛠️ Built With", classes="section_header")
            yield Static(
                "Python 3.8+ • Textual • Rich",
                classes="section_text about_section"
            )
            
            yield Button("Back to Menu", variant="primary", id="back_button")
        
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        self.action_close()
    
    def action_close(self) -> None:
        """Close the about screen."""
        self.app.pop_screen()
