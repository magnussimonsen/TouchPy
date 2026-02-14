import re
from rich.text import Text

NORWEGIAN_LAYOUT = r"""
  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9  |  0  |  +  |  \  |           
  |  Q  |  W  |  E  |  R  |  T  |  Y  |  U  |  I  |  O  |  P  |  Å  |  ¨  |
  |  A  |  S  |  D  |  F  |  G  |  H  |  J  |  K  |  L  |  Ø  |  Æ  |  '  |
  |  <  |  Z  |  X  |  C  |  V  |  B  |  N  |  M  |  ,  |  .  |  -  |
                    |           SPACE           |
"""

ENGLISH_LAYOUT = r"""
  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9  |  0  |  -  |  =  |
  |  Q  |  W  |  E  |  R  |  T  |  Y  |  U  |  I  |  O  |  P  |  [  |  ]  |
  |  A  |  S  |  D  |  F  |  G  |  H  |  J  |  K  |  L  |  ;  |  '  |  \  |
  |  Z  |  X  |  C  |  V  |  B  |  N  |  M  |  ,  |  .  |  /  |
                    |           SPACE           |
"""

def get_layout(name, highlight_key=None, error_keys=None):
    layout_str = ENGLISH_LAYOUT
    if name and name.lower() == "norwegian":
        layout_str = NORWEGIAN_LAYOUT
    
    # Create a Rich Text object from the raw string
    # This ensures characters like [ and ] are treated as literal text, not markup
    text = Text(layout_str)
    
    if error_keys:
        for char in error_keys:
            if not char:
                continue
            
            # Handle space errors specifically
            if char == ' ':
                try:
                    text.highlight_regex(r"SPACE", "bold white on red")
                except Exception:
                    pass
                continue

            if not char.strip():
                continue

            char = char.upper()
            escaped_char = re.escape(char)
            # Find key surrounded by spaces
            pattern = f"(?<=  ){escaped_char}(?=  )"
            try:
                text.highlight_regex(pattern, "bold white on red")
            except Exception:
                pass

    if highlight_key:
        # Handle space highlight specifically
        if highlight_key == ' ':
            try:
                text.highlight_regex(r"SPACE", "bold white on blue")
            except Exception:
                pass
        
        elif highlight_key.strip():
            # Find the key to highlight
            # We look for the character surrounded by spaces to ensure we match the key cap
            char = highlight_key.upper()
            
            # Determine the regex pattern based on the character
            # We want to match "  CHAR  " pattern which is common in the layout
            # Escape the char to handle special regex characters safely
            escaped_char = re.escape(char) 
            pattern = f"(?<=  ){escaped_char}(?=  )"
            
            # Apply the style to the matches
            # We use a bright blue color for visibility
            try:
                text.highlight_regex(pattern, "bold white on blue")
            except Exception:
                # If regex fails for some reason, just return unhighlighted text
                pass
            
    return text
