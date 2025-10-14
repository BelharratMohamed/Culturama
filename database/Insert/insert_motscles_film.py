import sqlite3
import requests

# --- TMDB API Configuration ---
API_KEY = "b6bd3cf240a8e12529d45b5acc73c332"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
BASE_URL = "https://api.themoviedb.org/3"

# --- Connecting to SQLite ---
conn = sqlite3.connect("../culturama.db")
cursor = conn.cursor()

# --- Retrieve all movies without keywords ---
cursor.execute("SELECT id, nom FROM oeuvre WHERE nom_type = 'Film' AND (mots_cles IS NULL OR mots_cles = '')")
films = cursor.fetchall()

print(f"🎬 {len(films)} films à mettre à jour...")

for film_id, film_title in films:
    # --- Retrieve the movie's TMDB ID ---
    search_url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={film_title}&language=fr"
    search_response = requests.get(search_url, headers=HEADERS)

    if search_response.status_code == 200 and search_response.json().get("results"):
        tmdb_id = search_response.json()["results"][0]["id"]

        # --- Retrieve movie keywords ---
        keywords_url = f"{BASE_URL}/movie/{tmdb_id}/keywords?api_key={API_KEY}&language=fr"
        keywords_response = requests.get(keywords_url, headers=HEADERS)

        if keywords_response.status_code == 200:
            keywords_data = keywords_response.json()
            keywords = [kw["name"] for kw in keywords_data.get("keywords", [])]
            mots_cles = ", ".join(keywords) if keywords else "Aucun"

            # --- Update the database ---
            cursor.execute("UPDATE oeuvre SET mots_cles = ? WHERE id = ?", (mots_cles, film_id))
            print(f"✅ {film_title} mis à jour avec les mots-clés : {mots_cles}")

        else:
            print(f"❌ Erreur lors de la récupération des mots-clés pour {film_title}")

    else:
        print(f"⚠️ Impossible de trouver {film_title} sur TMDB")

# Save changes
conn.commit()

# --- Close the connexion ---
conn.close()
print("🎉 Mise à jour terminée !")

