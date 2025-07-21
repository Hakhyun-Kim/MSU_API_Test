# Maple Story Universe API Test Application

A desktop application for testing and exploring the Maple Story Universe (MSU) API, built with Python and PyQt6.

## 📸 Screenshots

### Main Window
![Main Window](screenshots/main_window.png)
*The main application window showing the top 100 characters list*

### Character Details
![Character Details](screenshots/character_details.png)
*Detailed view of a selected character with equipment slots*

### Search Function
![Search Function](screenshots/search_function.png)
*Search functionality to filter characters by name or job*

## ✨ Features

- 🎮 Fetch and display top 100 MapleStory characters
- 👤 View character details including level, job, guild, and popularity
- 🎨 Display character avatars from official Nexon servers
- 💎 Display character equipment with item images (when available)
- 🔍 Search and filter characters by name or job
- 🖥️ Cross-platform support (Windows and macOS)
- 🧵 Asynchronous data loading with threading

## 🔧 Requirements

- Python 3.8 or higher
- PyQt6
- See `requirements.txt` for full dependencies

## 📦 Installation

### Option 1: Download Pre-built Release (Recommended)

1. Go to the [Releases](https://github.com/yourusername/MSU_API_Test/releases) page
2. Download the latest version for your operating system:
   - **Windows**: `MSU_API_Test-Windows.exe` or `MSU_API_Test_Setup_1.0.0.exe` (installer)
   - **macOS**: `MSU_API_Test-macOS`
   - **Linux**: `MSU_API_Test-Linux`
3. Run the downloaded file

### Option 2: Build from Source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/MSU_API_Test.git
cd MSU_API_Test
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) Build standalone executable:
```bash
python build.py
```

## 🚀 Running the Application

```bash
python main.py
# or on Windows:
py main.py
```

## 📁 Project Structure

```
MSU_API_Test/
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── .gitignore          # Git ignore rules
├── api/                # API client modules
│   ├── __init__.py
│   └── api_client.py   # MSU API client implementation
├── models/             # Data models
│   ├── __init__.py
│   ├── character.py    # Character data model
│   └── item.py        # Item data model
├── ui/                 # User interface components
│   ├── __init__.py
│   ├── main_window.py  # Main application window
│   └── character_widget.py  # Character display widget
└── screenshots/        # Application screenshots
    ├── main_window.png
    ├── character_details.png
    └── search_function.png
```

## 📖 Usage

1. **Launch the application** - The top 100 characters will be loaded automatically
2. **Browse characters** - Scroll through the character list on the left
3. **View details** - Click on any character to see their information and equipment
4. **Search** - Use the search box to filter by character name or job class
5. **Refresh** - Click "Refresh Top 100" to reload the latest character data

## 🔌 API Integration

Currently, the application uses mock data that simulates the MapleStory Universe API response. To integrate with the real API:

1. Register at [MapleStory Network](https://maplestory.net/develop)
2. Create an app to obtain your API key
3. Update `api/api_client.py` with your credentials:
```python
client = MSUApiClient(
    base_url="https://api.maplestory.net",
    api_key="YOUR_API_KEY_HERE"
)
```

## 🛠️ Development

### Adding New Features

- **Character Stats**: Extend the `Character` model in `models/character.py`
- **UI Enhancements**: Modify `ui/character_widget.py` for display improvements
- **API Endpoints**: Add new methods in `api/api_client.py`

### Building for Distribution

To create a standalone executable:
```bash
pip install pyinstaller
pyinstaller --windowed --onefile main.py
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📦 Creating a Release

Releases are automatically built when you create a new tag:

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

This will trigger GitHub Actions to:
- Build executables for Windows, macOS, and Linux
- Create a GitHub release with the built files
- Upload the executables as release assets

## 📝 Known Limitations

- Currently uses mock data instead of live API
- Item images are placeholders
- Limited to top 100 characters
- Equipment potential and stats not displayed

## 🔮 Future Enhancements

- [ ] Real MSU API integration
- [ ] Character comparison features
- [ ] Export character data to CSV/JSON
- [ ] Dark mode theme
- [ ] Multi-language support
- [ ] Character build analyzer
- [ ] Guild rankings view

## 📄 License

This project is for educational and testing purposes only. MapleStory and all related content are property of Nexon Corporation.

## 🙏 Acknowledgments

- Nexon for MapleStory Universe
- PyQt6 for the GUI framework
- The MapleStory community

---

**Note**: This is an unofficial application and is not affiliated with or endorsed by Nexon Corporation. 