import sqlite3
import requests

# Deezer API Configuration
API_URL = "https://api.deezer.com/playlist/9068702062"

# Connection to SQLite
conn = sqlite3.connect("../culturama.db")
cursor = conn.cursor()

# Requête vers l'API Deezer
response = requests.get(API_URL)

if response.status_code == 200:
    data = response.json()
    tracks = data.get("tracks", {}).get("data", [])[:30]  # Limite aux 30 premières musiques

    for track in tracks:
        track_id = track.get("id","")
        title = track.get("title", "Inconnu")
        artist = track.get("artist", {}).get("name", "Inconnu")
        cover = track.get("album", {}).get("cover", "")
        popularity = track.get("rank","Inconnu")
        date=""
        
        # Récupération des détails du morceau pour obtenir la date
        track_details_url = f"https://api.deezer.com/track/{track_id}"
        track_response = requests.get(track_details_url)
        
        if track_response.status_code == 200:
            track_info = track_response.json()
            date = track_info.get("release_date", "")  
        # Insertion dans la base de données
        cursor.execute("""
            INSERT INTO oeuvre (nom, auteur, couverture, date, popularite, nom_type)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, artist, cover, date, popularity, "Musique"))

    conn.commit()
    print("✅ Musiques insérées avec succès.")
else:
    print("❌ Erreur lors de la récupération de la playlist Deezer.")

# --- Close the connection ---
conn.close()
