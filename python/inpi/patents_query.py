
import requests
from bs4 import BeautifulSoup
import json

from python.inpi.token_manager2 import get_inpi_tokens


def nb_patents_by_year(secrets: list, year: str) -> int:
    """
    Renvoie pour une année donnée le nombre de brevets déposés qui portent sur le domaine G06.
    Dans la classification CIB, il s'agit du domaine CALCUL; COMPTAGE. https://ipcpub.wipo.int/
    Args:
        secrets (list): Liste contenant xsrf_token, access_token, refresh_token.
        annee (str): Année ciblée pour la recherche.

    """

    xsrf_token, access_token, refresh_token = secrets[0], secrets[1], secrets[2]

    # En-têtes de la requête et cookies
    headers = {
        'Accept': 'application/json',
        'X-XSRF-TOKEN': xsrf_token,
        'Cookie': f'XSRF-TOKEN={xsrf_token}; access_token={access_token}; session_token={refresh_token}'
    }
    cookies = {
        'XSRF-TOKEN': xsrf_token,
        'access_token': access_token,
        'session_token': refresh_token
    }

    requete = f"[ABFR=(intelligence artificielle OU artificial intelligence)] ET [DEPD={year}]"
    data = {
        "collections": ["FR", "EP", "WO", "CCP"],
        "query": requete,
        "size": 1
    }
    url_inpi_search = 'https://api-gateway.inpi.fr/services/apidiffusion/api/brevets/search'
    response = requests.post(url_inpi_search, json=data, headers=headers, cookies=cookies)

    # Conversion de la réponse en JSON
    responseJSON = response.content
    dataJSON = json.loads(responseJSON)

    # Debug: Affichage complet de dataJSON en cas d'absence des clés attendues
    if "metadata" not in dataJSON or "count" not in dataJSON["metadata"]:
        print("Erreur: Le JSON renvoyé par l'API ne contient pas la clé 'metadata' ou 'count'")
        print("Contenu de dataJSON :", json.dumps(dataJSON, indent=2))
        return 0  # ou lever une exception selon votre besoin

    # Extraction du nombre de brevets à partir des métadonnées
    nbre_brevets = dataJSON['metadata']['count']

    return (nbre_brevets)

def extract_patents_JSON(secrets: list, year: str, start: int, nb: int) -> dict:
    """
    Extrait les données JSON des brevets pour une année donnée, à partir d'une position
    et pour un nombre de résultats par itération.

    Args:
        secrets (list): Liste contenant les tokens de sécurisation.
        annee (str): Année ciblée.
        debut (int): Position de départ (offset) dans les résultats.
        nbre_par_iter (int): Nombre de résultats à récupérer.
    """

    xsrf_token, access_token, refresh_token = secrets[0], secrets[1], secrets[2]

    headers = {
        'Accept': 'application/json',
        'X-XSRF-TOKEN': xsrf_token,
        'Cookie': f'XSRF-TOKEN={xsrf_token}; access_token={access_token}; session_token={refresh_token}'
    }
    cookies = {
        'XSRF-TOKEN': xsrf_token,
        'access_token': access_token,
        'session_token': refresh_token
    }

    requete = f"[ABFR=(intelligence artificielle OU artificial intelligence)] ET [DEPD={year}]"
    data = {
        "collections": ["WO"],
        "query": requete,
        "fields": "document_key,PUBD,TIT,IPCR,INVNE,DENM",  # Champs retournés
        "position": start,  # Position de départ
        "size": nb  # Nombre de résultats à renvoyer
    }
    url_inpi_search = 'https://api-gateway.inpi.fr/services/apidiffusion/api/brevets/search'
    response = requests.post(url_inpi_search, json=data, headers=headers, cookies=cookies)
    responseJSON = response.content
    dataJSON = json.loads(responseJSON)
    return dataJSON



def getMetadataBrevet(secrets: list, idBrevet: str) -> str:
    """
    Récupère les métadonnées d'un brevet (au format XML) à partir de son identifiant.

    Args:
        secrets (list): Liste contenant xsrf_token, access_token, refresh_token.
        idBrevet (str): Identifiant du brevet.
    """

    xsrf_token, access_token, refresh_token = secrets[0], secrets[1], secrets[2]

    headers = {
        'Accept': 'application/xml',
        'X-XSRF-TOKEN': xsrf_token,
        'Cookie': f'XSRF-TOKEN={xsrf_token}; access_token={access_token}; session_token={refresh_token}'
    }

    urlNoticeBrevet = 'https://api-gateway.inpi.fr/services/apidiffusion/api/brevets/notice/pubnum/' + idBrevet
    response = requests.get(urlNoticeBrevet, headers=headers)
    return response.content  # Retourne le contenu XML


def getPatentInfo(secrets: list, id_brevet: str) -> dict:
    """
    Analyse la notice XML d'un brevet pour extraire plusieurs informations :
      - Numéro de brevet
      - Titre du brevet
      - Année de dépôt
      - Nom du déposant et pays du déposant
      - Liste des inventeurs (prénom, nom, et pays)
      - Abstract du brevet

    Les informations extraites seront renvoyées sous forme de dictionnaire.

    Args:
        secrets (list): Tokens d'accès à l'API INPI.
        id_brevet (str): Identifiant du brevet.
    """

    # Récupération et parsing de la notice XML
    notice = getMetadataBrevet(secrets, id_brevet)
    soup = BeautifulSoup(notice, 'xml')

    # Initialisation du dictionnaire de résultats
    patent_info = {}

    # Extraction du numéro de brevet
    doc_number = soup.find_all('fr-publication-reference')[1].find('doc-number').text
    patent_info["doc_number"] = doc_number

    # Extraction du titre du brevet
    try:
        invention_title = soup.find('invention-title').text
        patent_info["invention_title"] = invention_title
    except:
        patent_info["invention_title"] = None

    # Extraction de l'année de dépôt
    try:
        annee_depot = soup.find_all('fr-publication-reference')[0].find('document-id').find('date').text
        annee_depot = annee_depot[:4]
        patent_info["annee_depot"] = annee_depot
    except:
        patent_info["annee_depot"] = None

    # Extraction du nom du déposant de brevet
    try:
        applicant_name = soup.find_all('applicant')[1].find('last-name').text
        applicant_name = applicant_name.split(',')[0]
        patent_info["applicant_name"] = applicant_name
    except:
        patent_info["applicant_name"] = None

    """modif pour url"""
    # Extraction du nom du déposant de brevet
    try:
        applicant_name = soup.find_all('applicant')[1].find('last-name').text
        applicant_name = applicant_name.split(',')[0]
        patent_info["applicant_name"] = applicant_name
    except:
        patent_info["applicant_name"] = None

    # Extraction du pays du déposant de brevet
    try:
        applicant_country = soup.find_all('applicant')[0].find('country').text
        patent_info["applicant_country"] = applicant_country
    except:
        patent_info["applicant_country"] = None

    # Extraction de la liste des inventeurs (numéros impairs)
    try:
        inventors = soup.find_all('inventor')
        inventor_list = []
        for i in range(1, len(inventors), 2):
            inventor_last_name = inventors[i].find('last-name').text
            # On suppose que le format est "Nom,Prénom"
            parts = inventor_last_name.split(',')
            if len(parts) >= 2:
                nom_inventeur = parts[0].strip()
                prenom_inventeur = parts[1].strip()
            else:
                nom_inventeur = inventor_last_name.strip()
                prenom_inventeur = ""
            # Extraction du pays de l'inventeur (en utilisant l'inventor précédent dans la liste)
            inventor_country = inventors[i - 1].find('country').text
            # inventor_country = mondict[inventor_country]  # Décommenter si nécessaire
            inventor_info = {
                "prenom": prenom_inventeur,
                "nom": nom_inventeur,
                "inventor_country": inventor_country
            }
            inventor_list.append(inventor_info)
        patent_info["inventors"] = inventor_list
    except:
        patent_info["inventors"] = None

    # Extraction de l'abstract du brevet
    try:
        abstract = soup.find('abstract').find('p').text
        patent_info["abstract"] = abstract
    except:
        patent_info["abstract"] = None

    return patent_info


if __name__ == "__main__":
    # Récupération des secrets depuis les settings
    secrets = get_inpi_tokens()

    #Exemple du nb de brevets par an
    #n=nb_patents_by_year(secrets, "2020")
    #print(n)

    #"""
    data=extract_patents_JSON(secrets,"2020", 0, 10)
    print(data['results'])
    print(getPatentInfo(secrets, "EP3926551"))
    print(getMetadataBrevet(secrets, "EP3926551"))
    #"""

    """
    # Exemple des infos en JSON
    l=extract_patents_JSON(secrets, "2020", 0, 100)
    print(l['metadata'].keys())
    """

    """
    # Exemple d'analyse d'un brevet spécifique
    print("-----------------")
    print(getPatentInfo(secrets, "WO2007032122"))
    print("-----------------")
    print(getPatentInfo(secrets, "EP3926551"))
    """
