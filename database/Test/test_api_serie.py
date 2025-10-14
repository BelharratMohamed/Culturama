import requests

API_KEY = "b6bd3cf240a8e12529d45b5acc73c332"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
BASE_URL = "https://api.themoviedb.org/3"

# Étape 1 : Récupérer les séries populaires
popular_series_url = f"{BASE_URL}/tv/popular?api_key={API_KEY}&language=fr"
response = requests.get(popular_series_url, headers=HEADERS)

if response.status_code == 200:
    series = response.json().get("results", [])
    
    for show in series:
        show_id = show["id"]
        show_name = show["name"]

        # Étape 2 : Récupérer les créateurs de la série
        details_url = f"{BASE_URL}/tv/{show_id}?api_key={API_KEY}&language=fr"
        details_response = requests.get(details_url, headers=HEADERS)

        if details_response.status_code == 200:
            details = details_response.json()
            creators = [person["name"] for person in details.get("created_by", [])]

            if creators:
                print(f"Série : {show_name} | Créateur(s) : {', '.join(creators)}")
            else:
                print(f"Série : {show_name} | Créateur inconnu")
        else:
            print(f"Erreur lors de la récupération du créateur pour {show_name}")

else:
    print("Erreur lors de la récupération des séries populaires :", response.status_code)
