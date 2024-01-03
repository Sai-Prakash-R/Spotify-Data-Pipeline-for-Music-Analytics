import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import boto3
from datetime import datetime


def lambda_handler(event, context):
    
    client_id = os.environ.get('client_id')
    client_secret = os.environ.get('client_secret')
    
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    playlists = sp.user_playlists('spotify')
    
    playlist_top_50_global = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF"
    pl_uri = playlist_top_50_global.split("/")[-1]
    data = sp.playlist_tracks(playlist_top_50_global)
    
    print(data)
    filename="spotify_raw_" + str(datetime.now()) + ".json"
    
    client = boto3.client('s3')
    client.put_object(
        Bucket="s3-bucket-etl-spotify",
        Key="raw_data_spotify/to_processed/" + filename,
        Body=json.dumps(data)
        )