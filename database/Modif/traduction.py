import requests
import sqlite3
import deepl

# --- DeepL API configuration ---
API_KEY = "2e65afe6-ba69-4681-87eb-4c3b09ee0a0f:fx"
translator = deepl.Translator(API_KEY)

# --- Connection to SQLite ---
conn = sqlite3.connect("../culturama.db")
cursor = conn.cursor()

# --- English keyword recovery ---
cursor.execute("SELECT id, mots_cles, nom FROM oeuvre WHERE nom_type = 'Jeu-vidéo'")
oeuvres = cursor.fetchall()

for oeuvre_id, mots_cles, nom in oeuvres:
    if mots_cles:  # Checks if the keywords exist
        try:
            # Translation of keywords into French
            mots_cles_traduite = translator.translate_text(mots_cles, target_lang="FR").text

            # Database update
            cursor.execute("UPDATE oeuvre SET mots_cles = ? WHERE id = ?", (mots_cles_traduite, oeuvre_id))
            conn.commit()
			
            print(f"✅ Mots-clés traduite pour l'œuvre ID {oeuvre_id} Nom {nom}")

        except Exception as e:
            print(f"❌ Erreur de traduction pour l'œuvre ID {oeuvre_id} : {e}")
# Close the connection
conn.close()
