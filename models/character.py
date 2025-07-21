"""
Character data model
"""

from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class Character:
    """Model representing a MapleStory character"""
    rank: int
    name: str
    level: int
    job: str
    guild: Optional[str] = None
    popularity: int = 0
    avatar_url: Optional[str] = None
    world: Optional[str] = None
    exp: int = 0
    equipment: Optional[Dict] = None
    
    def __str__(self):
        return f"{self.name} (Lv.{self.level} {self.job})"
    
    def to_dict(self):
        """Convert character to dictionary"""
        return {
            "rank": self.rank,
            "name": self.name,
            "level": self.level,
            "job": self.job,
            "guild": self.guild,
            "popularity": self.popularity,
            "avatar_url": self.avatar_url,
            "world": self.world,
            "exp": self.exp
        } 