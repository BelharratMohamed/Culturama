import sqlite3
import requests

# --- TMDB API Configuration ---
API_KEY = "b6bd3cf240a8e12529d45b5acc73c332"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
BASE_URL = "https://api.themoviedb.org/3"

# --- Connecting to SQLite ---
conn = sqlite3.connect("../culturama.db")  # Remplace par ton chemin si besoin
cursor = conn.cursor()

# --- Recover popular series ---
for page in range(1, 11):  # To retrieve the series from pages 1 to 10
    popular_series_url = f"{BASE_URL}/tv/popular?api_key={API_KEY}&language=fr&page={page}"
    response = requests.get(popular_series_url, headers=HEADERS)

    if response.status_code == 200:
        series = response.json().get("results", [])

        for show in series:
            show_id = show["id"]
            show_title = show["name"]
            description = show.get("overview", "Aucune description")
            date = show.get("first_air_date", "Inconnue")
            popularite = show.get("popularity", 0)
            couverture = f"https://image.tmdb.org/t/p/w500{show.get('poster_path', '')}" if show.get("poster_path") else None

            # --- Recover the series creator ---
            details_url = f"{BASE_URL}/tv/{show_id}?api_key={API_KEY}&language=fr"
            details_response = requests.get(details_url, headers=HEADERS)

            if details_response.status_code == 200:
                details = details_response.json()
                creators = [person["name"] for person in details.get("created_by", [])]
                auteur = creators[0] if creators else "Inconnu"

                # --- Retrieve keywords ---
                keywords_url = f"{BASE_URL}/tv/{show_id}/keywords?api_key={API_KEY}"
                keywords_response = requests.get(keywords_url, headers=HEADERS)

                if keywords_response.status_code == 200:
                    keywords_data = keywords_response.json()
                    keywords = [kw["name"] for kw in keywords_data.get("results", [])]
                    mots_cles = ", ".join(keywords) if keywords else "Aucun"
                else:
                    mots_cles = "Aucun"

                # --- Check if the work is already in the database ---
                cursor.execute("SELECT COUNT(*) FROM oeuvre WHERE nom = ?", (show_title,))
                if cursor.fetchone()[0] == 0:
                    # --- Insert into SQLite ---
                    cursor.execute("""
                        INSERT INTO oeuvre (nom, description, date, auteur, popularite, couverture, nom_type, mots_cles)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (show_title, description, date, auteur, popularite, couverture, "Série", mots_cles))

                    print(f"✅ Ajouté : {show_title} | Créateur : {auteur} | Mots-clés : {mots_cles}")
                else:
                    print(f"⚠️ Déjà présent : {show_title}")

            else:
                print(f"❌ Erreur sur {show_title} - Impossible de récupérer le créateur")

        print(f"✅ Séries de la page {page} ajoutées avec succès.")

    else:
        print(f"❌ Erreur lors de la récupération des séries de la page {page} :", response.status_code)

# Save changes to the database
conn.commit()

# --- Close the connection ---
conn.close()
