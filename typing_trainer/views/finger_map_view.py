"""Finger map view showing which finger to use for each key."""

from textual.screen import Screen
from textual.widgets import Header, Footer, Static
from textual.binding import Binding
from textual.reactive import reactive


FINGER_MAP_ENGLISH = """
┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────────┐
│[magenta]  ~ [/magenta] │[magenta]  ! [/magenta] │[yellow]  @  [/yellow]│[blue]  #  [/blue]│[green]  $  [/green]│[green]  %  [/green]│[green]  ^  [/green]│[green]  &  [/green]│[blue]  *  [/blue]│[yellow]  (  [/yellow]│[magenta]  ) [/magenta] │[magenta]  _ [/magenta] │[magenta]  + [/magenta] │[magenta]        [/magenta] │
│[magenta]  ` [/magenta] │[magenta]  1 [/magenta] │[yellow]  2  [/yellow]│[blue]  3  [/blue]│[green]  4  [/green]│[green]  5  [/green]│[green]  6  [/green]│[green]  7  [/green]│[blue]  8  [/blue]│[yellow]  9  [/yellow]│[magenta]  0 [/magenta] │[magenta]  - [/magenta] │[magenta]  = [/magenta] │[magenta]   BKSP [/magenta] │
├─────┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──────┤
│[magenta]       [/magenta] │[magenta]  Q [/magenta] │[yellow]  W  [/yellow]│[blue]  E  [/blue]│[green]  R  [/green]│[green]  T  [/green]│[green]  Y  [/green]│[green]  U  [/green]│[blue]  I  [/blue]│[yellow]  O  [/yellow]│[magenta]  P [/magenta] │[magenta]  { [/magenta] │[magenta]  } [/magenta] │[magenta]     [/magenta] │
│[magenta]  TAB  [/magenta] │[magenta]  q [/magenta] │[yellow]  w  [/yellow]│[blue]  e  [/blue]│[green]  r  [/green]│[green]  t  [/green]│[green]  y  [/green]│[green]  u  [/green]│[blue]  i  [/blue]│[yellow]  o  [/yellow]│[magenta]  p [/magenta] │[magenta]    [/magenta] │[magenta]    [/magenta] │[magenta]     [/magenta] │
├────────┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┘      │
│[magenta]         [/magenta] │[magenta]  A [/magenta] │[yellow]  S  [/yellow]│[blue]  D  [/blue]│[green]  F  [/green]│[green]  G  [/green]│[green]  H  [/green]│[green]  J  [/green]│[blue]  K  [/blue]│[yellow]  L  [/yellow]│[magenta]  : [/magenta] │[magenta]  " [/magenta] │[magenta]         [/magenta] │
│[magenta]   CAPS  [/magenta] │[magenta]  a [/magenta] │[yellow]  s  [/yellow]│[blue]  d  [/blue]│[green]  f  [/green]│[green]  g  [/green]│[green]  h  [/green]│[green]  j  [/green]│[blue]  k  [/blue]│[yellow]  l  [/yellow]│[magenta]  ; [/magenta] │[magenta]  ' [/magenta] │[magenta]   ENTER [/magenta] │
├──────────┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──────────┤
│[magenta]            [/magenta] │[magenta]  Z [/magenta] │[yellow]  X  [/yellow]│[blue]  C  [/blue]│[green]  V  [/green]│[green]  B  [/green]│[green]  N  [/green]│[green]  M  [/green]│[blue]  <  [/blue]│[yellow]  >  [/yellow]│[magenta]  ? [/magenta] │[magenta]            [/magenta] │
│[magenta]    SHIFT   [/magenta] │[magenta]  z [/magenta] │[yellow]  x  [/yellow]│[blue]  c  [/blue]│[green]  v  [/green]│[green]  b  [/green]│[green]  n  [/green]│[green]  m  [/green]│[blue]  ,  [/blue]│[yellow]  .  [/yellow]│[magenta]  / [/magenta] │[magenta]    SHIFT   [/magenta] │
└─────────────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────────────┘

                    FINGER PLACEMENT GUIDE:
        
        LEFT HAND                          RIGHT HAND
        ─────────                          ──────────
        [magenta]Pinky[/magenta]:  A                          [magenta]Pinky[/magenta]:  ;
        [yellow]Ring[/yellow]:   S                          [yellow]Ring[/yellow]:   L
        [blue]Middle[/blue]: D                          [blue]Middle[/blue]: K
        [green]Index[/green]:  F (has bump)               [green]Index[/green]:  J (has bump)
        
        Thumbs: SPACE BAR
        
        ┌─────────────────────────────────────────────────┐
        │  F and J keys have small bumps to help you      │
        │  find the home row position without looking.    │
        └─────────────────────────────────────────────────┘
"""

FINGER_MAP_NORWEGIAN = """

┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬──────────┐
│[magenta]  ~ [/magenta] │[magenta]  ! [/magenta] │[yellow]  @  [/yellow]│[blue]  #  [/blue]│[green]  $  [/green]│[green]  %  [/green]│[green]  ^  [/green]│[green]  &  [/green]│[blue]  *  [/blue]│[yellow]  (  [/yellow]│[magenta]  ) [/magenta] │[magenta]  _ [/magenta] │[magenta]  + [/magenta] │[magenta]       [/magenta]   │
│[magenta]  ` [/magenta] │[magenta]  1 [/magenta] │[yellow]  2  [/yellow]│[blue]  3  [/blue]│[green]  4  [/green]│[green]  5  [/green]│[green]  6  [/green]│[green]  7  [/green]│[blue]  8  [/blue]│[yellow]  9  [/yellow]│[magenta]  0 [/magenta] │[magenta]  - [/magenta] │[magenta]  = [/magenta] │[magenta]   BKSP  [/magenta] │
├─────┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬───────┤
│[magenta]       [/magenta] │[magenta]  Q [/magenta] │[yellow]  W  [/yellow]│[blue]  E  [/blue]│[green]  R  [/green]│[green]  T  [/green]│[green]  Y  [/green]│[green]  U  [/green]│[blue]  I  [/blue]│[yellow]  O  [/yellow]│[magenta]  P [/magenta] │[magenta]  Å [/magenta] │[magenta]  ^ [/magenta] │[magenta]    [/magenta]   │
│[magenta]  TAB  [/magenta] │[magenta]  q [/magenta] │[yellow]  w  [/yellow]│[blue]  e  [/blue]│[green]  r  [/green]│[green]  t  [/green]│[green]  y  [/green]│[green]  u  [/green]│[blue]  i  [/blue]│[yellow]  o  [/yellow]│[magenta]  p [/magenta] │[magenta]  å [/magenta] │[magenta] ¨ ~[/magenta] │[magenta] ENTER [/magenta]│
├────────┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┐     │
│[magenta]         [/magenta] │[magenta]  A [/magenta] │[yellow]  S  [/yellow]│[blue]  D  [/blue]│[green]  F  [/green]│[green]  G  [/green]│[green]  H  [/green]│[green]  J  [/green]│[blue]  K  [/blue]│[yellow]  L  [/yellow]│[magenta]  Ø [/magenta] │[magenta]  Æ [/magenta] │[magenta]  * [/magenta] │[magenta]    [/magenta] │
│[magenta]   CAPS  [/magenta] │[magenta]  a [/magenta] │[yellow]  s  [/yellow]│[blue]  d  [/blue]│[green]  f  [/green]│[green]  g  [/green]│[green]  h  [/green]│[green]  j  [/green]│[blue]  k  [/blue]│[yellow]  l  [/yellow]│[magenta]  ø [/magenta] │[magenta]  æ [/magenta] │[magenta]  ' [/magenta] │[magenta]    [/magenta] │
├──────────┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴─────┴─────┤
│[magenta]            [/magenta] │[magenta]  Z [/magenta] │[yellow]  X  [/yellow]│[blue]  C  [/blue]│[green]  V  [/green]│[green]  B  [/green]│[green]  N  [/green]│[green]  M  [/green]│[blue]  ;  [/blue]│[yellow]  :  [/yellow]│[magenta]  - [/magenta] │[magenta]             [/magenta] │
│[magenta]    SHIFT   [/magenta] │[magenta]  z [/magenta] │[yellow]  x  [/yellow]│[blue]  c  [/blue]│[green]  v  [/green]│[green]  b  [/green]│[green]  n  [/green]│[green]  m  [/green]│[blue]  ,  [/blue]│[yellow]  .  [/yellow]│[magenta]  - [/magenta] │[magenta]    SHIFT    [/magenta] │
└─────────────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴──────────────┘

                    PLASSERING AV FINGRE:
        
        VENSTRE HÅND                       HØYRE HÅND
        ────────────                       ──────────
        [magenta]Lillefinger[/magenta]:  A                    [magenta]Lillefinger[/magenta]:  ;
        [yellow]Ringfinger[/yellow]:   S                    [yellow]Ringfinger[/yellow]:   L
        [blue]Langfinger[/blue]:   D                    [blue]Langfinger[/blue]:   K
        [green]Pekefinger[/green]:   F (har markering)    [green]Pekefinger[/green]:   J (har markering)
        
        Tommelfingre: MELLOMROMSTAST
        
        ┌─────────────────────────────────────────────────┐
        │  F- og J-tastene har små markeringer for å      │
        │  hjelpe deg finne grunnposisjonen uten å se.    │
        └─────────────────────────────────────────────────┘
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
        width: 100%;
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

