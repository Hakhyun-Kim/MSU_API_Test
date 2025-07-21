"""
Main window for MSU API Test application
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QLabel, QGroupBox, QScrollArea, QGridLayout,
    QHeaderView, QSplitter, QTextEdit, QLineEdit
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap
import json
from api.api_client import MSUApiClient
from models.character import Character
from ui.character_widget import CharacterWidget


class ApiWorker(QThread):
    """Worker thread for API calls"""
    data_ready = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        
    def run(self):
        try:
            # For now, using mock data since we don't have real API access
            characters = self.api_client.get_top_characters(100)
            self.data_ready.emit(characters)
        except Exception as e:
            self.error_occurred.emit(str(e))


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.api_client = MSUApiClient()
        self.characters = []
        self.current_character = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Maple Story Universe API Test")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Create toolbar
        toolbar_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("Refresh Top 100")
        self.refresh_btn.clicked.connect(self.load_characters)
        toolbar_layout.addWidget(self.refresh_btn)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search character...")
        self.search_input.textChanged.connect(self.filter_characters)
        toolbar_layout.addWidget(self.search_input)
        
        toolbar_layout.addStretch()
        main_layout.addLayout(toolbar_layout)
        
        # Create splitter for main content
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Character list
        left_panel = QGroupBox("Top 100 Characters")
        left_layout = QVBoxLayout()
        
        self.character_table = QTableWidget()
        self.character_table.setColumnCount(4)
        self.character_table.setHorizontalHeaderLabels(["Rank", "Name", "Level", "Job"])
        self.character_table.horizontalHeader().setStretchLastSection(True)
        self.character_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.character_table.itemSelectionChanged.connect(self.on_character_selected)
        
        left_layout.addWidget(self.character_table)
        left_panel.setLayout(left_layout)
        
        # Right panel - Character details
        self.character_widget = CharacterWidget()
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(self.character_widget)
        splitter.setSizes([400, 800])
        
        main_layout.addWidget(splitter)
        
        # Status bar
        self.status_label = QLabel("Ready")
        main_layout.addWidget(self.status_label)
        
        # Load initial data
        self.load_characters()
        
    def load_characters(self):
        """Load character data from API"""
        self.refresh_btn.setEnabled(False)
        self.status_label.setText("Loading characters...")
        
        # Create and start worker thread
        self.api_worker = ApiWorker(self.api_client)
        self.api_worker.data_ready.connect(self.on_data_loaded)
        self.api_worker.error_occurred.connect(self.on_error)
        self.api_worker.start()
        
    def on_data_loaded(self, characters):
        """Handle loaded character data"""
        self.characters = characters
        self.update_character_table(characters)
        self.refresh_btn.setEnabled(True)
        self.status_label.setText(f"Loaded {len(characters)} characters")
        
    def on_error(self, error_msg):
        """Handle API errors"""
        self.refresh_btn.setEnabled(True)
        self.status_label.setText(f"Error: {error_msg}")
        
    def update_character_table(self, characters):
        """Update the character table with data"""
        self.character_table.setRowCount(len(characters))
        
        for i, char in enumerate(characters):
            self.character_table.setItem(i, 0, QTableWidgetItem(str(char.rank)))
            self.character_table.setItem(i, 1, QTableWidgetItem(char.name))
            self.character_table.setItem(i, 2, QTableWidgetItem(str(char.level)))
            self.character_table.setItem(i, 3, QTableWidgetItem(char.job))
            
    def on_character_selected(self):
        """Handle character selection"""
        selected_rows = self.character_table.selectedIndexes()
        if selected_rows:
            row = selected_rows[0].row()
            if row < len(self.characters):
                self.current_character = self.characters[row]
                self.character_widget.set_character(self.current_character)
                
    def filter_characters(self, text):
        """Filter characters based on search text"""
        if not text:
            self.update_character_table(self.characters)
            return
            
        filtered = [char for char in self.characters 
                   if text.lower() in char.name.lower() 
                   or text.lower() in char.job.lower()]
        self.update_character_table(filtered) 