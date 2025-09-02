import requests

# Clé d'API Crunchbase
API_KEY = "aa316dfa75128c027b7582c104293ddb"

# L'identifiant de l'organisation
entity_id = "a01b8d46-d311-3333-7c34-aa3ae9c03f22"
# entity_id = "https://www.crunchbase.com/person/mark-zuckerberg"

# URL de base pour l'endpoint
base_url = "https://api.crunchbase.com/api/v4/entities/people/"

# Construit l'URL complète avec l'ID
url = f"{base_url}{entity_id}"

# Effectue la requête GET en passant la clé d'API en paramètre
response = requests.get(url, params={"user_key": API_KEY})

# Vérifie si la requête a réussi et affiche les données
if response.status_code == 200:
    data = response.json()
    print("Données de l'organisation :")
    print(data)
else:
    print(f"Erreur {response.status_code}: {response.text}")