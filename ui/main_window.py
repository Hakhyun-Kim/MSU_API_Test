"""
Main window UI for Maple Story Universe API Test
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTableWidget, QTableWidgetItem, QLabel, QPushButton,
    QLineEdit, QMessageBox, QProgressBar, QHeaderView,
    QDialog, QDialogButtonBox, QTextEdit, QSplitter, QGroupBox
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap
from api.api_client import MSUApiClient
from ui.character_widget import CharacterWidget
import os
import webbrowser


class ApiKeyDialog(QDialog):
    """Dialog to input API key"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("MapleStory API Key Required")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout()
        
        # Instructions
        instructions = QTextEdit()
        instructions.setReadOnly(True)
        instructions.setMaximumHeight(200)
        instructions.setHtml("""
        <h3>MapleStory Universe (MSU) API Key Required</h3>
        <p>To fetch real MapleStory character data, you need an API key from MSU.</p>
        <ol>
            <li>Visit https://msu.io/builder/docs</li>
            <li>Sign up or login to your MSU account</li>
            <li>Generate an API key from your dashboard</li>
            <li>Copy your API key and paste it below</li>
        </ol>
        <p><b>Note:</b> Your API key will be saved in config.py for future use.</p>
        """)
        layout.addWidget(instructions)
        
        # API key input
        self.api_key_label = QLabel("API Key:")
        layout.addWidget(self.api_key_label)
        
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Paste your API key here...")
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.api_key_input)
        
        # Open website button
        open_website_btn = QPushButton("Open MSU API Documentation")
        open_website_btn.clicked.connect(lambda: webbrowser.open("https://msu.io/builder/docs"))
        layout.addWidget(open_website_btn)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
    
    def get_api_key(self):
        """Get the entered API key"""
        return self.api_key_input.text().strip()


class DataLoader(QThread):
    """Thread for loading data from API"""
    data_loaded = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    progress_updated = pyqtSignal(int, str)
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        
    def run(self):
        """Run data loading in background"""
        try:
            self.progress_updated.emit(10, "Connecting to MapleStory API...")
            characters = self.api_client.get_top_characters(limit=100)
            self.progress_updated.emit(100, "Data loaded successfully!")
            self.data_loaded.emit(characters)
        except Exception as e:
            self.error_occurred.emit(str(e))


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.api_client = None
        self.characters = []
        self.init_api_client()
        self.init_ui()
        
    def init_api_client(self):
        """Initialize API client with API key"""
        # Try to load API key from config
        api_key = None
        
        # Check environment variable first
        api_key = os.getenv('MSU_API_KEY')
        
        # Try to load from config.py
        if not api_key:
            try:
                import config
                api_key = getattr(config, 'MSU_API_KEY', None)
                base_url = getattr(config, 'MSU_BASE_URL', None)
            except ImportError:
                base_url = None
        
        # If no API key, show dialog
        if not api_key or api_key == "your_msu_api_key_here":
            dialog = ApiKeyDialog(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                api_key = dialog.get_api_key()
                if api_key:
                    # Save to config.py
                    self.save_api_key(api_key)
                else:
                    QMessageBox.warning(self, "No API Key", 
                                      "No API key provided. The application will exit.")
                    exit(0)
            else:
                QMessageBox.information(self, "No API Key", 
                                      "API key is required. The application will exit.")
                exit(0)
        
        try:
            self.api_client = MSUApiClient(api_key=api_key, base_url=base_url)
        except ValueError as e:
            QMessageBox.critical(self, "API Error", str(e))
            exit(1)
    
    def save_api_key(self, api_key):
        """Save API key to config.py"""
        try:
            with open('config.py', 'w', encoding='utf-8') as f:
                f.write(f'# MapleStory Universe (MSU) API Configuration\n')
                f.write(f'# DO NOT SHARE THIS FILE - IT CONTAINS YOUR API KEY\n\n')
                f.write(f'MSU_API_KEY = "{api_key}"\n')
                f.write(f'MSU_BASE_URL = "https://api.msu.io"  # Default MSU API base URL\n')
            
            # Add config.py to .gitignore if not already there
            gitignore_path = '.gitignore'
            if os.path.exists(gitignore_path):
                with open(gitignore_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if 'config.py' not in content:
                    with open(gitignore_path, 'a', encoding='utf-8') as f:
                        f.write('\n# API configuration\nconfig.py\n')
        except Exception as e:
            QMessageBox.warning(self, "Save Error", 
                              f"Could not save API key to config.py: {str(e)}")
        
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
        
        # Set column resize modes for better display
        header = self.character_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Rank
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)           # Name - stretches
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Level
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)           # Job - stretches
        
        # Set minimum column widths
        self.character_table.setColumnWidth(0, 50)   # Rank
        self.character_table.setColumnWidth(1, 150)  # Name - minimum width
        self.character_table.setColumnWidth(2, 60)   # Level
        self.character_table.setColumnWidth(3, 120)  # Job
        
        # Disable text eliding and word wrap
        self.character_table.setWordWrap(False)
        self.character_table.setTextElideMode(Qt.TextElideMode.ElideNone)
        
        self.character_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.character_table.itemSelectionChanged.connect(self.on_character_selected)
        
        left_layout.addWidget(self.character_table)
        left_panel.setLayout(left_layout)
        
        # Right panel - Character details
        self.character_widget = CharacterWidget()
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(self.character_widget)
        splitter.setSizes([500, 700])  # Give more space to left panel
        
        # Set minimum width for left panel to prevent text cutoff
        left_panel.setMinimumWidth(400)
        
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
        self.api_worker = DataLoader(self.api_client)
        self.api_worker.data_loaded.connect(self.on_data_loaded)
        self.api_worker.error_occurred.connect(self.on_error)
        self.api_worker.progress_updated.connect(self.on_progress_update)
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
    
    def on_progress_update(self, progress, message):
        """Handle progress updates"""
        self.status_label.setText(message)
        
    def update_character_table(self, characters):
        """Update the character table with data"""
        self.character_table.setRowCount(len(characters))
        
        for i, char in enumerate(characters):
            # Rank column
            rank_item = QTableWidgetItem(str(char.rank))
            self.character_table.setItem(i, 0, rank_item)
            
            # Name column - with tooltip for full name
            name_item = QTableWidgetItem(char.name)
            name_item.setToolTip(char.name)  # Show full name on hover
            self.character_table.setItem(i, 1, name_item)
            
            # Level column
            level_item = QTableWidgetItem(str(char.level))
            self.character_table.setItem(i, 2, level_item)
            
            # Job column
            job_item = QTableWidgetItem(char.job)
            job_item.setToolTip(char.job)  # Show full job name on hover
            self.character_table.setItem(i, 3, job_item)
            
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