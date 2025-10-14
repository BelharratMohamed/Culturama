import sqlite3
import os,sys
import logging
from collections import defaultdict, Counter

# Fonction pour trouver la base de données
import os
_conn = None
def get_connection(db_path=None):
    global _conn
    if _conn is None:
        db_path = db_path or trouver_base_donnees()
        _conn = sqlite3.connect(db_path)
    return _conn

def trouver_base_donnees(nom_fichier="culturama.db", chemin_defaut=None):
    """
    Recherche récursive du fichier 'culturama.db' en remontant les répertoires.
    Si non trouvé, retourne chemin_defaut s'il est fourni.
    """
    dossier_actuel = os.getcwd()

    while True:
        db_path = os.path.join(dossier_actuel, nom_fichier)
        if os.path.exists(db_path):
            return db_path

        parent = os.path.dirname(dossier_actuel)
        if parent == dossier_actuel:
            # Racine atteinte
            break
        dossier_actuel = parent

    if chemin_defaut and os.path.exists(chemin_defaut):
        print(f"[Fallback] Utilisation du chemin par défaut : {chemin_defaut}")
        return chemin_defaut

    print(" Base de données introuvable.")
    return None

import random

def get_ids_par_type(type_oeuvre, db_path=None):
    """
    Récupère jusqu'à max_results' IDs aléatoires d'œuvres du type donné.
    """
    db_path = db_path or trouver_base_donnees()
    if not db_path:
        return []

    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id FROM oeuvre WHERE nom_type=? and id in(SELECT id_oeuvre FROM recommandation)", (type_oeuvre,))
    ids = [row[0] for row in cur.fetchall()]
    

    return ids
    
def get_ids_recommandation_par_type(type_oeuvre,conn, db_path=None):
    """
    Récupère les ids par type dans la table recommandation.
    """
    
    cur = conn.cursor()
    cur.execute("SELECT id_oeuvre FROM recommandation WHERE id_oeuvre in (SELECT id FROM oeuvre WHERE nom_type = ?) ORDER BY `ordre`",(type_oeuvre,))
    ids = [row[0] for row in cur.fetchall()]
    return ids

def rechercher_oeuvre_par_id(id_oeuvre,conn, db_path=None) -> list[str]:  
    """
    Recherche d'une œuvre dans la base de données à partir de son ID.

    Args:
        id_oeuvre (int): L'identifiant de l'œuvre à rechercher.
        db_path (str, optional): Chemin vers la base de données. Si None, utilise la fonction `trouver_base_donnees`.

    Returns:
        tuple or None: Les données de l'œuvre si trouvée, sinon None.
    """
    db_path = trouver_base_donnees()
    if not db_path:
        print("Base de données introuvable.")
        return None

    
    cur = conn.cursor()

    query = """
        SELECT id, nom, description, date, auteur, popularite, mots_cles, couverture, nom_type, score_evaluation
        FROM oeuvre
        WHERE id = ?
    """
    cur.execute(query, (id_oeuvre,))
    oeuvre = cur.fetchone()
    

    if oeuvre:
        return oeuvre
    else:
        print(f"Aucune œuvre trouvée avec l'ID {id_oeuvre}.")
        return ["0","0"]

# Fonctions pour la gestion des œuvres
def rechercher_oeuvres(db_path=None):
    """
    Recherche interactive d'œuvres dans la base de données.
    """
    db_path = db_path or trouver_base_donnees()
    if not db_path:
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    retour = []

    while True:
        mot_cle = input("\nEntrez un mot-clé pour rechercher une œuvre (ou tapez 'exit' pour quitter) : ").strip()

        if mot_cle.lower() == "exit":
            print("Fin de la recherche.")
            break

        query = """
            SELECT id, nom, description, date, auteur, popularite, mots_cles, couverture, nom_type, score_evaluation
            FROM oeuvre
            WHERE nom LIKE ? OR description LIKE ? OR mots_cles LIKE ? OR nom_type LIKE ?
        """
        params = (f"%{mot_cle}%", f"%{mot_cle}%", f"%{mot_cle}%", f"%{mot_cle}%")
        cur.execute(query, params)
        resultats = cur.fetchall()

        if resultats:
            print("\nŒuvres trouvées :\n")
            for oeuvre in resultats:
                print(f"ID : {oeuvre[0]}")
                print(f"Nom : {oeuvre[1]}")
                print(f"Description : {oeuvre[2]}")
                print(f"Date : {oeuvre[3]}")
                print(f"Auteur : {oeuvre[4]}")
                print(f"Popularité : {oeuvre[5]}")
                print(f"Mots-clés : {oeuvre[6]}")
                print(f"Type : {oeuvre[8]}")
                print(f"Score : {oeuvre[9]}")
                retour.append(oeuvre)
                print("-" * 50)

            voir_recommandations = input("\nVoulez-vous voir des recommandations basées sur ces œuvres ? (O/N) : ").strip().lower()
            if voir_recommandations == "o":
                recommander_oeuvres(resultats, cur)
        else:
            print("Aucune œuvre trouvée avec ce mot-clé.")

    conn.close()

def rechercher_oeuvres_return(conn, text="", categorie=None, type_oeuvre=None, db_path=None):
    """
    Search for works with:
    - Text search
    - Filter by category (if selected)
    - Filter by type (if selected)
    """
    try:
        db_path = db_path or trouver_base_donnees()
        if not db_path:
            return []

        
        cur = conn.cursor()

        query = """
            SELECT id
            FROM oeuvre
            WHERE (? = "" OR nom LIKE ? OR description LIKE ? OR mots_cles LIKE ?)
              AND (? IS NULL OR nom_type = ?)
              AND (? IS NULL OR categorie = ?)
            LIMIT 100
        """
        params = (
            text, f"%{text}%", f"%{text}%", f"%{text}%",
            type_oeuvre, type_oeuvre,
            categorie, categorie
        )

        print("[DEBUG] Requête SQL :", query)
        print("[DEBUG] Paramètres :", params)

        cur.execute(query, params)
        results = cur.fetchall()
        

        return [r[0] for r in results]
    
    except Exception as e:
        print("[ERREUR dans rechercher_oeuvres_return]", e)
        return []


def rechercher_ids_oeuvres_from_searchbox(data):
    """
    Search for works with:
    - Text search
    - Filter by category (if selected)
    - Filter by type (if selected)    
    """
    if not data or len(data) != 3:
        text, categorie, type_oeuvre = "", None, None
    else:
        text, categorie, type_oeuvre = data
    
    # Types normalisation
    type_mapping = {
        "film": "Film",
        "serie": "Série",
        "musique": "Musique",
        "peinturesculpture": "Peinture et Sculpture",
        "livre": "Livre",
        "jeuvideo": "Jeu-vidéo"
    }
    type_oeuvre = type_mapping.get(type_oeuvre, type_oeuvre)
    
    # Inputs cleaning
    text = (text or "").strip()
    type_oeuvre = None if type_oeuvre in ("Types...", "") else type_oeuvre
    categorie = None if categorie in ("Catégories...", "") else categorie  

    try:
        conn = get_connection()
        with conn:
            cur = conn.cursor()

            # SQL requests
            query = """
                SELECT DISTINCT o.id,
                CASE
                    WHEN LOWER(o.nom) LIKE ? THEN 1
                    WHEN LOWER(o.auteur) LIKE ? THEN 2
                    WHEN LOWER(o.mots_cles) LIKE ? THEN 3
                    WHEN LOWER(o.description) LIKE ? THEN 4
                    ELSE 5
                END AS priority
                FROM oeuvre o
            """
            params = []
            
            # Conditional joins with categories
            if categorie:
                query += """
                    JOIN oeuvre_categorie oc ON o.id = oc.id_oeuvre
                    JOIN categorie c ON oc.id_categorie = c.id
                """
            # To avoid injections
            query += " WHERE 1=1"
            
            # Filter by catégorie
            if categorie:
                query += " AND c.nom = ?"
                params.append(categorie)

            # Filter by type
            if type_oeuvre:
                query += " AND o.nom_type = ?"
                params.append(type_oeuvre)

            # Text search
            if text:
                keywords = text.lower().split()
                query += " AND ("
                
                for i, keyword in enumerate(keywords):
                    if i > 0:
                        query += " AND "
                    
                    like_param = f"%{keyword}%"
                    query += """
                        (LOWER(o.nom) LIKE ? OR
                        LOWER(o.auteur) LIKE ? OR
                        LOWER(o.description) LIKE ? OR
                        LOWER(o.mots_cles) LIKE ?)
                    """
                    params.extend([like_param] * 4)
                
                query += ")"
            
            # Order by priority
            query += " ORDER BY priority LIMIT 100"
            
            # Add priority's params
            like_param = f"%{text.lower()}%" if text else ""
            params = [like_param]*4 + params  # for the CASE of the SELECT
            
            cur.execute(query, params)
            return [row[0] for row in cur.fetchall()]

    except (sqlite3.Error, ValueError) as e:
        logging.error(f"Erreur DB: {e}")
        return []

def recommander_oeuvres(id_oeuvre, conn, db_path=None):
    """
    Recommande des œuvres similaires basées sur une œuvre spécifique.
    """
    db_path = db_path or trouver_base_donnees()
    if not db_path:
        return

    try:
        
        cur = conn.cursor()

        cur.execute("SELECT nom, nom_type, mots_cles, score_evaluation FROM oeuvre WHERE id = ?", (id_oeuvre,))
        oeuvre_reference = cur.fetchone()

        if not oeuvre_reference:
            print(f"No reference for id = {id_oeuvre}")
            
            return

        nom_ref, nom_type, mots_cles_ref, score_ref = oeuvre_reference
        print(f"\nWork found: {nom_ref} - Score: {score_ref}\n")

        cur.execute("""
            SELECT id, nom, mots_cles, score_evaluation 
            FROM oeuvre 
            WHERE id != ? and nom_type = ?
            ORDER BY score_evaluation DESC
        """, (id_oeuvre,nom_type))
        resultats = cur.fetchall()

        recommandations = []
        for id_o, nom, mots_cles, score in resultats:
            mots_cles_liste = set(mots_cles.split(", "))
            mots_cles_ref_liste = set(mots_cles_ref.split(", "))
            score_similarite = len(mots_cles_liste & mots_cles_ref_liste) / len(mots_cles_ref_liste)

            if score_similarite > 0:
                recommandations.append({"id": id_o, "nom": nom, "score": score, "similarite": score_similarite})

        recommandations.sort(key=lambda x: (x["similarite"], x["score"] if x["score"] is not None else 0), reverse=True)

        if recommandations:
            return recommandations[:10]
        else:
            print("Aucune recommandation trouvée.")

        
    except sqlite3.Error as e:
        print(f"Erreur de connexion à la base de données : {e}")

def recommander_oeuvres2(oeuvres_trouvees, cur):
    """
    Recommande des œuvres similaires basées sur les mots-clés et le type d'œuvre.
    """
    recommandations = []
    
    for oeuvre in oeuvres_trouvees:
        id_oeuvre, _, _, _, _, popularite, mots_cles, _, nom_type, _ = oeuvre

        query = """
            SELECT id, nom, popularite, mots_cles, nom_type
            FROM oeuvre
            WHERE (mots_cles LIKE ? OR nom_type = ?) AND id != ?
            ORDER BY popularite DESC
            LIMIT 5
        """
        params = (f"%{mots_cles}%", nom_type, id_oeuvre)
        cur.execute(query, params)
        recommandations.extend(cur.fetchall())

    if recommandations:
        print("\nRecommandations d'œuvres similaires :\n")
        for rec in recommandations:
            print(f"{rec[1]} (Popularité : {rec[2]}, Type : {rec[4]})")
        print("-" * 50)
    else:
        print("Aucune recommandation disponible.")

# Fonctions pour les recommandations personnalisées
def get_favorites(user_id, db_path=None):
    """Récupère les œuvres favorites d'un utilisateur."""
    db_path = db_path or trouver_base_donnees()
    if not db_path:
        return []

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    query = """
    SELECT oeuvre.id, oeuvre.nom, oeuvre.mots_cles, oeuvre.nom_type 
    FROM favoris
    JOIN oeuvre ON favoris.oeuvre_id = oeuvre.id
    WHERE favoris.user_id = ?;
    """
    cursor.execute(query, (user_id,))
    favorites = cursor.fetchall()
    
    conn.close()
    return favorites

def get_similar_works(favorites, db_path=None):
    """Recommande des œuvres similaires basées sur les mots-clés et la catégorie."""
    if not favorites:
        return []
    
    db_path = db_path or trouver_base_donnees()
    if not db_path:
        return []

    favorite_categories = set([oeuvre[3] for oeuvre in favorites])
    favorite_keywords = Counter()
    
    for _, _, mots_cles, _ in favorites:
        if mots_cles:
            favorite_keywords.update(mots_cles.lower().split(","))

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
    SELECT id, nom, mots_cles, nom_type 
    FROM oeuvre 
    WHERE nom_type IN ({})
    ORDER BY popularite DESC
    LIMIT 20;
    """.format(",".join("?" * len(favorite_categories)))

    cursor.execute(query, tuple(favorite_categories))
    candidate_works = cursor.fetchall()
    
    conn.close()

    recommendations = []
    for work in candidate_works:
        work_id, work_name, work_keywords, work_category = work
        if work_keywords:
            keywords = work_keywords.lower().split(",")
            similarity_score = sum(favorite_keywords.get(k, 0) for k in keywords)
            recommendations.append((work_id, work_name, similarity_score))
    
    recommendations.sort(key=lambda x: x[2], reverse=True)
    return recommendations[:10]

# Fonctions pour la modification des œuvres
def modifier_oeuvre(db_path=None, id_oeuvre=None, colonne=None, nouvelle_valeur=None):
    """
    Modifie une colonne spécifique d'une œuvre dans la base de données.
    """
    db_path = db_path or trouver_base_donnees()
    if not db_path:
        return

    colonnes_valides = [
        "nom", "date", "auteur", "popularite", "description",
        "like", "couverture", "mots_cles", "nom_type"
    ]
    
    if colonne not in colonnes_valides:
        raise ValueError(f"Colonne '{colonne}' non valide. Choisissez parmi {colonnes_valides}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        query = f"""
        UPDATE oeuvre 
        SET {colonne} = ? 
        WHERE id = ?
        """
        cursor.execute(query, (nouvelle_valeur, id_oeuvre))
        
        conn.commit()
        print(f"L'œuvre avec ID {id_oeuvre} a été mise à jour avec succès.")
    except sqlite3.Error as e:
        print(f"Erreur lors de la mise à jour : {e}")
    finally:
        if conn:
            conn.close()

def modifier_oeuvre_interactif(db_path=None):
    """
    Fonction interactive pour modifier une œuvre dans la base de données.
    """
    db_path = db_path or trouver_base_donnees()
    if not db_path:
        return

    colonnes_valides = [
        "nom", "date", "auteur", "popularite", "description",
        "like", "couverture", "mots_cles", "nom_type"
    ]
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        id_oeuvre = input("Entrez l'ID de l'œuvre à modifier : ").strip()
        
        cursor.execute("SELECT id FROM oeuvre WHERE id = ?", (id_oeuvre,))
        if not cursor.fetchone():
            print(f"Aucune œuvre trouvée avec l'ID {id_oeuvre}.")
            return
        
        print("\nColonnes disponibles pour modification :")
        for i, colonne in enumerate(colonnes_valides, 1):
            print(f"{i}. {colonne}")
        
        choix_colonne = input("\nEntrez le numéro de la colonne à modifier : ").strip()
        try:
            choix_colonne = int(choix_colonne)
            if choix_colonne < 1 or choix_colonne > len(colonnes_valides):
                raise ValueError
        except ValueError:
            print("Choix invalide. Veuillez entrer un numéro valide.")
            return
        
        colonne = colonnes_valides[choix_colonne - 1]
        nouvelle_valeur = input(f"Entrez la nouvelle valeur pour '{colonne}' : ").strip()
        
        query = f"""
        UPDATE oeuvre 
        SET {colonne} = ? 
        WHERE id = ?
        """
        cursor.execute(query, (nouvelle_valeur, id_oeuvre))
        
        conn.commit()
        print(f"L'œuvre avec ID {id_oeuvre} a été mise à jour avec succès.")
    
    except sqlite3.Error as e:
        print(f"Erreur lors de la mise à jour : {e}")
    finally:
        if conn:
            conn.close()

# Fonction pour le parcours des catégories
def parcours_categories(conn, db_path=None, start_category="Sport de combat"):
    """
    Renvoie les sous-catégories directes d'une catégorie donnée (pas de récursivité).
    Si start_category est None ou invalide, retourne les catégories racines.
    """
    import sqlite3
    from collections import defaultdict

    db_path = db_path or trouver_base_donnees()
    if not db_path:
        return []

    
    cursor = conn.cursor()

    cursor.execute("SELECT id, nom, id_parent FROM categorie;")
    categories = cursor.fetchall()
    

    category_tree = defaultdict(list)
    category_name_to_id = {}

    for cat_id, nom, id_parent in categories:
        if nom is None:
            continue
        category_tree[id_parent].append(nom)
        category_name_to_id[nom.lower()] = cat_id

    # Cas racine
    if start_category is None or start_category.lower() not in category_name_to_id:
        return category_tree[None]

    # Sinon, enfants directs de start_category
    start_id = category_name_to_id[start_category.lower()]
    return category_tree[start_id]

# Menu principal
def main():
    print("=== Système de gestion culturelle ===")
    print("1. Rechercher des œuvres")
    print("2. Recommander des œuvres similaires")
    print("3. Obtenir des recommandations personnalisées")
    print("4. Modifier une œuvre")
    print("5. Parcourir les catégories")
    print("6. Quitter")

    choix = input("\nChoisissez une option (1-6) : ").strip()

    if choix == "1":
        rechercher_oeuvres()
    elif choix == "2":
        nom_oeuvre = input("Entrez le nom d'une œuvre : ")
        recommander_oeuvres(nom_oeuvre)
    elif choix == "3":
        user_id = input("Entrez l'ID de l'utilisateur : ")
        favorites = get_favorites(user_id)
        recommendations = get_similar_works(favorites)
        print("\nRecommandations pour l'utilisateur :")
        for rec in recommendations:
            print(f"- {rec[1]} (Score de similarité: {rec[2]})")
    elif choix == "4":
        modifier_oeuvre_interactif()
    elif choix == "5":
        categorie = input("Entrez le nom de la catégorie de départ (vide pour 'Sport de combat') : ").strip()
        parcours_categories(start_category=categorie if categorie else "Sport de combat")
    elif choix == "6":
        print("Au revoir !")
        return
    else:
        print("Option invalide.")

    input("\nAppuyez sur Entrée pour continuer...")
    main()

if __name__ == "__main__":
    main()



def get_resource_path(relative_path):
        """ Find the file, works with PyInstaller, amde with help of an IA """
        try:
            base_path = sys._MEIPASS  # Search the file
        except AttributeError:
            base_path = os.path.abspath(".")  
        return os.path.join(base_path, relative_path)
