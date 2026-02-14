"""View showing instructions for adding custom exercises."""

from textual.screen import Screen
from textual.widgets import Header, Footer, Static
from textual.binding import Binding
from textual.reactive import reactive

INSTRUCTIONS_NORWEGIAN = """
[bold yellow]Hvordan legge til egne øvelser[/]

TouchPy lar deg legge til egne treningsfiler.

[bold green]Steg 1: Opprett mappe[/]
Lag en mappe kalt `exercises` i samme mappe som `TouchPy.exe`.

[bold green]Steg 2: Lag en tekstfil[/]
Lag en `.txt` fil inne i den nye mappen (f.eks `min_tekst.txt`).

[bold green]Steg 3: Filformat[/]
Filen må følge dette formatet:

1. [italic]Valgfritt:[/ italic] `Language: Norwegian` eller `Language: English` på første linje.
2. Tittel på øvelsen på neste linje.
3. Selve teksten som skal skrives.

[bold cyan]Eksempel på filinnhold:[/]
Language: Norwegian
Min egen øvelse
Dette er teksten som skal skrives.

[bold green]Steg 4: Start på nytt[/]
Start TouchPy på nytt, og øvelsen vil dukke opp i listen!
"""

INSTRUCTIONS_ENGLISH = """
[bold yellow]How to Add Custom Exercises[/]

TouchPy allows you to add your own exercise files.

[bold green]Step 1: Create Folder[/]
Create a folder named `exercises` next to `TouchPy.exe`.

[bold green]Step 2: Create Text File[/]
Create a `.txt` file inside that folder (e.g., `my_text.txt`).

[bold green]Step 3: File Format[/]
The file must follow this format:

1. [italic]Optional:[/ italic] `Language: English` or `Language: Norwegian` on the first line.
2. The title of the exercise on the next line.
3. The actual text to type.

[bold cyan]Example File Content:[/]
Language: English
My Custom Exercise
This is the text that should be typed.

[bold green]Step 4: Restart[/]
Restart TouchPy, and your exercise will appear in the list!
"""

class CustomExerciseInstructionsView(Screen):
    """Screen showing instructions for custom exercises."""
    
    BINDINGS = [
        Binding("escape", "back", "Back"),
        Binding("m", "back", "Back to Menu"),
        Binding("l", "toggle_language", "Toggle Language (Eng/Nor)"),
    ]
    
    current_text = reactive(INSTRUCTIONS_NORWEGIAN)
    is_norwegian = reactive(True)
    
    CSS = """
    CustomExerciseInstructionsView {
        align: center middle;
    }
    
    #content {
        width: 80;
        height: auto;
        border: solid $accent;
        padding: 1 2;
        background: $surface;
        color: $text;
    }
    
    #title {
        content-align: center middle;
        text-style: bold;
        margin-bottom: 1;
        color: $primary;
    }
    """
    
    def compose(self):
        yield Header()
        yield Static("Custom Exercises Help (Press 'L' to switch language)", id="title")
        yield Static(self.current_text, id="content")
        yield Footer()
        
    def action_back(self):
        """Go back to the previous screen."""
        self.app.pop_screen()

    def action_toggle_language(self):
        """Switch between English and Norwegian instructions."""
        self.is_norwegian = not self.is_norwegian
        if self.is_norwegian:
            self.current_text = INSTRUCTIONS_NORWEGIAN
        else:
            self.current_text = INSTRUCTIONS_ENGLISH
            
    def watch_current_text(self, new_text: str) -> None:
        """Update the content when current_text changes."""
        try:
            content_widget = self.query_one("#content", Static)
            content_widget.update(new_text)
        except Exception:
            pass
