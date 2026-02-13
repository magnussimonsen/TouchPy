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
        padding: 2;
    }
    
    .about_section {
        width: 100%;
        margin: 1 0;
    }
    
    #title {
        width: 100%;
        content-align: center middle;
        text-style: bold;
        color: $accent;
        margin-bottom: 2;
    }
    
    .section_header {
        width: 100%;
        text-style: bold;
        color: $primary;
        margin-top: 1;
        margin-bottom: 1;
    }
    
    .section_text {
        width: 100%;
        color: $text;
        margin-bottom: 1;
    }
    
    Button {
        width: 100%;
        margin-top: 2;
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
                "Magnus Simonsen & Claude Sonne \n"
                "GitHub: https://github.com/magnussimonsen/TouchPy\n"
                classes="section_text about_section"
            )
            
            # Description section
            yield Static("📖 About", classes="section_header")
            yield Static(
                "TouchPy is a beautiful terminal-based touch typing trainer "
                "built with Python, Textual, and Rich. Practice your typing "
                "skills with multiple exercises and get real-time feedback "
                "on your speed, accuracy, and mistakes.",
                classes="section_text about_section"
            )
            
            # License section
            yield Static("⚖️ License", classes="section_header")
            yield Static(
                "MIT License\n\n"
                "Copyright (c) 2026 Magnus Simonsen\n\n"
                "Permission is hereby granted, free of charge, to any person obtaining a copy "
                "of this software and associated documentation files (the \"Software\"), to deal "
                "in the Software without restriction, including without limitation the rights "
                "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell "
                "copies of the Software, and to permit persons to whom the Software is "
                "furnished to do so, subject to the following conditions:\n\n"
                "The above copyright notice and this permission notice shall be included in all "
                "copies or substantial portions of the Software.\n\n"
                "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR "
                "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, "
                "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE "
                "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER "
                "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, "
                "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE "
                "SOFTWARE.",
                classes="section_text about_section"
            )
            
            # Technology section
            yield Static("🛠️ Built With", classes="section_header")
            yield Static(
                "• Python 3.8+\n"
                "• Textual - Terminal UI framework\n"
                "• Rich - Beautiful text formatting",
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
