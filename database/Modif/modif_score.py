import sqlite3
import requests

# --- TMDB API Configuration ---
API_KEY = "b6bd3cf240a8e12529d45b5acc73c332"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
BASE_URL = "https://api.themoviedb.org/3"

# --- Connection to SQLite ---
conn = sqlite3.connect("../culturama.db")  # Remplace par ton chemin si besoin
cursor = conn.cursor()

# --- Retrieve all works without a rating score ---
cursor.execute("SELECT id, nom FROM oeuvre WHERE score_evaluation IS NULL")
works = cursor.fetchall()

print(f"📚 {len(works)} œuvres à mettre à jour avec le score d'évaluation...")

for work_id, work_title in works:
    # --- Search the work on TMDB by name ---
    search_url = f"{BASE_URL}/search/multi?api_key={API_KEY}&query={work_title}&language=fr"
    search_response = requests.get(search_url, headers=HEADERS)

    if search_response.status_code == 200:
        search_results = search_response.json().get("results", [])
        
        # If results are found, retrieve the information
        if search_results:
            result = search_results[0]  # Choose the first result found

            # Extract the evaluation score
            if result.get("media_type") == "movie" or result.get("media_type") == "tv":
                score_evaluation = result.get("vote_average", 0)

                # --- Update the database ---
                cursor.execute("""
                    UPDATE oeuvre 
                    SET score_evaluation = ? 
                    WHERE id = ?
                """, (score_evaluation, work_id))

                print(f"✅ Mise à jour du score pour : {work_title} | Score : {score_evaluation}")
            else:
                print(f"⚠️ Résultat non valide pour {work_title}.")

        else:
            print(f"⚠️ Aucun résultat trouvé pour {work_title}")

    else:
        print(f"❌ Erreur lors de la recherche pour {work_title} - Status code : {search_response.status_code}")

conn.commit()

# --- Close the connection ---
conn.close()
print("🎉 Mise à jour terminée !")

