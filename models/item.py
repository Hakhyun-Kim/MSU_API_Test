"""
Item data model
"""

from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class Item:
    """Model representing a MapleStory item"""
    name: str
    slot: str
    level: int = 0
    image_url: Optional[str] = None
    item_id: Optional[int] = None
    stats: Optional[Dict] = None
    potential: Optional[str] = None
    stars: int = 0
    
    def __str__(self):
        return f"{self.name} ({self.slot})"
    
    def to_dict(self):
        """Convert item to dictionary"""
        return {
            "name": self.name,
            "slot": self.slot,
            "level": self.level,
            "image_url": self.image_url,
            "item_id": self.item_id,
            "stats": self.stats,
            "potential": self.potential,
            "stars": self.stars
        } 