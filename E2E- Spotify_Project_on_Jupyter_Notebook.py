#!/usr/bin/env python
# coding: utf-8

# In[2]:


pip install spotipy


# In[3]:


import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# In[4]:


client_credentials_manager = SpotifyClientCredentials(client_id="7161d37d45534eb6892f0a86bdadacc7",
                                                      client_secret="862af086e1904480beaaa0cefdcd905a")


# In[5]:


sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


# In[6]:


playlist_hindi = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF"


# In[7]:


pl_uri = playlist_hindi.split("/")[-1]


# In[8]:


data = sp.playlist_tracks(playlist_hindi)


# In[9]:


data 


# In[10]:


data['items'][0]['track']['album']['id']


# In[11]:


data['items'][0]['track']['album']['total_tracks']


# In[12]:


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


# In[13]:


album_list


# In[14]:


data['items'][13]['track']['artists']


# In[15]:


artist_list=[]
for row in data['items']:
    for key, value in row.items():
        if key == "track":
            for artist in value['artists']:
                artist_data = {'artist_id':artist['id'],
                                'artist_name':artist['name'],
                                'artist_type':artist['type']}
                artist_list.append(artist_data)


# In[16]:


artist_list


# In[17]:


data['items'][0]['track']['name']


# In[18]:


songs_list=[]
for row in data['items']:
    song_id = row['track']['id']
    song_duration= row['track']['duration_ms']
    song_name=row['track']['name']
    song_popularity=row['track']['popularity']
    song_added_at = row['added_at']
    
    song_elements={'song_id':song_id,'song_duration':song_duration,'song_name':song_name,'song_popularity':song_popularity,'song_added_at':song_added_at}
    songs_list.append(song_elements)


# In[19]:


songs_list


# In[20]:


import pandas as pd
album_df = pd.DataFrame.from_dict(album_list)
album_df.head().info()


# In[21]:


album_df = album_df.drop_duplicates(subset=['album_id'])


# In[22]:


artist_df = pd.DataFrame(artist_list)
artist_df.head()


# In[23]:


artist_df = artist_df.drop_duplicates(subset=['artist_id'])


# In[24]:


artist_df.info()


# In[25]:


songs_df = pd.DataFrame(songs_list)
songs_df.head()


# In[26]:


songs_df = songs_df.drop_duplicates(subset=['song_id'])


# In[27]:


songs_df.info()


# In[28]:


album_df['release_date'] = pd.to_datetime(album_df['release_date'])


# In[29]:


album_df.head()


# In[30]:


songs_df['song_added_at'] = pd.to_datetime(songs_df['song_added_at'])


# In[31]:


songs_df.info()


# In[32]:


result = pd.concat([album_df,songs_df],axis=1)
result


# In[33]:


album_df.head()


# In[ ]:




