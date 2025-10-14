import requests

API_KEY = "b6bd3cf240a8e12529d45b5acc73c332"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
BASE_URL = "https://api.themoviedb.org/3"

# Étape 1 : Récupérer les films populaires
popular_movies_url = f"{BASE_URL}/movie/popular?api_key={API_KEY}&language=fr"
response = requests.get(popular_movies_url, headers=HEADERS)

if response.status_code == 200:
    movies = response.json().get("results", [])
    
    for movie in movies:
        movie_id = movie["id"]
        movie_title = movie["title"]

        # Étape 2 : Récupérer l'équipe du film (crew)
        credits_url = f"{BASE_URL}/movie/{movie_id}/credits?api_key={API_KEY}"
        credits_response = requests.get(credits_url, headers=HEADERS)

        if credits_response.status_code == 200:
            crew = credits_response.json().get("crew", [])
            directors = [person["name"] for person in crew if person["job"] == "Director"]

            if directors:
                print(f"Film : {movie_title} | Réalisateur : {', '.join(directors)}")
            else:
                print(f"Film : {movie_title} | Réalisateur inconnu")
        else:
            print(f"Erreur lors de la récupération du réalisateur pour {movie_title}")

else:
    print("Erreur lors de la récupération des films populaires :", response.status_code)
