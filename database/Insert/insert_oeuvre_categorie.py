import sqlite3

# Connection to the base database
conn = sqlite3.connect("../culturama.db")
cursor = conn.cursor()

# Recover the movies
cursor.execute("SELECT id FROM oeuvre WHERE nom_type='Série'")
oeuvres = cursor.fetchall()

# Parent categories
categories = [604,60,6]

# Insertion
for (id_oeuvre,) in oeuvres:
    for id_categorie in categories:
        cursor.execute(
            "INSERT OR IGNORE INTO oeuvre_categorie (id_oeuvre, id_categorie) VALUES (?, ?)",
            (id_oeuvre, id_categorie),
        )

# Validate and close the connection
conn.commit()
conn.close()

print("✅ Associations ajoutées avec succès.")
