import ZournalScraper
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

# Remember to run console commands in consolecommands.txt

scope = 'playlist-modify-public'
username = 'dr.jekyll284'

token = SpotifyOAuth(scope=scope,username=username)
spotifyObject = spotipy.Spotify(auth_manager=token)

"""
#create the playlist
playlist_name = input("Playlist name: ")
playlist_description = input("Playlist description: ")

spotifyObject.user_playlist_create(user=username,name=playlist_name,public=True,description=playlist_description)

# Find songs
user_input = input("Enter song: ")
list_of_songs = []
while user_input != "quit":
    result = spotifyObject.search(q=user_input)
    #print(json.dumps(result,sort_keys=4,indent=4))
    list_of_songs.append(result['tracks']['items'][0]['uri'])
    user_input = input("Enter song: ")
prePlaylist = spotifyObject.user_playlists(user=username)
playlist = prePlaylist['items'][0]['id']        #playlist we just created

spotifyObject.user_playlist_add_tracks(user=username,playlist_id=playlist,tracks=list_of_songs) #add the songs
"""

"""
###########################################
# Year Playlist
# Debugged and working
year = "2020"
playlist_name = "songs of the day ({})".format(year)
playlist_description = "just a little (enormous) playlist of each song I've highlighted as a \"Song of the Day\" in my journal during {}🥰".format(year)
spotifyObject.user_playlist_create(user=username,name=playlist_name,public=True,description=playlist_description)

prePlaylist = spotifyObject.user_playlists(user=username)
playlist = prePlaylist['items'][0]['id'] 


for entry in ZournalScraper.zournal:
    if ZournalScraper.zournal[entry].year == year:
        songList = []
        for song in ZournalScraper.zournal[entry].sotd:
            try:
                title = song.title
                artist = song.artists[0]
                query = title + " " + artist
            except:
                query = song.songLine
            try:
                searchResults = spotifyObject.search(q=query)
                topResult = searchResults['tracks']['items'][0]['uri']
                songList.append(topResult)
            except: 
                continue
        try:
            spotifyObject.user_playlist_add_tracks(user=username,playlist_id=playlist,tracks=songList)
        except:
            continue
"""



###########################################
# Day playlist
print("Generate Day Playlist")
day = input("Entry ID? ")

if day in ZournalScraper.zournal:
    date = ZournalScraper.zournal[day].month + "/" + ZournalScraper.zournal[day].day + "/" + ZournalScraper.zournal[day].year
    
    playlist_name = "Zournal SOTD {}".format(day)
    playlist_description = "Songs of the day from {}".format(date)
    spotifyObject.user_playlist_create(user=username,name=playlist_name,public=True,description=playlist_description)

    prePlaylist = spotifyObject.user_playlists(user=username)
    playlist = prePlaylist['items'][0]['id']

    songList = []

    for song in ZournalScraper.zournal[day].sotd:
        try:
            title = song.title
            artist = song.artists[0]
            query = title + " " + artist
        except:
            query = song.songLine
        try:
            searchResults = spotifyObject.search(q=query)
            topResult = searchResults['tracks']['items'][0]['uri']
            songList.append(topResult)
        except: 
            continue
    try:
        spotifyObject.user_playlist_add_tracks(user=username,playlist_id=playlist,tracks=songList)
    except:
        print("error")
else:
    print("Entry not found.")




