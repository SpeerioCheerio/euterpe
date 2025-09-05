import spotipy
import matplotlib
matplotlib.use('Agg')  # Ensures we can render on a server without X11
import matplotlib.pyplot as plt
from io import BytesIO
import base64


def get_top_albums(sp, time_range='medium_term'):
    """
    Return a list of top albums and associated track counts for the specified time range.
    Example return:
    [
        {"album_name": "Album A", "track_count": 3, "album_image": "https://...", "artists": "Artist1"},
        {"album_name": "Album B", "track_count": 2, "album_image": "https://...", "artists": "Artist2"},
        ...
    ]
    """
    results = sp.current_user_top_tracks(limit=50, time_range=time_range)
    albums = {}
    album_details = {}
    
    for track in results['items']:
        album_name = track['album']['name']
        albums[album_name] = albums.get(album_name, 0) + 1
        
        # Store album details (image and artists) - only store once per album
        if album_name not in album_details:
            # Get album image (prefer 300px, fallback to largest available)
            album_image = None
            if track['album']['images']:
                # Try to find 300px image first
                for img in track['album']['images']:
                    if img['width'] == 300:
                        album_image = img['url']
                        break
                # If no 300px image, use the first (largest) available
                if not album_image:
                    album_image = track['album']['images'][0]['url']
            
            # Get album artists
            artists_names = ', '.join(artist['name'] for artist in track['album']['artists'])
            
            album_details[album_name] = {
                'image': album_image,
                'artists': artists_names
            }

    # Sort by track count
    sorted_albums = sorted(albums.items(), key=lambda x: x[1], reverse=True)

    # Return top 10 with details
    data = []
    for album_name, count in sorted_albums[:10]:
        details = album_details[album_name]
        data.append({
            "album_name": album_name,
            "track_count": count,
            "album_image": details['image'],
            "artists": details['artists']
        })
    
    return data

def get_top_songs(sp, time_range='medium_term'):
    """
    Return a list of top songs for the specified time range.
    Example return:
    [
        {"song_name": "Song A", "artists": "Artist1, Artist2", "album_image": "https://..."},
        {"song_name": "Song B", "artists": "Artist1", "album_image": "https://..."},
        ...
    ]
    """
    results = sp.current_user_top_tracks(limit=50, time_range=time_range)
    data = []
    for track in results['items']:
        artists_names = ', '.join(artist['name'] for artist in track['artists'])
        
        # Get album image (prefer 300px, fallback to largest available)
        album_image = None
        if track['album']['images']:
            # Try to find 300px image first
            for img in track['album']['images']:
                if img['width'] == 300:
                    album_image = img['url']
                    break
            # If no 300px image, use the first (largest) available
            if not album_image:
                album_image = track['album']['images'][0]['url']
        
        data.append({
            "song_name": track['name'],
            "artists": artists_names,
            "album_image": album_image,
            "popularity": track.get('popularity', 0),
            "duration_ms": track.get('duration_ms', 0)
        })
    return data

def get_hidden_gems(sp, time_range='medium_term'):
    """
    Return songs sorted by rarity (lowest popularity first).
    Shows the user's most unique and underground music taste.
    Example return:
    [
        {"song_name": "Obscure Track", "artists": "Underground Artist", "popularity": 5, "album_image": "https://...", "duration_ms": 240000},
        {"song_name": "Deep Cut", "artists": "Indie Band", "popularity": 12, "album_image": "https://...", "duration_ms": 180000},
        ...
    ]
    """
    results = sp.current_user_top_tracks(limit=50, time_range=time_range)
    data = []
    
    for track in results['items']:
        artists_names = ', '.join(artist['name'] for artist in track['artists'])
        
        # Get album image (prefer 300px, fallback to largest available)
        album_image = None
        if track['album']['images']:
            # Try to find 300px image first
            for img in track['album']['images']:
                if img['width'] == 300:
                    album_image = img['url']
                    break
            # If no 300px image, use the first (largest) available
            if not album_image:
                album_image = track['album']['images'][0]['url']
        
        data.append({
            "song_name": track['name'],
            "artists": artists_names,
            "album_image": album_image,
            "popularity": track.get('popularity', 0),
            "duration_ms": track.get('duration_ms', 0)
        })
    
    # Sort by popularity (ascending - rarest first)
    data.sort(key=lambda x: x['popularity'])
    
    return data

def get_top_artists(sp, time_range='medium_term'):
    """
    Return a list of top artists for the specified time range.
    Example return:
    [
        {"artist_name": "Artist A", "artist_image": "https://...", "genres": ["rock", "pop"]},
        {"artist_name": "Artist B", "artist_image": "https://...", "genres": ["jazz"]},
        ...
    ]
    """
    results = sp.current_user_top_artists(limit=50, time_range=time_range)
    data = []
    for artist in results['items']:
        # Get artist image (prefer 300px, fallback to largest available)
        artist_image = None
        if artist['images']:
            # Try to find 300px image first
            for img in artist['images']:
                if img['width'] == 300:
                    artist_image = img['url']
                    break
            # If no 300px image, use the first (largest) available
            if not artist_image:
                artist_image = artist['images'][0]['url']
        
        data.append({
            "artist_name": artist['name'],
            "artist_image": artist_image,
            "genres": artist.get('genres', [])
        })
    return data

def analyze_top_playlists(sp):
    """
    Return the top 10 playlists created by the user,
    sorted by the number of the user's top short-term songs contained.
    Example return:
    [
        {"playlist_name": "My Playlist 1", "top_songs_count": 10},
        {"playlist_name": "My Playlist 2", "top_songs_count": 8},
        ...
    ]
    """
    # Get the current user's profile to retrieve their user ID
    user_profile = sp.current_user()
    user_id = user_profile['id']

    # Fetch all playlists created by the user
    playlists = sp.current_user_playlists(limit=50)['items']
    user_playlists = [p for p in playlists if p['owner']['id'] == user_id]

    # Fetch the user's top tracks (short_term)
    top_tracks = sp.current_user_top_tracks(limit=50, time_range="short_term")['items']
    top_track_ids = set(track['id'] for track in top_tracks)

    playlist_data = []

    for playlist in user_playlists:
        playlist_id = playlist['id']
        playlist_name = playlist['name']

        tracks = sp.playlist_items(
            playlist_id,
            fields="items(track(id))",
            limit=100
        )['items']

        top_songs_count = 0
        for item in tracks:
            track = item['track']
            if track and track['id'] in top_track_ids:
                top_songs_count += 1

        playlist_data.append({
            "playlist_name": playlist_name,
            "top_songs_count": top_songs_count
        })

    # Sort and return top 10
    sorted_playlists = sorted(playlist_data, key=lambda x: x['top_songs_count'], reverse=True)[:10]
    return sorted_playlists

def get_artists_fallen_off(sp):
    """
    Identify artists that appear in the long term list, but not in medium or short term lists.
    Returns something like:
    [
        {"artist_name": "Artist X", "artist_image": "https://...", "genres": ["rock", "pop"]},
        {"artist_name": "Artist Y", "artist_image": "https://...", "genres": ["jazz"]},
        ...
    ]
    """
    long_term_artists = sp.current_user_top_artists(limit=50, time_range="long_term")['items']
    medium_term_artists = sp.current_user_top_artists(limit=50, time_range="medium_term")['items']
    short_term_artists = sp.current_user_top_artists(limit=50, time_range="short_term")['items']

    # Create artist details dictionary from long term artists
    long_term_details = {}
    for artist in long_term_artists:
        # Get artist image (prefer 300px, fallback to largest available)
        artist_image = None
        if artist['images']:
            # Try to find 300px image first
            for img in artist['images']:
                if img['width'] == 300:
                    artist_image = img['url']
                    break
            # If no 300px image, use the first (largest) available
            if not artist_image:
                artist_image = artist['images'][0]['url']
        
        long_term_details[artist['name']] = {
            'artist_image': artist_image,
            'genres': artist.get('genres', [])
        }

    long_term_set = set(a['name'] for a in long_term_artists)
    medium_term_set = set(a['name'] for a in medium_term_artists)
    short_term_set = set(a['name'] for a in short_term_artists)

    fallen_off_artists = long_term_set - medium_term_set - short_term_set

    return [{
        "artist_name": artist_name,
        "artist_image": long_term_details[artist_name]['artist_image'],
        "genres": long_term_details[artist_name]['genres']
    } for artist_name in sorted(fallen_off_artists)]

def get_artists_standing_test_of_time(sp):
    """
    Identify artists that appear in the short, medium, and long term lists.
    Returns something like:
    [
        {"artist_name": "Artist A", "artist_image": "https://...", "genres": ["rock", "pop"]},
        {"artist_name": "Artist B", "artist_image": "https://...", "genres": ["jazz"]},
        ...
    ]
    """
    long_term_artists = sp.current_user_top_artists(limit=50, time_range="long_term")['items']
    medium_term_artists = sp.current_user_top_artists(limit=50, time_range="medium_term")['items']
    short_term_artists = sp.current_user_top_artists(limit=50, time_range="short_term")['items']

    # Create artist details dictionary
    all_artists = {}
    for artist_list in [long_term_artists, medium_term_artists, short_term_artists]:
        for artist in artist_list:
            if artist['name'] not in all_artists:
                # Get artist image (prefer 300px, fallback to largest available)
                artist_image = None
                if artist['images']:
                    # Try to find 300px image first
                    for img in artist['images']:
                        if img['width'] == 300:
                            artist_image = img['url']
                            break
                    # If no 300px image, use the first (largest) available
                    if not artist_image:
                        artist_image = artist['images'][0]['url']
                
                all_artists[artist['name']] = {
                    'artist_image': artist_image,
                    'genres': artist.get('genres', [])
                }

    long_term_set = set(a['name'] for a in long_term_artists)
    medium_term_set = set(a['name'] for a in medium_term_artists)
    short_term_set = set(a['name'] for a in short_term_artists)

    consistent_artists = long_term_set & medium_term_set & short_term_set

    return [{
        "artist_name": artist_name,
        "artist_image": all_artists[artist_name]['artist_image'],
        "genres": all_artists[artist_name]['genres']
    } for artist_name in sorted(consistent_artists)]

def get_music_variety_by_season(sp, time_range='medium_term'):
    """
    Return seasonal genre data for frontend chart rendering.
    Returns raw data for much faster loading and better integration with the UI.
    """
    # Fetch top tracks
    results = sp.current_user_top_tracks(limit=50, time_range=time_range)
    if not results['items']:
        return {
            "error": f"No top tracks found for time_range='{time_range}'.",
            "seasonal_data": {}
        }

    # Define seasons
    seasons = {
        "Winter": (12, 1, 2),
        "Spring": (3, 4, 5),
        "Summer": (6, 7, 8),
        "Fall":   (9, 10, 11)
    }
    seasonal_genres = {s: [] for s in seasons}

    # Gather genres for each season
    for track in results['items']:
        release_date = track['album']['release_date']
        if len(release_date) >= 7:  # ensure it has YYYY-MM
            month = int(release_date[5:7])
            for season_name, months in seasons.items():
                if month in months:
                    # Get each artist's genres and extend the list
                    for artist in track['artists']:
                        try:
                            artist_info = sp.artist(artist['id'])
                            seasonal_genres[season_name].extend(artist_info['genres'])
                        except:
                            # Skip if artist info can't be fetched
                            pass
                    break

    # For each season, compute top 10 genres
    seasonal_data = {}
    total_genres = 0
    
    for season_name, genres_list in seasonal_genres.items():
        if genres_list:
            genre_counts = {}
            for g in genres_list:
                genre_counts[g] = genre_counts.get(g, 0) + 1
            # Sort descending by count, take top 10
            sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            # Convert to list of dicts
            seasonal_data[season_name] = [{"genre": k, "count": v} for k, v in sorted_genres]
            total_genres += sum(v for k, v in sorted_genres)
        else:
            seasonal_data[season_name] = []

    return {
        "error": None,
        "seasonal_data": seasonal_data,
        "total_genres": total_genres,
        "seasons_with_data": [season for season, data in seasonal_data.items() if data]
    }



def get_release_year_trends(sp, time_range='medium_term'):
    """
    Return release year distribution data for frontend chart rendering.
    Returns raw data for much faster loading and better integration with the UI.
    """
    results = sp.current_user_top_tracks(limit=50, time_range=time_range)
    years = []
    
    for track in results['items']:
        date_str = track['album']['release_date']
        if date_str[:4].isdigit():
            years.append(int(date_str[:4]))

    if not years:
        return {
            "error": "No release year data available.",
            "data": []
        }

    # Count tracks by year
    year_counts = {}
    for y in years:
        year_counts[y] = year_counts.get(y, 0) + 1

    # Convert to list of dicts for JSON, only include years with tracks
    data = [{"year": year, "count": count} for year, count in sorted(year_counts.items())]
    
    # Add metadata for better chart rendering
    min_year = min(years)
    max_year = max(years)
    peak_year_data = max(year_counts.items(), key=lambda x: x[1])
    
    return {
        "error": None,
        "data": data,
        "total_tracks": len(years),
        "year_range": {"min": min_year, "max": max_year},
        "peak_year": {"year": peak_year_data[0], "count": peak_year_data[1]}
    }
