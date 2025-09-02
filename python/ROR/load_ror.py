from rdflib import Graph, URIRef, Namespace, RDF
import pandas as pd

from python.ROR.ror_functions import create_orga, add_wikipedia, add_wikidata, add_website, add_country, add_city, \
    add_name, add_domain, add_relations
from python.geonames.mapping import create_mapping_from_graphdb, match_country, match_city, build_city_dicts, build_country_dict
from python.util.insert_graph import insert_graph
from python.util.Namespaces import ONT, WD, WDT, RDFS, SKOS


def load_ror(file_path:str):
    chunk_size = 1000  # nombre de lignes par chunk
    chunk_nb=0

    mapping=create_mapping_from_graphdb("iso2") #dataframe pour trouver URI d'une ville à partir de son nom et du code pays
    country_dict = build_country_dict(mapping, "iso2")
    official_dict, alternate_dict = build_city_dicts(mapping)

    # Lecture du CSV par chunks
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        # Créer un nouveau graphe pour chaque chunk
        g = Graph()
        for index, row in chunk.iterrows():
            # URI de l'organisation basée sur son ID
            orga_uri = URIRef(row['id'])
            if orga_uri is not None and orga_uri != "nan":
                create_orga(orga_uri, row['types'], g)

                #add domain, wikipedia, wikidata, website,
                add_domain(orga_uri, str(row['domains']), g)
                add_wikipedia(orga_uri, str(row['links.type.wikipedia']),g)
                add_wikidata(orga_uri, str(row['external_ids.type.wikidata.preferred']), g)
                #add_website(orga_uri, str(row['links.type.website']), g)

                # ajout du pays (classe)
                country = match_country(country_dict, row['locations.geonames_details.country_code'])
                if country:
                    country_uri = URIRef(country)
                    g.add((orga_uri, ONT.inCountry, country_uri))

                # ajout de la ville (classe)
                city = match_city(official_dict, alternate_dict, row['locations.geonames_details.name'], country)
                if city:
                    city = URIRef(city)
                    g.add((orga_uri, ONT.inCity, city))
                
                #labels
                add_name(orga_uri, row['names.types.ror_display'], g)

                #child/parent/related
                add_relations(orga_uri, row['relationships'],g)

                #print(f"Organization ROR added to local graph: {orga_uri} ---  {domain_uri} --- {linkedin_uri}")

        # Insérer le graphe du chunk dans GraphDB
        insert_graph(g)
        print(f"[ORGANIZATIONS] local graph of chunck {chunk_nb} added to GraphDB")
        chunk_nb += 1

    print("[ORGANIZATIONS] all chunks of organization added to GraphDB")


if __name__ == "__main__":
    load_ror("../../ROR/v1.60-2025-02-27-ror-data_schema_v2.csv")




"""
'id', 'admin.created.date', 'admin.created.schema_version',
'admin.last_modified.date', 'admin.last_modified.schema_version',
'domains', 'established', 'external_ids.type.fundref.all',
'external_ids.type.fundref.preferred', 'external_ids.type.grid.all',
'external_ids.type.grid.preferred', 'external_ids.type.isni.all',
'external_ids.type.isni.preferred', 'external_ids.type.wikidata.all',
'external_ids.type.wikidata.preferred', 'links.type.website',
'links.type.wikipedia', 'locations.geonames_id',
'locations.geonames_details.continent_code',
'locations.geonames_details.continent_name',
'locations.geonames_details.country_code',
'locations.geonames_details.country_name',
'locations.geonames_details.country_subdivision_code',
'locations.geonames_details.country_subdivision_name',
'locations.geonames_details.lat', 'locations.geonames_details.lng',
'locations.geonames_details.name', 'names.types.acronym',
'names.types.alias', 'names.types.label', 'names.types.ror_display',
'ror_display_lang', 'relationships', 'status', 'types'
"""
