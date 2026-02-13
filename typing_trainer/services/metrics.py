"""Metrics calculation service."""

from typing import Tuple


class MetricsCalculator:
    """Calculates typing metrics like WPM and accuracy."""
    
    @staticmethod
    def calculate_wpm(characters_typed: int, elapsed_seconds: float) -> float:
        """Calculate words per minute.
        
        Uses the standard definition: 1 word = 5 characters.
        
        Args:
            characters_typed: Number of characters typed
            elapsed_seconds: Time elapsed in seconds
            
        Returns:
            Words per minute (0 if elapsed_seconds is 0)
        """
        if elapsed_seconds <= 0:
            return 0.0
        
        # Standard: 1 word = 5 characters
        words = characters_typed / 5.0
        minutes = elapsed_seconds / 60.0
        
        return words / minutes if minutes > 0 else 0.0
    
    @staticmethod
    def calculate_accuracy(target_text: str, typed_text: str) -> float:
        """Calculate typing accuracy as a percentage.
        
        Compares each character position and calculates the percentage
        of correct characters.
        
        Args:
            target_text: The text that should have been typed
            typed_text: The text that was actually typed
            
        Returns:
            Accuracy percentage (0-100)
        """
        if not target_text:
            return 100.0
        
        if not typed_text:
            return 0.0
        
        correct_chars = 0
        comparison_length = min(len(target_text), len(typed_text))
        
        for i in range(comparison_length):
            if target_text[i] == typed_text[i]:
                correct_chars += 1
        
        # Penalize for length differences
        total_length = max(len(target_text), len(typed_text))
        accuracy = (correct_chars / total_length) * 100.0
        
        return accuracy
    
    @staticmethod
    def get_character_status(target_text: str, typed_text: str, position: int) -> str:
        """Get the status of a character at a specific position.
        
        Args:
            target_text: The text that should have been typed
            typed_text: The text that was actually typed
            position: The character position to check
            
        Returns:
            'correct', 'incorrect', or 'pending'
        """
        if position >= len(typed_text):
            return 'pending'
        
        if position >= len(target_text):
            return 'incorrect'  # Extra characters
        
        if target_text[position] == typed_text[position]:
            return 'correct'
        else:
            return 'incorrect'
