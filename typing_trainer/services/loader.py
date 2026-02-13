"""Exercise loader service."""

from pathlib import Path
from typing import List
from ..models import Exercise


class ExerciseLoader:
    """Loads exercises from .txt files in a directory."""
    
    def __init__(self, exercises_dir: Path):
        """Initialize the loader with an exercises directory.
        
        Args:
            exercises_dir: Path to the directory containing exercise files
        """
        self.exercises_dir = exercises_dir
    
    def load_exercises(self) -> List[Exercise]:
        """Load all exercises from .txt files in the exercises directory.
        
        Returns:
            List of Exercise objects sorted by filename
        """
        exercises = []
        
        if not self.exercises_dir.exists():
            return exercises
        
        # Find all .txt files in the exercises directory
        txt_files = sorted(self.exercises_dir.glob("*.txt"))
        
        for file_path in txt_files:
            try:
                exercise = self._load_exercise(file_path)
                exercises.append(exercise)
            except Exception as e:
                # Skip files that can't be loaded
                print(f"Warning: Could not load {file_path}: {e}")
        
        return exercises
    
    def _load_exercise(self, file_path: Path) -> Exercise:
        """Load a single exercise from a file.
        
        The first line of the file is the title, and the remaining lines
        are the exercise text.
        
        Args:
            file_path: Path to the exercise file
            
        Returns:
            Exercise object
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if not lines:
            raise ValueError("Exercise file is empty")
        
        # First line is the title
        title = lines[0].strip()
        
        # Rest is the exercise text
        text = ''.join(lines[1:]).strip()
        
        if not text:
            raise ValueError("Exercise text is empty")
        
        # Use filename (without extension) as ID
        exercise_id = file_path.stem
        
        return Exercise(
            id=exercise_id,
            title=title,
            text=text,
            source_path=file_path
        )
