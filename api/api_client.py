"""
API client for Maple Story Universe
"""

import requests
import json
from typing import List, Dict, Optional
from models.character import Character
from models.item import Item


class MSUApiClient:
    """Client for interacting with Maple Story Universe API"""
    
    def __init__(self, base_url: str = None, api_key: str = None):
        # Since real MSU API requires registration, we'll use mock data for now
        self.base_url = base_url or "https://api.maplestory.net"
        self.api_key = api_key
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})
            
    def get_top_characters(self, limit: int = 100) -> List[Character]:
        """
        Get top characters by ranking
        For now, returns mock data
        """
        # Mock data based on the Korean ranking page we saw
        mock_characters = [
            {
                "rank": 1,
                "name": "오지환",
                "level": 300,
                "job": "키네시스",
                "guild": "투나",
                "popularity": 90272,
                "avatar_url": "https://avatar.maplestory.nexon.com/Character/180/IBLILGNFJLEHBEHOKIDMCAPJNPFOMODAJBLGKNPDFIGGPLKFDMGLMEBFOEMGIALGINCLFOGKGMIAMCDJALLKBCOJCCHKGPJKHANKAKHEICJFAIDPDIKOKHMOMGBEPBJCFENECMNGOGLJHAJJLOHCCBCGOIEDMJAAPFFDPMINHMPBKPLFNDMLNFLOLOPOFHCMNGABJIGGPEAIHGPCNMLJKKFMKGJLJJIIIAJCOKHCFKCDLAEICNMGPDOLJABPJAGP.png"
            },
            {
                "rank": 2,
                "name": "버터",
                "level": 300,
                "job": "나이트로드",
                "guild": "루루",
                "popularity": 3841,
                "avatar_url": "https://avatar.maplestory.nexon.com/Character/180/AFDGDIKAMNCDOGCIENDCJOGEJDELIDEGADDAAMIMNCLMAJGCGOOFCFFALPNAEKNMKOJDHEAOJDMJNLDONJEHOLGEFPFMFNMCBOBEOELFIMODPJNHHDOGMIEHBKAPCAHLFKHLAICBALEJIEKABFIHCCKNFDEIHCMKJCHHIGFJLINPOGBBIKLPBIMMJDMKLIENEGJENEDMPMIMMDOHPADPBAGMAFOKOOFHANPLLEICMKJOIALPGAFBEGKKKKNHDJGI.png"
            },
            {
                "rank": 3,
                "name": "테룽이",
                "level": 300,
                "job": "카이저",
                "guild": "프라하",
                "popularity": 1145,
                "avatar_url": "https://avatar.maplestory.nexon.com/Character/180/KGCMALLHFGKMDDACLIJLPBLGCAFACLEPEAEAHNCABNGBGIIJCFIPNBIAKPHAPAHMJNJJHFOANCOIDICINMDEACKKBHBIELGIHANFDBBDJPBBDOHGCOPPIPMNOGGMDGDPCCKHDBGKIIEICDNEDLIHHDCOEDDACEKHOPNFFGKFLFFGLNCMHEELAMIPDCPGHMIEINMHKCIOCFLGLANOOBLNILNEMCBFGPIKCOJJJIDMHBLIKLLKAMPCHPCNACAEOKNE.png"
            }
        ]
        
        # Generate more mock data
        jobs = ["히어로", "팔라딘", "다크나이트", "보우마스터", "신궁", "패스파인더", 
                "나이트로드", "섀도어", "듀얼블레이드", "비숍", "아크메이지(불,독)", "아크메이지(썬,콜)",
                "캐논슈터", "캡틴", "바이퍼", "미하일", "소울마스터", "플레임위자드", "윈드브레이커",
                "나이트워커", "스트라이커", "데몬슬레이어", "데몬어벤져", "제논", "블래스터",
                "배틀메이지", "와일드헌터", "메카닉", "아란", "에반", "메르세데스", "팬텀", "루미너스",
                "은월", "카이저", "엔젤릭버스터", "초월자", "카데나", "일리움", "아크", "호영", "아델",
                "카인", "라라", "칼리", "렌"]
        
        guilds = ["Cross", "Frozen", "달치즈", "금별", "송이", "반달", "생글", None]
        
        for i in range(len(mock_characters), min(limit, 100)):
            mock_characters.append({
                "rank": i + 1,
                "name": f"Player{i+1}",
                "level": 275 + (i % 26),
                "job": jobs[i % len(jobs)],
                "guild": guilds[i % len(guilds)],
                "popularity": max(100, 100000 - i * 1000)
            })
            
        # Convert to Character objects
        characters = []
        for data in mock_characters[:limit]:
            char = Character(
                rank=data["rank"],
                name=data["name"],
                level=data["level"],
                job=data["job"],
                guild=data.get("guild"),
                popularity=data.get("popularity", 0),
                avatar_url=data.get("avatar_url")
            )
            
            # Add mock equipment for demonstration
            if data["rank"] <= 10:
                char.equipment = self._generate_mock_equipment(char)
                
            characters.append(char)
            
        return characters
        
    def _generate_mock_equipment(self, character: Character) -> Dict[str, Item]:
        """Generate mock equipment for a character"""
        equipment = {}
        
        # Mock item data
        item_types = {
            "weapon": ("Arcane Umbra Weapon", "weapon_arcane.png"),
            "hat": ("Arcane Umbra Hat", "hat_arcane.png"),
            "top": ("Arcane Umbra Suit", "top_arcane.png"),
            "shoes": ("Arcane Umbra Shoes", "shoes_arcane.png"),
            "gloves": ("Arcane Umbra Gloves", "gloves_arcane.png"),
            "cape": ("Tyrant Cape", "cape_tyrant.png"),
            "ring1": ("Superior Gollux Ring", "ring_gollux.png"),
            "ring2": ("Meister Ring", "ring_meister.png"),
            "ring3": ("Reinforced Gollux Ring", "ring_gollux2.png"),
            "ring4": ("Kanna's Treasure", "ring_kanna.png")
        }
        
        for slot, (name, image) in item_types.items():
            equipment[slot] = Item(
                name=name,
                slot=slot,
                level=200,
                image_url=None  # In real implementation, would have actual URLs
            )
            
        return equipment
        
    def get_character_details(self, character_name: str) -> Optional[Character]:
        """Get detailed information about a specific character"""
        # In real implementation, would make API call
        # For now, return None
        return None
        
    def search_characters(self, query: str) -> List[Character]:
        """Search for characters by name"""
        # In real implementation, would make API call
        # For now, return empty list
        return [] 