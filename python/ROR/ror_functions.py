import pandas as pd
from rdflib import URIRef, Graph, Namespace, RDF, OWL, Literal

from python.util.city_mapping import get_city_by_label_and_code2
from python.util.country_mapping import get_country_by_by_code_iso2
from python.util.Namespaces import ONT, WD, WDT, RDFS, SKOS

def create_orga(orga_uri: URIRef, types: str, g: Graph):
    #print(types)
    liste_type = [type.strip() for type in types.split(";")]
    for type in liste_type:
        if type=='healthcare':
            g.add((orga_uri, RDF.type, ONT.Healthcare))
        elif type=='archive':
            g.add((orga_uri, RDF.type, ONT.Archive))
        elif type=='company':
            g.add((orga_uri, RDF.type, ONT.Company))
        elif type=='education':
            g.add((orga_uri, RDF.type, ONT.School))
        elif type=='funder':
            g.add((orga_uri, RDF.type, ONT.Investor))
        elif type=='nonprofit':
            g.add((orga_uri, RDF.type, ONT.Nonprofit))
        elif type=='facility':
            g.add((orga_uri, RDF.type, ONT.Facility))
        elif type=='government':
            g.add((orga_uri, RDF.type, ONT.Government))
        elif type=='other':
            g.add((orga_uri, RDF.type, ONT.Other))

def add_domain(orga_uri: URIRef, domain: str, g: Graph):
    base="http://"
    if domain is not None and domain != "nan":
        domain_uri=URIRef(base+domain)
        g.add((domain_uri, RDF.type, ONT.Organization))
        g.add((orga_uri, OWL.sameAs, domain_uri))

def add_link(orga_uri: URIRef, link: str, g: Graph):
    if link is not None and link != "nan":
        link = link.replace("https://", "http://")
        link_uri = URIRef(link)
        g.add((link_uri, RDF.type, ONT.Organization))
        g.add((orga_uri, OWL.sameAs, link_uri))

def add_wikipedia(orga_uri: URIRef, wikipedia: str, g: Graph):
    if wikipedia is not None and wikipedia != "nan":
        wikipedia_uri=URIRef(wikipedia)
        g.add((wikipedia_uri, RDF.type, ONT.Organization))
        g.add((orga_uri, OWL.sameAs, wikipedia_uri))

def add_wikidata(orga_uri: URIRef, wikidata: str, g: Graph):
    if wikidata is not None and wikidata != "nan":
        base="https://www.wikidata.org/wiki/"
        wikidata_uri=URIRef(str(base+wikidata))
        g.add((wikidata_uri, RDF.type, ONT.Organization))
        g.add((orga_uri, OWL.sameAs, wikidata_uri))

def add_website(orga_uri: URIRef, website: str, g: Graph):
    if website is not None and website != "nan":
        website_uri=URIRef(website)
        g.add((website_uri, RDF.type, ONT.Organization))
        g.add((orga_uri, OWL.sameAs, website_uri))

def add_country(uri:URIRef, country_code: str, g: Graph, mapping_country: pd.DataFrame):
    if country_code is not None and not pd.isna(country_code) and country_code not in ["nan", "None"]:
        try:
            country = get_country_by_by_code_iso2(mapping_country, country_code)
            country_uri = URIRef(country)
            g.add((uri, ONT.isLocalizedIn, country_uri))
        except Exception as e:
            #print(f"the country code {country_code} was not found in the mapping")
            a=1

def add_city(uri:URIRef, city:str, country_code: str, g: Graph, mapping_city: pd.DataFrame):
    if city is not None and not pd.isna(city) and city not in ["nan", "None"]:
        try:
            city_ = get_city_by_label_and_code2(mapping_city, city, country_code)
            city_uri = URIRef(city_)
            g.add((uri, ONT.isLocalizedIn, city_uri))
        except Exception as e:
            #print(f"the city {city} in {country_code} was not found in the mapping")
            a=1
            #puique le mapping marche pas bien, on place la ville dans une dataproperty en plus
            g.add((uri, ONT.cityName, Literal(city)))

def add_name(uri:URIRef, name: str, g: Graph):
    if name is not None :
        g.add((uri, SKOS.prefLabel, Literal(name)))


def get_relations_to_dict(s: str) -> dict:
    """
    Convertit une chaîne structurée contenant des listes séparées par des points-virgules
    en un dictionnaire de listes.

    Exemple:
    "child : child1, child2, child3; parent : parent1, parentX ; related : name1, name2, nameY"
    retourne:
    {'child': ['child1', 'child2', 'child3'],
     'parent': ['parent1', 'parentX'],
     'related': ['name1', 'name2', 'nameY']}
    """
    result = {}
    # Sépare la chaîne en parties grâce au point-virgule.
    parts = s.split(";")
    for part in parts:
        # Vérifie qu'il y a bien un deux-points dans la partie
        if ":" in part:
            key, values = part.split(":", 1)
            key = key.strip()  # Enlève les espaces inutiles
            # Sépare les valeurs par la virgule et retire les espaces
            values_list = [v.strip() for v in values.split(",") if v.strip()]
            result[key] = values_list
    return result


def add_relations(uri: URIRef, relations: str, g: Graph):
    """
    Ajoute des relations dans le graphe RDF à partir d'une chaîne de relations.
    Les relations attendues sont 'child', 'parent' et 'related'.
    """
    if relations is not None and not pd.isna(relations):
        relations_dict = get_relations_to_dict(relations)
        #print(relations_dict.keys())

        # Ajoute les relations "child"
        for child in relations_dict.get('child', []):
            child_uri = URIRef(str(child))
            g.add((uri, ONT.hasChild, child_uri))

        # Ajoute les relations "parent"
        for parent in relations_dict.get('parent', []):
            parent_uri = URIRef(str(parent))
            g.add((uri, ONT.hasParent, parent_uri))

        # Ajoute les relations "related"
        for related in relations_dict.get('related', []):
            related_uri = URIRef(str(related))
            g.add((uri, ONT.relatedTo, related_uri))

if __name__ == "__main__":
    s = "child : child1, child2, child3; parent : parent1, parentX ; related : name1, name2, nameY"
    print(get_relations_to_dict(s))