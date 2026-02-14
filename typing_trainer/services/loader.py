"""Exercise loader service."""

from pathlib import Path
from typing import List
from ..models import Exercise


class ExerciseLoader:
    """Loads exercises from .txt files in one or more directories."""
    
    def __init__(self, exercises_dirs):
        """Initialize the loader with exercises directory/directories.
        
        Args:
            exercises_dirs: Path or list of Paths to directories containing exercise files
        """
        # Support both single path and list of paths
        if isinstance(exercises_dirs, (Path, str)):
            self.exercises_dirs = [Path(exercises_dirs)]
        else:
            self.exercises_dirs = [Path(d) for d in exercises_dirs]
    
    def load_exercises(self) -> List[Exercise]:
        """Load all exercises from .txt files in all exercises directories.
        
        Returns:
            List of Exercise objects sorted by filename
        """
        exercises = []
        seen_ids = set()  # Track IDs to avoid duplicates
        
        # Load from all directories (external directory first for priority)
        for exercises_dir in reversed(self.exercises_dirs):
            if not exercises_dir.exists():
                continue
            
            # Find all .txt files in the exercises directory
            txt_files = sorted(exercises_dir.glob("*.txt"))
            
            for file_path in txt_files:
                try:
                    exercise = self._load_exercise(file_path)
                    # Only add if we haven't seen this ID before (external overrides internal)
                    if exercise.id not in seen_ids:
                        exercises.append(exercise)
                        seen_ids.add(exercise.id)
                except Exception as e:
                    # Skip files that can't be loaded
                    print(f"Warning: Could not load {file_path}: {e}")
        
        # Sort by ID to maintain consistent order
        exercises.sort(key=lambda e: e.id)
        return exercises
    
    def _load_exercise(self, file_path: Path) -> Exercise:
        """Load a single exercise from a file.
        
        The file may optionally start with metadata tags like 'keyboard-layout: Norwegian'.
        The first non-metadata line is the title, and the remaining lines are the exercise text.
        
        Args:
            file_path: Path to the exercise file
            
        Returns:
            Exercise object
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if not lines:
            raise ValueError("Exercise file is empty")
        
        layout = "English"
        start_index = 0
        
        # Parse metadata
        while start_index < len(lines):
            line = lines[start_index].strip()
            if line.lower().startswith("keyboard-layout:") or line.lower().startswith("language:"):
                value = line.split(":", 1)[1].strip()
                if "norwegian" in value.lower():
                    layout = "Norwegian"
                elif "english" in value.lower():
                    layout = "English"
                start_index += 1
            else:
                break
        
        if start_index >= len(lines):
             raise ValueError("Exercise file has only metadata or is empty")

        # First non-metadata line is the title
        title = lines[start_index].strip()
        
        # Rest is the exercise text
        text = ''.join(lines[start_index + 1:]).strip()
        
        if not text:
            # If text is empty, maybe the title was the text?
            # But based on spec, title is mandatory.
             raise ValueError("Exercise text is empty")
        
        # Use filename (without extension) as ID
        exercise_id = file_path.stem
        
        return Exercise(
            id=exercise_id,
            title=title,
            text=text,
            source_path=file_path,
            layout=layout
        )
