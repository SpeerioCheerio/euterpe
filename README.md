# Euterpe Dashboard

A beautiful, Spotify-inspired music analytics dashboard that provides deep insights into your listening habits and musical journey. Named after Euterpe, the Greek muse of music, this dashboard transforms your Spotify data into an elegant, interactive experience.

![Dashboard Preview](https://img.shields.io/badge/Status-Live-brightgreen) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Flask](https://img.shields.io/badge/Flask-2.0+-red) ![Spotify API](https://img.shields.io/badge/Spotify-Web%20API-1ed760)

## Features

### Music Library Analytics
- **Top Tracks**: Your most-played songs with popularity ratings and album artwork
- **Top Artists**: Favorite artists with genre information and profile photos
- **Top Albums**: Most-listened albums with cover art and artist details
- **Hidden Gems**: Discover your rarest tracks (lowest popularity scores)
- **Top Playlists**: Playlists containing the most of your top songs

### Advanced Analytics
- **Timeless Artists**: Artists that consistently appear across different time periods
- **Trending Down**: Artists with declining interest over time
- **Release Trends**: Visual analysis of your music by release year
- **Seasonal Variety**: Genre diversity across different seasons

### Beautiful UI
- **Spotify-Inspired Design**: Dark theme with authentic Spotify color palette
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile
- **Interactive Charts**: Native HTML/CSS/JS charts (no heavy dependencies)
- **Real Album Artwork**: High-quality images from Spotify's CDN
- **Smooth Animations**: Hover effects and transitions for premium feel

### Performance Optimized
- **Fast Loading**: Native charts instead of heavy Matplotlib
- **Efficient API Calls**: Parallel data fetching for quick load times
- **Smart Caching**: Optimized data retrieval patterns
- **Lightweight**: Minimal dependencies for fast deployment

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Spotify Developer Account
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/euterpe_dashboard.git
cd euterpe_dashboard
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Spotify API

#### Create Spotify App
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Click "Create App"
3. Fill in app details:
   - **App Name**: Euterpe Dashboard
   - **App Description**: Music analytics dashboard
   - **Redirect URI**: `http://localhost:5000`
4. Note down your **Client ID** and **Client Secret**

#### Set Up Environment Variables
Create a `.env` file in the root directory:
```env
CLIENT_ID=your_spotify_client_id_here
CLIENT_SECRET=your_spotify_client_secret_here
REDIRECT_URI=http://localhost:5000
SCOPE=user-top-read user-read-recently-played user-library-read playlist-read-private playlist-read-collaborative
```

### 5. Run the Application
```bash
python app.py
```

### 6. Access the Dashboard
Open your browser and navigate to: `http://localhost:5000`

## Project Structure

```
euterpe_dashboard/
├── app.py                 # Flask application and API routes
├── logic.py              # Spotify API integration and data processing
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not tracked)
├── .gitignore           # Git ignore rules
├── favicon.png          # Dashboard favicon
├── templates/
│   └── index.html       # Main dashboard template
└── static/
    └── js/
        └── script.js    # Frontend JavaScript functionality
```

## API Endpoints

### Music Data
- `GET /top_songs?time_range={short_term|medium_term|long_term}` - Top tracks
- `GET /top_artists?time_range={short_term|medium_term|long_term}` - Top artists
- `GET /top_albums?time_range={short_term|medium_term|long_term}` - Top albums
- `GET /hidden_gems?time_range={short_term|medium_term|long_term}` - Rarest tracks
- `GET /top_playlists` - Playlists with most top songs

### Analytics
- `GET /artists_standing_test_of_time` - Consistent favorite artists
- `GET /artists_falling_off` - Artists with declining interest
- `GET /release_year_trends?time_range={short_term|medium_term|long_term}` - Release year analysis
- `GET /music_variety_by_season?time_range={short_term|medium_term|long_term}` - Seasonal genre variety

### Static Files
- `GET /favicon.png` - Dashboard favicon
- `GET /static/js/script.js` - Frontend JavaScript

## Design System

### Color Palette
```css
--spotify-black: #000000
--spotify-dark-gray: #121212
--spotify-darker-gray: #181818
--spotify-light-gray: #282828
--spotify-white: #ffffff
--spotify-light-text: #b3b3b3
--spotify-green: #3b82f6        /* Custom blue accent */
--spotify-green-hover: #60a5fa  /* Hover state */
```

### Typography
- **Primary Font**: Circular (Spotify's font family)
- **Fallback**: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif
- **Weights**: 400 (regular), 500 (medium), 600 (semibold), 700 (bold)

### Components
- **Cards**: Rounded corners (12px), subtle shadows, hover animations
- **Lists**: Clean typography, proper spacing, image thumbnails
- **Charts**: Native HTML/CSS bars with smooth transitions
- **Navigation**: Sidebar with active states and smooth transitions

## Security & Privacy

### Data Handling
- **No Data Storage**: All data is fetched in real-time from Spotify
- **Local Processing**: Analytics computed client-side when possible
- **Secure Credentials**: API keys stored in environment variables
- **HTTPS Ready**: Configured for secure deployment

### Spotify Permissions
The app requests minimal necessary permissions:
- `user-top-read`: Access to your top tracks and artists
- `user-read-recently-played`: Recent listening history
- `user-library-read`: Your saved music library
- `playlist-read-private`: Access to your private playlists
- `playlist-read-collaborative`: Collaborative playlists

## Deployment

### Local Development
```bash
python app.py
```

### Production Deployment

#### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

#### Using Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

#### Environment Variables for Production
```env
FLASK_ENV=production
CLIENT_ID=your_production_client_id
CLIENT_SECRET=your_production_client_secret
REDIRECT_URI=https://yourdomain.com
```

## Development

### Adding New Features

#### 1. Backend (Python/Flask)
- Add new functions in `logic.py`
- Create corresponding routes in `app.py`
- Update imports as needed

#### 2. Frontend (JavaScript)
- Add new functions in `static/js/script.js`
- Update navigation in `templates/index.html`
- Add corresponding CSS styles

#### 3. Testing
```bash
# Run the application
python app.py

# Test API endpoints
curl http://localhost:5000/top_songs?time_range=medium_term
```

### Code Style
- **Python**: Follow PEP 8 guidelines
- **JavaScript**: Use modern ES6+ syntax
- **CSS**: Use CSS custom properties for theming
- **HTML**: Semantic markup with proper accessibility

## Data Insights

### What You Can Discover
- **Musical Evolution**: How your taste changes over time
- **Genre Diversity**: Seasonal patterns in your listening
- **Hidden Preferences**: Rare tracks that define your unique taste
- **Artist Loyalty**: Which artists stand the test of time
- **Discovery Patterns**: How you find new music

### Time Ranges
- **Short Term (4 weeks)**: Recent listening habits
- **Medium Term (6 months)**: Current musical preferences
- **Long Term (1 year)**: Overall musical identity

## Contributing

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/euterpe_dashboard.git

# Install development dependencies
pip install -r requirements.txt

# Run in development mode
export FLASK_ENV=development
python app.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Spotify**: For providing the comprehensive Web API
- **Spotipy**: Python library for Spotify Web API
- **Flask**: Lightweight web framework
- **Euterpe**: The Greek muse of music who inspired this project

## Support

### Common Issues

#### "Unauthorized User API key"
- Verify your Spotify app credentials in `.env`
- Check that redirect URI matches your Spotify app settings
- Ensure your Spotify app is not in development mode restrictions

#### "No data showing"
- Make sure you have sufficient listening history on Spotify
- Try different time ranges (short_term, medium_term, long_term)
- Check browser console for JavaScript errors

#### "Favicon not loading"
- Ensure `favicon.png` is in the root directory
- Check that the Flask route is properly configured
- Clear browser cache

### Getting Help
- **Issues**: Open a GitHub issue for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check this README and inline code comments

## Roadmap

### Planned Features
- [ ] **Export Data**: Download your analytics as CSV/JSON
- [ ] **Social Features**: Compare with friends (with permission)
- [ ] **Advanced Filters**: Filter by genre, year, popularity
- [ ] **Playlist Generation**: Create playlists based on insights
- [ ] **Mobile App**: Native mobile application
- [ ] **Real-time Updates**: Live listening activity
- [ ] **Custom Themes**: Multiple color schemes
- [ ] **Data Visualization**: More chart types and interactive graphs

### Version History
- **v1.0.0**: Initial release with core analytics
- **v1.1.0**: Added Hidden Gems and enhanced UI
- **v1.2.0**: Performance optimizations and native charts
- **v1.3.0**: Enhanced overview dashboard with previews

---

**Made with love and music by music lovers, for music lovers.**

*Discover the story of your musical journey with Euterpe Dashboard.*
