from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum
from models.Player import Player

class Game:
    """Represents a soccer game event."""
    
    def __init__(self, chat_id, location: str, date: datetime, max_players: int, 
                 max_waitlist = 0, created_by = 0):
        """
        Initialize a new game.

        :param chat_id: Telegram chat ID
        :param location: Where the game will be played
        :param date: When the game will be played
        :param max_players: Maximum number of players allowed
        :param max_waitlist: Maximum number of players on the waiting list (default is max_players + 10)
        :param created_by: User ID of the game creator (default is 0)
        """
        if max_waitlist == 0:
            max_waitlist = max_players + 10
        self.chat_id = chat_id  # Telegram chat ID
        self.location = location  # Where the game will be played
        self.date = date  # When the game will be played
        self.max_players = max_players  # Maximum number of players allowed
        self.max_waitlist = max_waitlist  # Maximum number of players on the waiting list
        self.players = []  # List of player user IDs
        self.waiting_list = []  # Waiting list if maximum reached
        self.created_by = created_by  # User ID of the game creator
      
    def add_player(self,  new_player: Player) -> bool:
        """Add a player to the game."""
        if len(self.players) < self.max_players:
            self.players.append(new_player)
            return True
        elif len(self.waiting_list) < self.max_waitlist:
            self.waiting_list.append(new_player)
            return True
        return False
        
    def remove_player(self, user_id) -> bool:
        """Remove a player from the game."""
        if user_id in [player.user_id for player in self.players]:
            player = self.get_player(user_id)
            # !! check if this compasion holds true from the player class
            self.players.remove(player)
            return True
        elif user_id in [player.user_id for player in self.waiting_list]:
            player = self.get_player(user_id)
            self.waiting_list.remove(player)
            return True
        return False
    
    def get_player(self,user_id)->Player:
        """Get a player by user ID."""
        for player in self.players:
            if player.user_id == user_id:
                return player
        for player in self.waiting_list:
            if player.user_id == user_id:
                return player
        return None
    
    def is_player_on_play_list(self,player: Player)->bool:
        """Check if a player is on the play list"""
        return player in self.players
    
    def is_player_on_wait_list(self,player: Player)->bool:
        """Check if a player is on the wait list"""
        return player in self.waiting_list
    
    def get_all_players_names_on_play_list(self)->List[str]:
        """Get all the players names"""
        return [player.full_name for player in self.players]
    
    def get_players_names_on_wait_list(self)->List[str]:
        """Get all the players names"""
        return [player.full_name for player in self.waiting_list]
    
    def get_num_players(self)->int:
        """Get the number of players"""
        return len(self.players)
    
    def get_num_players_on_wait_list(self)->int:    
        """Get the number of players"""
        return len(self.waiting_list)
    
    def get_num_players_total(self)->int:
        """Get the number of players"""
        return len(self.players) + len(self.waiting_list)
