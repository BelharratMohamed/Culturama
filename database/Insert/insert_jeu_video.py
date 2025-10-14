import sqlite3
import requests

# --- RAWG API Configuration ---
API_KEY = "bfe3644e84924dc6b1e5095570b9743d"
BASE_URL = "https://api.rawg.io/api/games"

# --- Connecting to SQLite ---
conn = sqlite3.connect("../culturama.db")
cursor = conn.cursor()

# --- Recover Popular Video Games ---
for page in range(1, 11):  
    search_url = f"{BASE_URL}?key={API_KEY}&page={page}"
    response = requests.get(search_url)

    if response.status_code == 200:
        data = response.json()

        if "results" in data:
            for game in data["results"]:
                game_title = game.get("name")
                game_id = game.get("id")  
                score_evaluation = game.get("rating", None)
                couverture = game.get("background_image", None)
                mots_cles = ", ".join([tag["name"] for tag in game.get("tags", [])]) if game.get("tags") else "Aucun"
                date = game.get("released", "Date inconnue")
                
                # --- Retrieve description and developers via a second API call ---
                details_url = f"https://api.rawg.io/api/games/{game_id}?key={API_KEY}"
                details_response = requests.get(details_url)
                
                if details_response.status_code == 200:
                    game_details = details_response.json()
                    description = game_details.get("description_raw", "Aucune description disponible")
                    developers = ", ".join([dev["name"] for dev in game_details.get("developers", [])]) if game_details.get("developers") else "Inconnu"
                else:
                    description = "Aucune description disponible"
                    developers = "Inconnu"

                # --- Check if the game is already in the database ---
                cursor.execute("SELECT COUNT(*) FROM oeuvre WHERE nom = ?", (game_title,))
                if cursor.fetchone()[0] == 0:
                    try:
                        cursor.execute("""
                            INSERT INTO oeuvre (nom, description, score_evaluation, couverture, nom_type, mots_cles, date, auteur)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (game_title, description, score_evaluation, couverture, "Jeu_vidéo", mots_cles, date, developers))
                        print(f"✅ Jeu inséré : {game_title}")
                    except sqlite3.Error as e:
                        print(f"❌ Erreur SQL lors de l'insertion de '{game_title}': {e}")

            conn.commit()

    else:
        print(f"❌ Erreur lors de la récupération des jeux vidéo de la page {page} :", response.status_code)

# --- Close the connection ---
conn.commit()
conn.close()

print("✅ Jeux vidéo insérés avec succès.")
