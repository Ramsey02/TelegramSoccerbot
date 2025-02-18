from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum

class GameStatus(Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Game:
    """Represents a soccer game event."""
    
    def __init__(self, game_id: str, chat_id: int, location: str, date: datetime, max_players: int, max_waitlist: int, created_by: int):
        self.game_id = game_id  # Unique identifier for the game
        self.chat_id = chat_id  # Telegram chat ID
        self.location = location  # Where the game will be played
        self.date = date  # When the game will be played
        self.max_players = max_players  # Maximum number of players allowed
        self.max_waitlist = max_waitlist  # Maximum number of players on the waiting list
        self.status = GameStatus.SCHEDULED
        self.players = []  # List of player user IDs
        self.waiting_list = []  # Waiting list if maximum reached
        self.created_by = created_by  # User ID of the game creator
    
    
    def is_full(self, list_type: str) -> bool:
        """Check if the game has reached max players."""
        if list_type == "players":
            return len(self.players) >= self.max_players
        else:
            return len(self.waiting_list) >= self.max_waitlist
    
    
    def available_spots(self, list_type: str) -> int:
        """Get the number of available spots."""
        if list_type == "players":
            return self.max_players - len(self.players)
        else:
            return self.max_waitlist - len(self.waiting_list)
    
    def add_player(self, user_id: int) -> bool:
        """Add a player to the game."""
        if not self.is_full("players"):
            self.players.append(user_id)
            return True
        else:  # If the game is full, add to waiting list if possible
            if not self.is_full("waiting_list"):
                self.waiting_list.append(user_id)
                return True
            return False
        
    def remove_player(self, user_id: int) -> bool:
        """Remove a player from the game."""
        if user_id in self.players:
            self.players.remove(user_id)
            return True
        elif user_id in self.waiting_list:
            self.waiting_list.remove(user_id)
            return True
        return False