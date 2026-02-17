import re
from rich.text import Text
from .views.finger_map_view_compact import FINGER_MAP_ENGLISH, FINGER_MAP_NORWEGIAN


def get_layout(name, highlight_key=None, error_keys=None):
    """Get the keyboard layout with optional highlighting.
    
    Args:
        name: Layout name ("English" or "Norwegian")
        highlight_key: Character to highlight as next key to press
        error_keys: List of characters to highlight as error keys
        
    Returns:
        Rich Text object with the keyboard layout
    """
    # Get the appropriate finger map
    if name and name.lower() == "norwegian":
        layout_str = FINGER_MAP_NORWEGIAN
    else:
        layout_str = FINGER_MAP_ENGLISH
    
    # Track if space should be highlighted
    space_style = None
    
    # Apply error highlighting first (red background)
    if error_keys:
        for char in error_keys:
            if not char:
                continue
            
            # Handle space - mark for later
            if char == ' ':
                space_style = "white on red"
                continue
            
            if not char.strip():
                continue
            
            # Try both upper and lower case
            for ch in [char.upper(), char.lower()]:
                layout_str = _highlight_char(layout_str, ch, "white on red")
    
    # Apply next key highlighting (blue background with white text) - this takes precedence
    if highlight_key:
        if highlight_key == ' ':
            # Highlight space bar (overrides error style if set)
            space_style = "white on blue"
        elif highlight_key.strip():
            # Try both upper and lower case
            for ch in [highlight_key.upper(), highlight_key.lower()]:
                layout_str = _highlight_char(layout_str, ch, "white on blue")
    
    # Apply space bar highlighting if needed
    if space_style:
        layout_str = layout_str.replace("MELLOMROMSTAST", f"[{space_style}]MELLOMROMSTAST[/{space_style}]")
        layout_str = layout_str.replace("SPACE BAR", f"[{space_style}]SPACE BAR[/{space_style}]")
    
    # Convert to Rich Text object
    from rich.markup import render
    return Text.from_markup(layout_str)


def _highlight_char(layout_str, char, style):
    """Helper function to highlight a specific character in the layout.
    
    Args:
        layout_str: The layout string with Rich markup
        char: Character to highlight  
        style: Rich style to apply (e.g., "white on blue")
        
    Returns:
        Modified layout string
    """
    # Escape special regex characters
    escaped_char = re.escape(char)
    
    # Pattern to match the character within any color tag
    # The structure is: │[color]  CHAR [/color] │ (2 spaces before, 1 space after)
    # Or: │[color]  CHAR  [/color]│ (2 spaces before, 2 spaces after)
    
    # Try to find and replace the character with various spacing patterns
    patterns = [
        # Standard pattern: │[color]  CHAR [/color] │
        (rf'│\[[a-z]+\](  {escaped_char} )\[/[a-z]+\] │', rf'│[{style}]\1[/{style}] │'),
        # Alternative: │[color]  CHAR  [/color]│
        (rf'│\[[a-z]+\](  {escaped_char}  )\[/[a-z]+\]│', rf'│[{style}]\1[/{style}]│'),
        # For special keys like TAB, CAPS, SHIFT, BKSP, ENTER
        (rf'│\[[a-z]+\]({escaped_char})\[/[a-z]+\] │', rf'│[{style}]\1[/{style}] │'),
    ]
    
    for pattern, replacement in patterns:
        layout_str = re.sub(pattern, replacement, layout_str, flags=re.IGNORECASE)
    
    return layout_str
