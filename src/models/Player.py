from datetime import datetime
from typing import Optional
from dataclasses import dataclass

@dataclass
class Player:
    """ represents an individual player in a soccer game"""
    
    def __init__(self, user_id: int, username: str, full_name: str, registration_date: datetime):
        self.user_id = user_id
        self.username = username
        self.full_name = full_name
        self.registration_date = registration_date

    @classmethod
    def from_update(cls, update):
        """ creates a new player object from a telegram update """
        user = update.message.from_user
        return cls(
            user_id=user.id,
            username=user.username or f"user_{user.id}",
            full_name=f"{user.first_name} {user.last_name or ''}".strip(),
            registration_date=datetime.now()
        )
