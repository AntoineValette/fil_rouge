import json
import requests

from python.semantic_scholar.semantic_functions.get_authors_IDs import get_authors_IDs

"""
BUT : récupérer les ORCID qui sont parfois dans les external IDs des auteurs sur Semantic Scholar
ou essayer d'obtenir des noms complets (sans initial)
"""

# Récupération de la liste des IDs d'auteurs
list_authors = get_authors_IDs()

# Définition de l'URL et des paramètres sans virgule finale (pour éviter d'en faire des tuples)
url = 'https://api.semanticscholar.org/graph/v1/author/batch'
params = {'fields': 'name,externalIds,url,affiliations,homepage'}

batch_size = 1000

for i in range(0, len(list_authors), batch_size):
    batch = list_authors[i:i + batch_size]
    payload = {"ids": batch}

    r = requests.post(
        url,
        params=params,
        json=payload
    )

    # Affiche le JSON formaté pour chaque batch
    print(json.dumps(r.json(), indent=2))


