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
    def add_player(self, player: Player, chat_id : int) -> bool:
        """Add or update a player in storage."""
        if chat_id not in self.games:
            return False
        game = self.games[chat_id]
        game.add_player(player.user_id)
        return True
        
    def get_player(self, user_id: int, chat_id : int) -> Optional[Player]:
        """Get a player by user ID."""
        if chat_id not in self.games:
            return None
        game = self.games[chat_id]
        if user_id in game.players:
            return game.players[user_id]
        return None
    
    def remove_player(self, user_id: int, chat_id : int) -> bool:
        """Remove a player. Returns True if successful."""
        if chat_id not in self.games:
            return False
        game = self.games[chat_id]
        if user_id in game.players:
            game.remove_player(user_id)
            return True
        return False
    
    def get_all_players(self, chat_id : int) -> List[Player]:
        """Get all registered players."""
        if chat_id not in self.games:
            return []
        game = self.games[chat_id]
        return game.players.values()
    
    # Game operations
    def create_game(self, chat_id: int, max_players: int = 18 , created_by: Optional[int] = None, date: datetime = datetime.now()
                    ,location: str = None) -> Game:
        """Create a new game with chat_id."""
        game = Game(
            chat_id=chat_id,
            location=location,
            date=date,
            max_players=max_players,
            max_waitlist=max_players+10,  # Default to 0 if None
            created_by=created_by or 0  # Default to 0 if None
        )
        self.games[chat_id] = game
        return game
    
    def get_game(self, game_id: str) -> Optional[Game]:
        """Get a game by ID."""
        return self.games.get(game_id)
    
    def update_game(self, game: Game) -> None:
        """Update a game in storage."""
        if game.game_id in self.games:
            self.games[game.game_id] = game
    
    def delete_game(self, game_id: str) -> bool:
        """Delete a game. Returns True if successful."""
        if game_id in self.games:
            del self.games[game_id]
            return True
        return False

    def is_football_group(self, group_id):
        """Check if a group is registered as a football group"""
        return group_id in self.games.get(group_id)

    def register_football_group(self, group_id,user_id):
        """Register a group as a football coordination group"""
        if group_id not in self.games:
            self.games[group_id] = self.create_game(group_id, max_players=18, created_by=user_id, date=datetime.now(), location="default")
            return True
        return False
    
