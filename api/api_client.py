"""
API client for Maple Story Universe (MSU) API
Using the official MSU API from https://msu.io/builder/docs
"""

import requests
import json
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from models.character import Character
from models.item import Item


class MSUApiClient:
    """Client for interacting with MapleStory Universe (MSU) API"""
    
    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key
        self.base_url = base_url or "https://api.msu.io"
        self.session = requests.Session()
        
        # Set up headers for MSU API
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        self.session.headers.update(headers)
    
    def get_top_characters(self, limit: int = 100, world: str = None) -> List[Character]:
        """
        Get top characters by ranking from MSU API
        
        Args:
            limit: Number of characters to return
            world: Specific world to get rankings from (optional)
        """
        try:
            # MSU API endpoint for character rankings
            endpoint = f"{self.base_url}/v1/characters/rankings"
            params = {
                'limit': min(limit, 100),
                'type': 'overall'  # overall, level, fame, etc.
            }
            
            if world:
                params['world'] = world
            
            response = self.session.get(endpoint, params=params)
            
            if response.status_code == 200:
                data = response.json()
                characters = []
                
                for rank_data in data.get('rankings', []):
                    char = Character(
                        rank=rank_data.get('rank', 0),
                        name=rank_data.get('name', 'Unknown'),
                        level=rank_data.get('level', 0),
                        job=rank_data.get('job', 'Unknown'),
                        guild=rank_data.get('guild'),
                        popularity=rank_data.get('fame', 0),
                        avatar_url=rank_data.get('avatar_url')
                    )
                    
                    # Get detailed character info for top 10
                    if char.rank <= 10:
                        char_details = self._get_character_details(char.name, world)
                        if char_details:
                            char.avatar_url = char_details.get('avatar_url', char.avatar_url)
                            char.equipment = char_details.get('equipment', {})
                    
                    characters.append(char)
                
                return characters[:limit]
            else:
                print(f"MSU API Error: {response.status_code}")
                print(f"Response: {response.text}")
                return self._get_mock_characters(limit)
                
        except Exception as e:
            print(f"Error getting top characters from MSU API: {str(e)}")
            return self._get_mock_characters(limit)
    
    def _get_character_details(self, character_name: str, world: str = None) -> Optional[Dict]:
        """Get detailed character information from MSU API"""
        try:
            endpoint = f"{self.base_url}/v1/characters/{character_name}"
            params = {}
            if world:
                params['world'] = world
            
            response = self.session.get(endpoint, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                # Parse equipment data
                equipment = {}
                for item_data in data.get('equipment', []):
                    slot = item_data.get('slot', 'unknown')
                    equipment[slot] = Item(
                        name=item_data.get('name', 'Unknown'),
                        slot=slot,
                        level=item_data.get('level', 0),
                        image_url=item_data.get('image_url')
                    )
                
                return {
                    'avatar_url': data.get('avatar_url'),
                    'equipment': equipment
                }
                
        except Exception as e:
            print(f"Error getting character details for {character_name}: {str(e)}")
        
        return None
    
    def get_character_details(self, character_name: str) -> Optional[Character]:
        """Get detailed information about a specific character"""
        try:
            endpoint = f"{self.base_url}/v1/characters/{character_name}"
            response = self.session.get(endpoint)
            
            if response.status_code == 200:
                data = response.json()
                
                char = Character(
                    rank=0,  # Rank not available in single character lookup
                    name=data.get('name', character_name),
                    level=data.get('level', 0),
                    job=data.get('job', 'Unknown'),
                    guild=data.get('guild'),
                    popularity=data.get('fame', 0),
                    avatar_url=data.get('avatar_url')
                )
                
                # Parse equipment
                equipment = {}
                for item_data in data.get('equipment', []):
                    slot = item_data.get('slot', 'unknown')
                    equipment[slot] = Item(
                        name=item_data.get('name', 'Unknown'),
                        slot=slot,
                        level=item_data.get('level', 0),
                        image_url=item_data.get('image_url')
                    )
                
                char.equipment = equipment
                return char
                
        except Exception as e:
            print(f"Error getting character details: {str(e)}")
        
        return None
    
    def search_characters(self, query: str, world: str = None) -> List[Character]:
        """Search for characters by name using MSU API"""
        try:
            endpoint = f"{self.base_url}/v1/characters/search"
            params = {
                'q': query,
                'limit': 50
            }
            if world:
                params['world'] = world
            
            response = self.session.get(endpoint, params=params)
            
            if response.status_code == 200:
                data = response.json()
                characters = []
                
                for char_data in data.get('characters', []):
                    char = Character(
                        rank=0,  # Search results don't include rank
                        name=char_data.get('name', 'Unknown'),
                        level=char_data.get('level', 0),
                        job=char_data.get('job', 'Unknown'),
                        guild=char_data.get('guild'),
                        popularity=char_data.get('fame', 0),
                        avatar_url=char_data.get('avatar_url')
                    )
                    characters.append(char)
                
                return characters
                
        except Exception as e:
            print(f"Error searching characters: {str(e)}")
        
        return []
    
    def get_worlds(self) -> List[str]:
        """Get available worlds from MSU API"""
        try:
            endpoint = f"{self.base_url}/v1/worlds"
            response = self.session.get(endpoint)
            
            if response.status_code == 200:
                data = response.json()
                return [world.get('name') for world in data.get('worlds', [])]
                
        except Exception as e:
            print(f"Error getting worlds: {str(e)}")
        
        return []
    
    def _get_mock_characters(self, limit: int) -> List[Character]:
        """Fallback mock data if MSU API is not available"""
        print("Warning: Using mock data. Please check your MSU API configuration.")
        
        mock_characters = []
        jobs = ["Hero", "Paladin", "Dark Knight", "Bowmaster", "Sniper", "Pathfinder"]
        guilds = ["Cross", "Frozen", "달치즈", "금별", "송이", "반달", "생글", None]
        names = ["TestWarrior", "DemoMage", "SampleArcher", "ExampleThief", "MockPirate", "Prototype"]
        
        for i in range(min(limit, 6)):
            mock_characters.append(Character(
                rank=i + 1,
                name=names[i % len(names)] + str(i + 1),
                level=275 + (i % 26),
                job=jobs[i % len(jobs)],
                guild=guilds[i % len(guilds)],
                popularity=max(100, 10000 - i * 1000)
            ))
        
        return mock_characters 