import sqlite3

# Connection to the database
conn = sqlite3.connect("../culturama.db")
cursor = conn.cursor()

# Insertion script
types = ["Film", "Série", "Livre", "Jeu_vidéo", "Musique", "Peinture_Sculpture"]

for t in types:
    cursor.execute("INSERT INTO type (nom) SELECT ? WHERE NOT EXISTS (SELECT 1 FROM type WHERE nom = ?)", (t, t))

# Validate and close
conn.commit()
conn.close()

