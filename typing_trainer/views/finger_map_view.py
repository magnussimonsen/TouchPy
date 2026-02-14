"""Finger map view showing which finger to use for each key."""

from textual.screen import Screen
from textual.widgets import Header, Footer, Static
from textual.binding import Binding
from textual.reactive import reactive


FINGER_MAP_ENGLISH = r"""
LEFT HAND                                   RIGHT HAND
Pinky  Ring   Middle Index          Index  Middle Ring   Pinky
 .--.  .--.   .--.   .--.           .--.   .--.   .--.   .--.
 |  |  |  |   |  |   |  |           |  |   |  |   |  |   |  |
 |Q |  |W |   |E |   |R |           |U |   |I |   |O |   |P |
 |A |  |S |   |D |   |F |           |J |   |K |   |L |   |; |
 |Z |  |X |   |C |   |V |           |M |   |, |   |. |   |/ |
 '  '  '  '   '  '   '  '           '  '   '  '   '  '   '  '
  /      /      /      /             \      \      \      \
 1      2      3      4               4      3      2      1
 
ENGLISH Key Mapping:
[1] Pinky:  1 Q A Z      |      [1] Pinky:  0 P ; / - = ' [ ]
[2] Ring:   2 W S X      |      [2] Ring:   9 O L .
[3] Middle: 3 E D C      |      [3] Middle: 8 I K ,
[4] Index:  4 R F V      |      [4] Index:  7 U J M
            5 T G B      |                  6 Y H N
            
Thumbs: SPACE BAR
"""

FINGER_MAP_NORWEGIAN = r"""
VENSTRE HÅND                                HØYRE HÅND
Lille  Ring   Lang   Peke           Peke   Lang   Ring   Lille
 .--.  .--.   .--.   .--.           .--.   .--.   .--.   .--.
 |  |  |  |   |  |   |  |           |  |   |  |   |  |   |  |
 |Q |  |W |   |E |   |R |           |U |   |I |   |O |   |P |
 |A |  |S |   |D |   |F |           |J |   |K |   |L |   |Ø |
 |< |  |Z |   |X |   |C |           |M |   |, |   |. |   |- |
 '  '  '  '   '  '   '  '           '  '   '  '   '  '   '  '
  /      /      /      /             \      \      \      \
 1      2      3      4               4      3      2      1
 
NORSK Tasteoversikt:
[1] Lille:  1 Q A < Z    |      [1] Lille:  0 P Å + \ ' ¨ ^ *
[2] Ring:   2 W S X      |      [2] Ring:   9 O L . Ø
[3] Lang:   3 E D C      |      [3] Lang:   8 I K , Æ
[4] Peke:   4 R F V      |      [4] Peke:   7 U J M
            5 T G B      |                  6 Y H N
            
Tomler: MELLOMROM (SPACE)
"""

class FingerMapView(Screen):
    """Screen showing the touch typing finger map."""
    
    BINDINGS = [
        Binding("escape", "back", "Back"),
        Binding("m", "back", "Back to Menu"),
        Binding("l", "toggle_language", "Toggle Language (Eng/Nor)"),
    ]
    
    current_map = reactive(FINGER_MAP_NORWEGIAN)
    is_norwegian = reactive(True)
    
    CSS = """
    FingerMapView {
        align: center middle;
    }
    
    #map_container {
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
        yield Static("Touch Typing Finger Map (Press 'L' to switch)", id="title")
        yield Static(self.current_map, id="map_container")
        yield Footer()
        
    def action_back(self):
        """Go back to the previous screen."""
        self.app.pop_screen()
        
    def action_toggle_language(self):
        """Switch between English and Norwegian finger maps."""
        self.is_norwegian = not self.is_norwegian
        if self.is_norwegian:
            self.current_map = FINGER_MAP_NORWEGIAN
        else:
            self.current_map = FINGER_MAP_ENGLISH
            
    def watch_current_map(self, new_map: str) -> None:
        """Update the map display when current_map changes."""
        try:
            map_widget = self.query_one("#map_container", Static)
            map_widget.update(new_map)
        except Exception:
            pass

