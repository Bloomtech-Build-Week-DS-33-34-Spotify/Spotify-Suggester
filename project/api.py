import requests
from os import getenv

# Generate an access token
# authetication URL
AUTH_URL = 'https://accounts.spotify.com/api/token'
# POST
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': getenv('SPOTIFY_CLIENT_ID'),
    'client_secret': getenv('SPOTIFY_CLIENT_SECRET'),
})
# convert the response to JSON
auth_response_data = auth_response.json()
# save the access token
access_token = auth_response_data['access_token']

# used for authenticating all API calls
headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}


def get_track_features(user_text):
    '''
    Return track id and audio features of song in user text string
    '''
    user_text = user_text.strip()
    user_track, user_artist = user_text.split(" by ")
    user_track = user_track.replace(" ", "%")
    user_artist = user_artist.replace(" ", "%")

    # GET request to get the track id given song and artist
    track_response = requests.get(
        f"https://api.spotify.com/v1/search?query=track:{user_track}+artist:{user_artist}&type=track&limit=1", headers=headers).json()

    user_track_id = track_response['tracks']['items'][0]['id']
    user_track_name = track_response['tracks']['items'][0]['name']
    user_track_artist = track_response['tracks']['items'][0]['album']['artists'][0]['name']

    # GET request to audio-features endpoint
    features_response = requests.get(
        f'http://api.spotify.com/v1/audio-features/{user_track_id}', headers=headers).json()

    audio_features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                      'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature']
    user_track_features = [features_response[feature]
                           for feature in audio_features]
    return (user_track_name, user_track_artist, user_track_id, user_track_features)
