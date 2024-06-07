import os
import base64
from requests import post, get
from dotenv import load_dotenv
import json

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)

    if result.status_code == 200:
        json_result = result.json()
        return json_result["access_token"]
    else:
        raise Exception("Failed to get token.")

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_song(token, song_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={song_name}&type=track&limit=10"
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["tracks"]["items"]
    if len(json_result) == 0:
        print("No songs found")
        return None
    
    return json_result

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=5"
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = result.json()
    return json_result['artists']['items']

def get_artist_details(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_auth_header(token)    
    result = get(url, headers=headers)
    return result.json()

def get_artist_top_tracks(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    return result.json()['tracks']

# app/spotify.py

def get_top_artists(token, limit=10):
    url = f"https://api.spotify.com/v1/browse/featured-playlists?limit={limit}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    playlists = json.loads(result.content)["playlists"]["items"]
    top_artists = []
    seen_artists = set()
    for playlist in playlists:
        playlist_id = playlist["id"]
        playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        playlist_result = get(playlist_url, headers=headers)
        tracks = json.loads(playlist_result.content)["items"]
        for track in tracks:
            artist = track["track"]["artists"][0]
            artist_id = artist["id"]
            if artist_id not in seen_artists and len(top_artists) < limit:
                artist_url = f"https://api.spotify.com/v1/artists/{artist_id}"
                artist_result = get(artist_url, headers=headers)
                artist_data = json.loads(artist_result.content)
                top_artists.append({
                    "name": artist_data["name"],
                    "image": artist_data["images"][0]["url"] if artist_data["images"] else None
                })
                seen_artists.add(artist_id)
    return top_artists

def get_top_albums(token, limit=10):
    url = f"https://api.spotify.com/v1/browse/new-releases?limit={limit}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    albums = json.loads(result.content)["albums"]["items"]
    top_albums = []
    for album in albums:
        top_albums.append({
            "name": album["name"],
            "image": album["images"][0]["url"] if album["images"] else None,
            "artist_name": album["artists"][0]["name"]
        })
    return top_albums


