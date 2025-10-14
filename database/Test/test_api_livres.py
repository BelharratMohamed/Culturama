import requests

API_KEY = "AIzaSyB3JwEFXovRDDWSyS-x7dMsgiE_z5hz5zk"
BASE_URL = "https://www.googleapis.com/books/v1/volumes"

def get_book_info(query):
    url = f"{BASE_URL}?q={query}&key={API_KEY}"
    response = requests.get(url)
    return response.json()

# Exemple pour rechercher un livre
book_info = get_book_info("Le Petit Prince")
print(book_info)
