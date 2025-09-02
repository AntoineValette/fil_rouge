from rdflib import Graph, URIRef, Namespace, RDF
import pandas as pd

from python.geonames.mapping import create_mapping_from_graphdb, match_country, match_city, build_city_dicts, build_country_dict
from python.crunchbase.orga_people_functions.geography_functions import add_region, add_linkedin
from python.crunchbase.orga_people_functions.orga_functions import add_name, add_description, add_primary_role, \
    add_domain
from python.util.insert_graph import insert_graph
from python.util.Namespaces import ONT, WD, WDT, RDFS, SKOS

def load_organizations(file_path:str):
    base_orga = "https://www.crunchbase.com/organization/"
    base_domain = "https://"

    chunk_size = 1000  # nombre de lignes par chunk
    chunk_nb=0

    mapping=create_mapping_from_graphdb("iso3") #dataframe pour trouver URI d'une ville à partir de son nom et du code pays
    country_dict = build_country_dict(mapping, "iso3")
    official_dict, alternate_dict = build_city_dicts(mapping)


    # Lecture du CSV par chunks
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        # Créer un nouveau graphe pour chaque chunk
        g = Graph()
        for index, row in chunk.iterrows():

            # URI de l'organisation basée sur son UUID
            orga_uri = URIRef(base_orga + row['uuid'])
            # primary_role : company, investor, school
            add_primary_role(orga_uri, row['primary_role'], g)

            # URI du domaine de l'organisation
            domain_uri=add_domain(orga_uri, row['domain'], g)

            # ajout du name et de la description
            add_name(orga_uri, row['name'], g)
            add_description(orga_uri, row['short_description'], g)

            # ajout de la region (dataproperty)
            add_region(orga_uri, row['region'],g)

            # ajout du pays (classe)
            country = match_country(country_dict, row['country_code'])
            if country:
                country_uri = URIRef(country)
                g.add((orga_uri, ONT.inCountry, country_uri))

            # ajout de la ville (classe)
            city = match_city(official_dict, alternate_dict, row['city'], country)
            if city:
                city = URIRef(city)
                g.add((orga_uri, ONT.inCity, city))

            #print(f"Company added to local graph: {orga_uri} ---  {domain_uri} --- {linkedin_uri}")

        # Insérer le graphe du chunk dans GraphDB
        insert_graph(g)
        print(f"[ORGANIZATIONS] local graph of chunck {chunk_nb} added to GraphDB")
        chunk_nb += 1

    print("[ORGANIZATIONS] all chunks of organization added to GraphDB")


if __name__ == "__main__":
    load_organizations("../../crunchbase/organizations.csv")