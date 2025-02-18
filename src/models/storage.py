from typing import Dict, List, Optional
from datetime import datetime
import uuid

from .player import Player
from .game import Game, GameStatus

class Storage:
    """Manages in-memory data for the bot without persistence."""
    
    def __init__(self):
        """Initialize storage with empty collections."""
        self.players: Dict[int, Player] = {}  # user_id -> Player
        self.games: Dict[str, Game] = {}      # game_id -> Game
    
    # Player operations
    def add_player(self, player: Player) -> None:
        """Add or update a player in storage."""
        self.players[player.user_id] = player
    
    def get_player(self, user_id: int) -> Optional[Player]:
        """Get a player by user ID."""
        return self.players.get(user_id)
    
    def remove_player(self, user_id: int) -> bool:
        """Remove a player. Returns True if successful."""
        if user_id in self.players:
            del self.players[user_id]
            return True
        return False
    
    def get_all_players(self) -> List[Player]:
        """Get all registered players."""
        return list(self.players.values())
    
    # Game operations
    def create_game(self, location: str, date: datetime, max_players: int, 
                    chat_id: int, created_by: Optional[int] = None) -> Game:
        """Create a new game with chat_id."""
        game_id = str(uuid.uuid4())
        game = Game(
            game_id=game_id,
            chat_id=chat_id,
            location=location,
            date=date,
            max_players=max_players,
            created_by=created_by or 0  # Default to 0 if None
        )
        self.games[game_id] = game
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
    def get_games_by_chat_id(self, chat_id: int) -> List[Game]:
        """Get all games for a chat."""
        return [game for game in self.games.values() if game.chat_id == chat_id]
    
