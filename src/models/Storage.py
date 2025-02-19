from typing import Dict, List, Optional
from datetime import datetime
import uuid

from .Player import Player
from .Game import Game

# define for different players in different games
class Storage:
    """Manages in-memory data for the bot without persistence."""
    
    def __init__(self):
        """Initialize storage with empty collections."""
        self.games: Dict[str, Game] = {}      # chat_id -> Game , game per chat group
        # each groupchat got its own players lists so that we can manage the players in the group chat 
        # each groupchat and user got thier own unique ids, 
        # so we can use the chat_id and user_id to identify the players in the group chat
        # and we can identify the player's groupchat by a defined function 
    
    # Player operations
    def add_player(self, player: Player, chat_id) -> bool:
        """Add or update a player in storage."""
        game = self.games[chat_id]
        return game.add_player(player)

    def get_player(self, user_id, chat_id) -> Optional[Player]:
        """Get a player by user ID."""
        game = self.games[chat_id]
        return game.get_player(user_id)
    
    def remove_player(self, user_id, chat_id) -> bool:
        """Remove a player. Returns True if successful."""
        game = self.games[chat_id]
        return game.remove_player(user_id)

    def get_all_players_in_play_list(self, chat_id) -> List[Player]:
        """Get all registered players."""
        game = self.games[chat_id]
        return game.get_all_players_names_on_play_list()
    
    def get_all_players_in_waiting_list(self, chat_id) -> List[Player]:
        """Get all registered players."""
        game = self.games[chat_id]
        return game.get_players_names_on_wait_list()
    
    # Game operations
    
    def create_game(self, chat_id,created_by = 0, max_players: int = 18,
                    date: datetime = datetime.now() , location: str=None) -> Game:
        """Create a new game with chat_id."""
        game = Game(
            chat_id=chat_id,
            location=location,
            date=date,
            max_players=max_players,
            max_waitlist=max_players+10,  # Default to 0 if None
            created_by=created_by  # Default to 0 if None
        )
        self.games[chat_id] = game
        return game
    
    def get_game(self, game_id) -> Optional[Game]:
        """Get a game by ID."""
        if game_id in self.games:
            return self.games.get(game_id)
        else:
            return None
        
    def is_group_registered(self, group_id) -> bool:
        """Check if a group is registered."""
        return group_id in self.games
    
    def update_game(self, game: Game) -> None:
        """Update a game in storage."""
        if game.game_id in self.games:
            self.games[game.game_id] = game
    
    def delete_game(self, game_id) -> bool:
        """Delete a game. Returns True if successful."""
        if game_id in self.games:
            del self.games[game_id]
            return True
        return False

    def is_football_group(self, group_id):
        """Check if a group is registered as a football group"""
        return group_id in self.games.get(group_id)

    def register_football_group(self, group_id):
        """Register a group as a football coordination group, just registeration, no games created"""
        """Return True if successful"""
        if group_id not in self.games:
            self.games[group_id] = None
            return True
        return False
    
