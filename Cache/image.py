import sqlite3
import requests
import os

# Connection to the database
conn = sqlite3.connect("../database/culturama.db")
cursor = conn.cursor()

# Retrieve covers of each work
cursor.execute("SELECT id, couverture FROM oeuvre WHERE id=1408 OR id=1430")
oeuvres = cursor.fetchall()

for id_oeuvre, couverture in oeuvres:
    # Define a file name based on the work ID
    image_name = f"{id_oeuvre}.jpg"
    image_path = image_name
    
    # Check if the cover is already downloaded
    if not os.path.exists(image_path):
        print(f"⏳ Téléchargement de {couverture}...")
        try:
            response = requests.get(couverture, stream=True)
            if response.status_code == 200:
                # Binary writing
                with open(image_path, "wb") as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"✅ Image {image_name} enregistrée !")
            else:
                print(f"❌ Erreur lors du téléchargement de {couverture}")
        except Exception as e:
            print(f"❌ Échec : {e}")

# Close the connection
conn.close()
