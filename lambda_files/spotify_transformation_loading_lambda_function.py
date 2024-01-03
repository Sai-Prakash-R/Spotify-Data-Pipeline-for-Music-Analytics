import json
import boto3
from datetime import datetime
from io import StringIO
import pandas as pd



def album(data):
    album_list = []
    for row in data['items']:
        album_id = row['track']['album']['id']
        album_name = row['track']['album']['name']
        release_date = row['track']['album']['release_date']
        external_urls = row['track']['album']['external_urls']['spotify']
        
        album_elements = {"album_id":album_id,
                          "album_name":album_name,
                          "release_date": release_date,
                          "external_urls":external_urls}
        
        album_list.append(album_elements)
    
    return album_list 
    
def artist(data):
    artist_list=[]
    for row in data['items']:
        for key, value in row.items():
            if key == "track":
                for artist in value['artists']:
                    artist_data = {'artist_id':artist['id'],
                                    'artist_name':artist['name'],
                                    'artist_type':artist['type']}
                    artist_list.append(artist_data)
    
    return artist_list

def songs(data):
    songs_list=[]
    for row in data['items']:
        song_id = row['track']['id']
        song_duration= row['track']['duration_ms']
        song_name=row['track']['name']
        song_popularity=row['track']['popularity']
        song_added_at = row['added_at']
        
        song_elements={'song_id':song_id,'song_duration':song_duration,'song_name':song_name,'song_popularity':song_popularity,'song_added_at':song_added_at}
        songs_list.append(song_elements)
    
    return songs_list

def lambda_handler(event, context):
    
    s3 = boto3.client('s3')
    Bucket = "s3-bucket-etl-spotify"
    Key = "raw_data_spotify/to_processed/"
    
    spotify_data = []
    spotify_keys = []
    for file in s3.list_objects(Bucket = Bucket, Prefix=Key)['Contents']:
        file_key = file['Key']
        if file_key.split(".")[-1] == "json":
            response = s3.get_object(Bucket = Bucket, Key = file_key)
            content = response['Body']
            jsonObj = json.loads(content.read())
            spotify_data.append(jsonObj)
            spotify_keys.append(file_key)
    
    for data in spotify_data:
        album_list = album(data)
        artist_list = artist(data)
        songs_list = songs(data)
        
        #Album DataFrame 
        album_df = pd.DataFrame.from_dict(album_list)
        album_df = album_df.drop_duplicates(subset=['album_id'])
        
        #Artist Dataframe
        artist_df = pd.DataFrame.from_dict(artist_list)
        artist_df = artist_df.drop_duplicates(subset=['artist_id'])
        
        #Songs DataFrame
        songs_df = pd.DataFrame.from_dict(songs_list)
        songs_df = songs_df.drop_duplicates(subset=['song_id'])
        
        album_df['release_date'] = pd.to_datetime(album_df['release_date'], format='mixed')
        songs_df['song_added_at'] = pd.to_datetime(songs_df['song_added_at'], format='mixed')
        
        song_key = "transformed_data/songs_data/song_transformed_" + str(datetime.now()) + ".csv"
        song_buffer = StringIO()
        songs_df.to_csv(song_buffer, index=False)
        song_content = song_buffer.getvalue()
        s3.put_object(Bucket = Bucket, Key = song_key,  Body = song_content)
        
        album_key = "transformed_data/album_data/album_transformed_" + str(datetime.now()) + ".csv"
        album_buffer = StringIO()
        album_df.to_csv(album_buffer, index=False)
        album_content = album_buffer.getvalue()
        s3.put_object(Bucket = Bucket, Key = album_key,  Body = album_content)
        
        artist_key = "transformed_data/artist_data/artist_transformed_" + str(datetime.now()) + ".csv"
        artist_buffer = StringIO()
        artist_df.to_csv(artist_buffer, index=False)
        artist_content = artist_buffer.getvalue()
        s3.put_object(Bucket = Bucket, Key = artist_key,  Body = artist_content)

    s3_resource = boto3.resource('s3')
    for key in spotify_keys:
        copy_source={
            'Bucket' : Bucket,
            'Key' : key
        }
        s3_resource.meta.client.copy(copy_source,Bucket,'raw_data_spotify/processed/' + key.split("/")[-1])
        s3_resource.Object(Bucket,key).delete()