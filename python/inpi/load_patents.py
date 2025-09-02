from rdflib import Graph, URIRef, Namespace, RDF, Literal

from python.inpi.patent_functions import normalize_string, add_title, add_applicant, add_inventors, add_abstract
from python.inpi.patents_query import nb_patents_by_year, extract_patents_JSON, getPatentInfo
from python.geonames.mapping import create_mapping_from_graphdb, build_country_dict
from python.inpi.token_manager2 import get_inpi_tokens
from python.util.check_uri import clean_and_encode_uri, is_valid_uri
from python.util.insert_graph import insert_graph
from python.util.Namespaces import ONT, WD, WDT, RDFS, SKOS

Base_url="http://inpi.fr/brevets/"

def load_patents_by_year(secrets: list, annee: str):
    """
    Traite les brevets pour une année donnée.
    - Récupère le nombre total de brevets.
    - Parcourt les brevets par itération (pagination) et pour chaque brevet,
      extrait et analyse les informations via la fonction analyseXmlNotice.

    Args:
        secrets (list): Liste des tokens pour l'API INPI.
        annee (str): Année pour laquelle traiter les brevets.
    """

    total_brevets = nb_patents_by_year(secrets, annee)
    resultats_par_iteration = 10
    iter=0

    mapping = create_mapping_from_graphdb("iso2") #dataframe pour trouver URI d'une ville à partir de son nom et du code pays
    country_dict = build_country_dict(mapping, "iso2")

    for i in range(0, total_brevets, resultats_par_iteration):
        g = Graph()
        data_JSON = extract_patents_JSON(secrets, annee, i, resultats_par_iteration)

        # Pour chaque brevet récupéré, extraire les informations
        for result in data_JSON['results']:
            id_brevet = result['documentId']
            #print(id_brevet)
            if id_brevet is not None:
                patentInfo=getPatentInfo(secrets, id_brevet)

                #add URI patent
                #print(patentInfo['doc_number'])
                patent_uri=(Base_url+patentInfo['doc_number'])
                patent_uri=URIRef(clean_and_encode_uri(patent_uri))
                if is_valid_uri(patent_uri):
                    g.add((patent_uri, RDF.type, ONT.Patent))
                    print(f"patent with URI {patent_uri} added to local graph")

                    #add title
                    add_title(patent_uri, patentInfo['invention_title'], g)

                    #add applicant_URI
                    add_applicant(patent_uri, patentInfo['applicant_name'], g, country_dict, patentInfo['applicant_country'])

                    #add inventors
                    add_inventors(patent_uri, patentInfo['inventors'], g, country_dict)

                    #add abstract
                    add_abstract(patent_uri, patentInfo['abstract'], g)
                else:
                    print(f"patent {patent_uri} is invalid")

        # Insérer le graphe du chunk dans GraphDB
        insert_graph(g)
        print(f"[PATENTS] local graph of iter {iter} added to GraphDB")
        iter+=1

    print(f"[PATENTS] all iters of patents added to GraphDB for year {annee}")


if __name__ == "__main__":
    # Récupération des secrets depuis les settings
    secrets = get_inpi_tokens()
    load_patents_by_year(secrets, "2020")
    load_patents_by_year(secrets, "2021")
    load_patents_by_year(secrets, "2022")
    #load_patents_by_year(secrets, "2023")
    #load_patents_by_year(secrets, "2024")

