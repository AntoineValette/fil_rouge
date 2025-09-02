import requests
import time
import json  # Pour sauvegarder les résultats

from python.semantic_scholar.print_article import printArticle


def fetch_all_responses(base_url):
    """
    Récupère toutes les pages de réponses (en suivant le token de pagination)
    et retourne une liste contenant l'ensemble des réponses.
    
    Logique ajoutée :
      - Lorsqu'un token déjà vu est rencontré, on stocke la réponse dans r_seen.
      - Au début de la boucle interne, on compare le token courant au token de la boucle précédente.
        Si les deux sont identiques, on prend le token contenu dans r_seen.
        Sinon, on prend le token courant (r['token']).
    """
    responses = []
    headers = {"User-Agent": "SemanticScholarScraper/1.0"}
    seen_tokens = set()
    
    # Pour mémoriser le token de la boucle précédente et la réponse associée en cas de doublon
    prev_token = None
    r_seen = None

    while True:
        try:
            response = requests.get(base_url, headers=headers)
            
            if response.status_code == 429:  # Trop de requêtes
                wait_time = 10
                print(f"⚠️ Trop de requêtes ! Attente de {wait_time}s avant de réessayer...")
                time.sleep(wait_time)
                continue  # Réessayer immédiatement après la pause
            
            response.raise_for_status()  # Vérifie les erreurs HTTP
            r = response.json()
            responses.append(r)
            
            print(f"📊 Nombre total annoncé par l'API : {r.get('total', 'inconnu')}")

            # Boucle de pagination
            while "token" in r:
                # Vérification en début de boucle :
                # Si le token courant est identique au token de la boucle précédente
                # et qu'une réponse duplicate a été stockée, on utilise son token.
                if prev_token is not None and r.get("token") == prev_token and r_seen is not None:
                    token = r_seen.get("token")
                    print(f"🔄 Token inchangé, utilisation du token stocké dans r_seen : {token}")
                else:
                    token = r.get("token")

                if token is None:
                    print("✅ Fin de pagination : plus de token disponible.")
                    break  # Fin de la pagination

                # Si le token a déjà été vu, on stocke la réponse dans r_seen
                # puis on continue pour forcer la récupération d'une nouvelle page.
                if token in seen_tokens:
                    print(f"🔁 Token {token} déjà récupéré, stockage dans r_seen et passage à la page suivante...")
                    r_seen = r
                    time.sleep(3)  # Petite pause pour éviter le throttling
                    response = requests.get(f"{base_url}&token={token}", headers=headers)
                    if response.status_code == 429:
                        wait_time = 10
                        print(f"⚠️ Trop de requêtes ! Attente de {wait_time}s avant de réessayer...")
                        time.sleep(wait_time)
                        continue  # Réessayer après la pause
                    response.raise_for_status()
                    r_seen = response.json()
                    continue  # Retour en début de boucle pour vérifier le token actualisé
                
                # Nouveau token non vu, on l'ajoute à l'ensemble
                seen_tokens.add(token)
                print(f"📄 Passage à la page suivante avec token : {token}") 

                time.sleep(3)  # Pause pour éviter le throttling
                response = requests.get(f"{base_url}&token={token}", headers=headers)
                if response.status_code == 429:
                    wait_time = 10
                    print(f"⚠️ Trop de requêtes ! Attente de {wait_time}s avant de réessayer...")
                    time.sleep(wait_time)
                    continue
                response.raise_for_status()
                r = response.json()
                if "token" not in r:
                    print("⚠️ L'API ne fournit plus de token après cette page.")
                
                responses.append(r)
                # Mémorisation du token courant pour la prochaine itération
                prev_token = token
                # On réinitialise r_seen puisque le token a changé
                r_seen = None

            return responses  # Sortie propre de la boucle principale

        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur réseau : {e}")
            wait_time = 10
            print(f"🕒 Attente de {wait_time}s avant de réessayer...")
            time.sleep(wait_time)  # Pause avant de réessayer

    return responses



def combine_data(responses):
    """
    Combine les listes "data" de chacune des réponses en une seule liste.
    """
    combined = []
    for resp in responses:
        if "data" in resp:
            combined.extend(resp["data"])
    return combined


def get_data_JSON(year=2020):
    """
    Récupère les données des articles publiés entre 2020 et 2023 avec l'API Semantic Scholar.
    """

    # Définition des paramètres de la requête
    query = "artificial intelligence | AI"
    fields = ("paperId,corpusId,externalIds,url,title,authors,venue,publicationVenue,"
              "year,fieldsOfStudy,s2FieldsOfStudy,publicationTypes,publicationDate,journal,abstract")

    all_data = []

    for month in range(1, 13):  # De janvier (1) à décembre (12)
        date_filter = f"{year}-{month:02d}"  # Format YYYY-MM

        url = (f"http://api.semanticscholar.org/graph/v1/paper/search/bulk?query={query}"
                f"&publicationDateOrYear={date_filter}"
                f"&fields={fields}"
                f"&maxResults=10000")  # Récupération par blocs de 10 000

        print(f"🔍 Requête envoyée pour {date_filter}")

        responses = fetch_all_responses(url)
        all_data.extend(combine_data(responses))  # Fusionner les résultats

        print(f"📊 Articles récupérés jusqu’ici : {len(all_data)}")
        
        # 💡 Pause de 3 secondes pour éviter d’être bloqué par l’API
        time.sleep(3)

    print(f"✅ Nombre total d'articles récupérés en {year} : {len(all_data)}")

    return all_data


if __name__ == "__main__":
    articles = get_data_JSON(year=2020)
    for article in articles[:5]:  # Afficher les 5 premiers articles
        print(article)
        printArticle(article)
