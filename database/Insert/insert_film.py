import requests
import sqlite3

# Configuration of TMDB's API
API_KEY = "b6bd3cf240a8e12529d45b5acc73c332"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
BASE_URL = "https://api.themoviedb.org/3"

# --- Connection to SQLITE ---
conn = sqlite3.connect("../culturama.db")
cursor = conn.cursor()

# --- Recover popular movies ---
for page in range(1, 11):  # To retrieve the films on pages 1 to 10
    popular_movies_url = f"{BASE_URL}/movie/popular?api_key={API_KEY}&language=fr&page={page}"
    response = requests.get(popular_movies_url, headers=HEADERS)

    if response.status_code == 200:
        movies = response.json().get("results", [])

        for movie in movies:
            movie_id = movie["id"]
            movie_title = movie["title"]
            description = movie.get("overview", "Aucune description")
            date = movie.get("release_date", "Inconnue")
            popularite = movie.get("popularity", 0)
            couverture = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path', '')}" if movie.get("poster_path") else None

            # --- Recover the director ---
            credits_url = f"{BASE_URL}/movie/{movie_id}/credits?api_key={API_KEY}"
            credits_response = requests.get(credits_url, headers=HEADERS)

            if credits_response.status_code == 200:
                crew = credits_response.json().get("crew", [])
                directors = [person["name"] for person in crew if person["job"] == "Director"]
                auteur = directors[0] if directors else "Inconnu"

                # --- Insert into SQLITE ---
                cursor.execute("""
                    INSERT INTO oeuvre (nom, description, date, auteur, popularite, couverture, nom_type)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (movie_title, description, date, auteur, popularite, couverture, "Film"))

                print(f"Ajouté : {movie_title} | Réalisateur : {auteur}")

            else:
                print(f"❌ Erreur sur {movie_title} - Impossible de récupérer le réalisateur")

        print(f"✅ Films de la page {page} ajoutés avec succès.")

    else:
        print(f"❌ Erreur lors de la récupération des films de la page {page} :", response.status_code)

# --- Save changes to the database ---
conn.commit()

# --- Close the connection ---
conn.close()
