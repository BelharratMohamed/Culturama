import requests
import sqlite3

# Connection to SQLITE 
conn = sqlite3.connect("../culturama.db") 
cursor = conn.cursor()

# Configuration of WikiArt's API
WIKIART_API_URL = "https://www.wikiart.org/en/App/Painting/MostViewedPaintings?offset=0&quantity=100&limit=100&randomSeed=123&json=2"

response = requests.get(WIKIART_API_URL)

if response.status_code == 200:
    paints = response.json()

    for paint in paints:
        paint_id = paint.get("contentId")
        title = paint.get("title", "Inconnu")
        artist = paint.get("artistName", "Inconnu")
        date = paint.get("yearAsString", "")
        couverture = paint.get("image", "")

        # Retrieve the description and the tags
        get_description_tags_url = f"https://www.wikiart.org/en/App/Painting/ImageJson/{paint_id}"
        description_tags_response = requests.get(get_description_tags_url)

        description = ""
        tags = ""

        if description_tags_response.status_code == 200:
            details = description_tags_response.json()
            description = details.get("description", "")
            tags = details.get("tags", "")
            # Insert into SQLITE
            cursor.execute("""
                INSERT INTO oeuvre (nom, description, date, auteur, couverture, mots_cles, nom_type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (title, description, date, artist, couverture, tags, "Peinture et Sculpture"))
            conn.commit()

        print(f"🎨 {title} par {artist} ({date})")
        print(f"🖼️ couverture: {couverture}")
        print(f"📝 Description: {description}")
        print(f"🏷️ Tags: {tags}")
        print("------")
else:
    print("Erreur lors de la récupération des peintures")

# Close the connection to the database
conn.close()
