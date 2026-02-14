"""Data models for the typing trainer application."""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Exercise:
    """Represents a typing exercise.
    
    Attributes:
        id: Unique identifier for the exercise (typically the filename)
        title: Display title of the exercise
        text: The text content to type
        source_path: Path to the source file
        layout: The keyboard layout to use (e.g. "English", "Norwegian")
    """
    id: str
    title: str
    text: str
    source_path: Path
    layout: str = "English"
    
    @property
    def word_count(self) -> int:
        """Calculate the number of words in the exercise text."""
        return len(self.text.split())
