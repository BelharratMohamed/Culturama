import requests

URL = "https://api.deezer.com/chart"
response = requests.get(URL)

if response.status_code == 200:
    data = response.json()
    for track in data["tracks"]["data"]:
        print(f"{track['title']} - {track['artist']['name']}")

