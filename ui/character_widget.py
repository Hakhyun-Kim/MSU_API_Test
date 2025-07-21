"""
Character widget for displaying character details and items
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QGridLayout, QGroupBox, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from urllib.request import urlopen
from io import BytesIO
from PIL import Image
import requests


class ItemWidget(QFrame):
    """Widget to display a single item"""
    
    def __init__(self, item=None):
        super().__init__()
        self.setFrameStyle(QFrame.Shape.Box)
        self.setMaximumSize(100, 120)
        self.setMinimumSize(100, 120)
        
        layout = QVBoxLayout()
        layout.setSpacing(2)
        
        # Item image
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(64, 64)
        self.image_label.setMaximumSize(64, 64)
        self.image_label.setStyleSheet("border: 1px solid #ccc; background-color: #f0f0f0;")
        
        # Item name
        self.name_label = QLabel("Empty")
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setWordWrap(True)
        self.name_label.setMaximumHeight(40)
        font = self.name_label.font()
        font.setPointSize(8)
        self.name_label.setFont(font)
        
        layout.addWidget(self.image_label)
        layout.addWidget(self.name_label)
        self.setLayout(layout)
        
        if item:
            self.set_item(item)
            
    def set_item(self, item):
        """Set the item to display"""
        self.name_label.setText(item.name)
        
        # Load item image if available
        if hasattr(item, 'image_url') and item.image_url:
            try:
                response = requests.get(item.image_url, timeout=5)
                if response.status_code == 200:
                    pixmap = QPixmap()
                    pixmap.loadFromData(response.content)
                    scaled_pixmap = pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, 
                                                 Qt.TransformationMode.SmoothTransformation)
                    self.image_label.setPixmap(scaled_pixmap)
            except:
                # If image loading fails, show placeholder
                self.image_label.setText("No Image")


class CharacterWidget(QWidget):
    """Widget to display character information and equipment"""
    
    def __init__(self):
        super().__init__()
        self.character = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        main_layout = QVBoxLayout()
        
        # Character info section
        info_group = QGroupBox("Character Information")
        info_layout = QVBoxLayout()
        
        # Character avatar
        self.avatar_label = QLabel()
        self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.avatar_label.setMinimumSize(200, 200)
        self.avatar_label.setMaximumSize(200, 200)
        self.avatar_label.setStyleSheet("border: 2px solid #ccc; background-color: #f0f0f0;")
        
        # Character details
        self.name_label = QLabel("Select a character")
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = self.name_label.font()
        font.setPointSize(16)
        font.setBold(True)
        self.name_label.setFont(font)
        
        self.level_label = QLabel("Level: -")
        self.level_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.job_label = QLabel("Job: -")
        self.job_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.guild_label = QLabel("Guild: -")
        self.guild_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.popularity_label = QLabel("Popularity: -")
        self.popularity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        info_layout.addWidget(self.avatar_label)
        info_layout.addWidget(self.name_label)
        info_layout.addWidget(self.level_label)
        info_layout.addWidget(self.job_label)
        info_layout.addWidget(self.guild_label)
        info_layout.addWidget(self.popularity_label)
        info_layout.addStretch()
        
        info_group.setLayout(info_layout)
        main_layout.addWidget(info_group)
        
        # Equipment section
        equipment_group = QGroupBox("Equipment")
        equipment_scroll = QScrollArea()
        equipment_scroll.setWidgetResizable(True)
        
        self.equipment_widget = QWidget()
        self.equipment_layout = QGridLayout()
        self.equipment_layout.setSpacing(10)
        self.equipment_widget.setLayout(self.equipment_layout)
        
        equipment_scroll.setWidget(self.equipment_widget)
        equipment_layout = QVBoxLayout()
        equipment_layout.addWidget(equipment_scroll)
        equipment_group.setLayout(equipment_layout)
        
        main_layout.addWidget(equipment_group)
        self.setLayout(main_layout)
        
    def set_character(self, character):
        """Set the character to display"""
        self.character = character
        
        # Update character info
        self.name_label.setText(character.name)
        self.level_label.setText(f"Level: {character.level}")
        self.job_label.setText(f"Job: {character.job}")
        self.guild_label.setText(f"Guild: {character.guild if character.guild else 'None'}")
        self.popularity_label.setText(f"Popularity: {character.popularity:,}")
        
        # Load character avatar if available
        if hasattr(character, 'avatar_url') and character.avatar_url:
            try:
                response = requests.get(character.avatar_url, timeout=5)
                if response.status_code == 200:
                    pixmap = QPixmap()
                    pixmap.loadFromData(response.content)
                    scaled_pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio,
                                                 Qt.TransformationMode.SmoothTransformation)
                    self.avatar_label.setPixmap(scaled_pixmap)
            except:
                self.avatar_label.setText("No Avatar")
        else:
            self.avatar_label.setText("No Avatar")
            
        # Clear and update equipment
        self.clear_equipment()
        if hasattr(character, 'equipment') and character.equipment:
            self.display_equipment(character.equipment)
            
    def clear_equipment(self):
        """Clear the equipment display"""
        while self.equipment_layout.count():
            child = self.equipment_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
    def display_equipment(self, equipment):
        """Display character equipment"""
        # Equipment slots mapping
        slots = [
            ("Hat", 0, 0), ("Face", 0, 1), ("Eye", 0, 2),
            ("Overall", 1, 0), ("Top", 1, 1), ("Bottom", 1, 2),
            ("Shoes", 2, 0), ("Gloves", 2, 1), ("Cape", 2, 2),
            ("Weapon", 3, 0), ("Shield", 3, 1), ("Earring", 3, 2),
            ("Ring1", 4, 0), ("Ring2", 4, 1), ("Ring3", 4, 2), ("Ring4", 4, 3),
            ("Pendant", 5, 0), ("Belt", 5, 1), ("Medal", 5, 2)
        ]
        
        for slot_name, row, col in slots:
            item = equipment.get(slot_name.lower())
            if item:
                item_widget = ItemWidget(item)
            else:
                item_widget = ItemWidget()
            self.equipment_layout.addWidget(item_widget, row, col) 