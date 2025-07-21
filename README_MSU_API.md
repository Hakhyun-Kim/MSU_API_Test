# MapleStory Universe (MSU) API Integration

This application now uses the MapleStory Universe (MSU) API from https://msu.io/builder/docs to fetch real MapleStory character data.

## Setup Instructions

### 1. Get MSU API Key

1. Visit [https://msu.io/builder/docs](https://msu.io/builder/docs)
2. Sign up or login to your MSU account
3. Generate an API key from your dashboard
4. Copy your API key

### 2. Configure the Application

#### Option A: Using config.py (Recommended)
1. Copy `config.example.py` to `config.py`
2. Replace `your_msu_api_key_here` with your actual MSU API key
3. Optionally modify the `MSU_BASE_URL` if needed

#### Option B: Using Environment Variable
Set the environment variable:
```bash
# Windows
set MSU_API_KEY=your_actual_api_key_here

# macOS/Linux
export MSU_API_KEY=your_actual_api_key_here
```

### 3. Run the Application

```bash
python main.py
```

The application will:
- Prompt for API key if not configured
- Fetch real character data from MSU API
- Display top 100 characters with rankings
- Show character details and equipment for top 10 characters

## API Features

- **Character Rankings**: Get top 100 characters by overall ranking
- **Character Details**: View detailed character information including equipment
- **World Support**: Filter by specific MapleStory worlds
- **Search**: Search for characters by name
- **Equipment Display**: Show character equipment with item details

## API Endpoints Used

- `GET /v1/characters/rankings` - Get character rankings
- `GET /v1/characters/{name}` - Get character details
- `GET /v1/characters/search` - Search characters
- `GET /v1/worlds` - Get available worlds

## Error Handling

- Falls back to mock data if API is unavailable
- Shows helpful error messages for configuration issues
- Graceful handling of network errors

## Security Notes

- API keys are saved locally in `config.py`
- `config.py` is automatically added to `.gitignore`
- Never share your API key publicly

## Troubleshooting

### "API key is required" error
- Make sure you've set up your API key in `config.py` or environment variable
- Check that the API key is valid and not expired

### "MSU API Error" messages
- Verify your internet connection
- Check if the MSU API service is available
- Ensure your API key has the necessary permissions

### Mock data showing instead of real data
- Check your API key configuration
- Verify network connectivity
- Look for error messages in the console output

## Support

For MSU API support, visit:
- [MSU API Documentation](https://msu.io/builder/docs)
- [MSU Community](https://msu.io/community)

For application issues, check the console output for detailed error messages. 