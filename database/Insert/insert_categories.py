import csv
import sqlite3

# Connection to the database
conn = sqlite3.connect("../culturama.db")
cursor = conn.cursor()

# Open the CSV file
with open("../data/categories.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)  # Ignore the first line indicating the columns

    for row in reader:
        try:
            # Veriff if the line contains 3 columns
            if len(row) < 3:
                raise ValueError(f"Ligne mal formatée, nombre de colonnes insuffisant : {row}")

            # Values extraction
            id_cat = int(row[0])
            nom = row[1].strip().replace('"', '')
            id_parent = row[2].strip()
            id_parent = int(id_parent) if id_parent != "NULL" else None
            
            # Veriff if the id already exists
            cursor.execute("SELECT 1 FROM categorie WHERE id = ?", (id_cat,))
            if cursor.fetchone():
                print(f"ID {id_cat} déjà existant, ligne ignorée.")
                continue  # Ignore this line if the id already exists

            # Insert in the database
            cursor.execute("INSERT INTO categorie (id, nom, id_parent) VALUES (?, ?, ?)", (id_cat, nom, id_parent))

        except ValueError as e:
            print(f"Erreur dans la ligne : {e}")
            break  # Stop the script execution if a line is poorly formatted

# Validate and close
conn.commit()
conn.close()
