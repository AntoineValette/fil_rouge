import requests

# Clé d'API Crunchbase
API_KEY = "aa316dfa75128c027b7582c104293ddb"

# L'identifiant de l'organisation
entity_id = "df662812-7f97-0b43-9d3e-12f64f504fbb"

# URL de base pour l'endpoint
base_url = "https://api.crunchbase.com/api/v4/entities/organizations/"
url = f"{base_url}{entity_id}"

# Liste des champs à récupérer (séparés par des virgules)
fields = (
    "acquiree_acquisitions,acquirer_acquisitions,child_organizations,child_ownerships,"
    "event_appearances,fields,founders,headquarters_address,investors,ipos,jobs,"
    "key_employee_changes,layoffs,parent_organization,parent_ownership,"
    "participated_funding_rounds,participated_funds,participated_investments,"
    "press_references,raised_funding_rounds,raised_funds,raised_investments"
)

# Effectue la requête GET en passant la clé d'API et les champs souhaités en paramètres
response = requests.get(url, params={"user_key": API_KEY, "field_ids": fields})

# Vérifie si la requête a réussi et affiche les données
if response.status_code == 200:
    data = response.json()
    print("Données de l'organisation :")
    print(data)
else:
    print(f"Erreur {response.status_code}: {response.text}")