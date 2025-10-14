import sqlite3
import requests

# --- Configuring the Google Books API ---
API_KEY = "AIzaSyB3JwEFXovRDDWSyS-x7dMsgiE_z5hz5zk" 
BASE_URL = "https://www.googleapis.com/books/v1/volumes"

# --- Coonnection to SQLite ---
conn = sqlite3.connect("../culturama.db")  
cursor = conn.cursor()

# --- Retrieve the books from pages 1 to 10 ---
for page in range(1, 11):
    search_url = f"{BASE_URL}?q=subject:fiction&key={API_KEY}&langRestrict=fr&page={page}"
    response = requests.get(search_url)

    if response.status_code == 200:
        data = response.json()

        if "items" in data:
            count = 0  # Counter to limit the number of inserts before commit
            for book in data["items"]:
                book_info = book["volumeInfo"]
                book_title = book_info.get("title")
                description = book_info.get("description", "Aucune description disponible")
                score_evaluation = book_info.get("averageRating", None)
                couverture = book_info.get("imageLinks", {}).get("thumbnail", None)
                mots_cles = ", ".join(book_info.get("categories", [])) if "categories" in book_info else "Aucun"
                auteur = ", ".join(book_info.get("authors", ["Auteur inconnu"])) if "authors" in book_info else "Auteur inconnu"
                date = book_info.get("publishedDate", "Date inconnue")

                # --- Check if the book is already in the database ---
                cursor.execute("SELECT COUNT(*) FROM oeuvre WHERE nom = ?", (book_title,))
                if cursor.fetchone()[0] == 0:
                    # --- Insert into SQLite ---
                    cursor.execute("""
                        INSERT INTO oeuvre (nom, description, score_evaluation, couverture, nom_type, mots_cles, auteur, date)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (book_title, description, score_evaluation, couverture, "Livre", mots_cles, auteur, date))
                    count += 1

                    # --- Commit after every 50 inserts to avoid locking ---
                    if count % 50 == 0:
                        conn.commit()
                        print(f"✅ {count} livres insérés, commit effectué.")

            # Final commit after the last page
            conn.commit()

        else:
            print(f"⚠️ Aucune donnée trouvée pour cette page")

    else:
        print(f"❌ Erreur lors de la récupération des livres de la page {page} :", response.status_code)

conn.commit()

# --- Close the connection ---
conn.close()

print("✅ Livres des pages 6 à 10 insérés avec succès.")
