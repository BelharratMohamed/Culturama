import sqlite3
import requests

# --- TMDB API Configuration ---
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiNmJkM2NmMjQwYThlMTI1MjlkNDViNWFjYzczYzMzMiIsIm5iZiI6MTc0MTM2MjI4My4yMzksInN1YiI6IjY3Y2IxNDZiMzBmNDQ0NGM2YjJiNjg1ZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.1axZLW3nIEDvf31Zdqt7lYhjvUPXKC0m8cLQf2I0tMo"
BASE_URL = "https://api.themoviedb.org/3"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# --- Connection to SQLite ---
try:
    conn = sqlite3.connect("../culturama.db")
    cursor = conn.cursor()
    print("✅ Connexion à la base de données réussie.")
except sqlite3.Error as e:
    print(f"❌ Erreur de connexion à la base de données: {e}")
    exit(1)

# --- Select all movies with a description of "Aucune description disponible" ---
try:
    cursor.execute("SELECT id, nom, date FROM oeuvre WHERE description = 'Aucune description disponible' AND nom_type = 'Film'")
    oeuvres = cursor.fetchall()
    print(f"✅ {len(oeuvres)} films à mettre à jour.")
except sqlite3.Error as e:
    print(f"❌ Erreur lors de l'exécution de la requête SQL: {e}")
    exit(1)

if not oeuvres:
    print("⛔ Aucune œuvre de type 'Film' à mettre à jour.")
else:
    for id_oeuvre, nom, date in oeuvres:
        if not nom or not date:
            print(f"⚠️ Données invalides pour l'ID {id_oeuvre}: nom ou date manquants.")
            continue  # Ignore records with invalid data

        # Display of the current work
        print(f"🔍 Recherche pour {nom} ({date})")

        # TMDB API query with English language (default 'en-US')
        popular_movies_url = f"{BASE_URL}/search/movie?query={nom}&year={date}&language=en-US&page=1"
        try:
            response = requests.get(popular_movies_url, headers=HEADERS)
            print(f"🛠 Réponse de l'API pour {nom}: {response.status_code}")
            response.raise_for_status()  # Checks if the API returned an error
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur lors de l'appel API pour {nom}: {e}")
            continue

        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])

            if results:
                new_description = results[0].get("overview", "Aucune description")
                print(f"📝 Nouvelle description pour {nom}: {new_description}")

                # Database update
                try:
                    cursor.execute("UPDATE oeuvre SET description = ? WHERE id = ?", (new_description, id_oeuvre))
                    conn.commit()
                    print(f"✅ Description mise à jour pour {nom}.")
                except sqlite3.Error as e:
                    print(f"❌ Erreur de mise à jour pour {nom}: {e}")
            else:
                print(f"⚠️ Aucune correspondance trouvée dans l'API pour {nom} ({date})")
        else:
            print(f"🚨 Erreur dans la réponse de l'API pour {nom}: Code {response.status_code}")

# Close the connection
conn.close()
print("✅ Connexion à la base de données fermée.")
