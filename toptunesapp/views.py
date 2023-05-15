from django.shortcuts import render
import requests
import json

# Create your views here.

def home(request):
    top_tracks = None

    if request.method == 'POST':
        albumid = request.POST['albumid']

        CLIENT_ID = "646223e1b4234341b3fcf56f6c2f35b8"
        CLIENT_SECRET = "38902bc57e744696a08031fd0efde906"

        grant_type = 'client_credentials'
        body_params = {'grant_type' : grant_type}

        url='https://accounts.spotify.com/api/token'
        response = requests.post(url, data=body_params, auth = (CLIENT_ID, CLIENT_SECRET)) 

        token_raw = json.loads(response.text)
        token = token_raw["access_token"]
        

        URL = f'https://api.spotify.com/v1/albums/{albumid}/tracks'
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
            }
        response = requests.get(URL, headers=headers)
        data = response.json()
        items = data['items']
        ids = [i['id'] for i in items] 
        url = "https://api.spotify.com/v1/tracks"
        headers = {
        "Authorization": f"Bearer {token}"
        }
        params = {
        "ids": ",".join(ids)
        }
        response = requests.get(url, headers=headers, params=params)
        tracks_dict = response.json()
        tracks = tracks_dict['tracks']
        track_info = []
        for track in tracks:
            name = track['name']
            popularity = track['popularity']
            track_info.append({'name': name, 'popularity': popularity})

        sorted_tracks = sorted(track_info, key=lambda x: x['popularity'], reverse=True)
        top_tracks = sorted_tracks[:3]

        

    return render(request, 'home.html', {'top_tracks': top_tracks})