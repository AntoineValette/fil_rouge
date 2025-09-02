import pandas as pd
from rdflib import Graph, URIRef, Literal, Namespace, OWL

#from python.util.city_mapping import get_city_by_label_and_code3
#from python.util.country_mapping import get_country_by_by_code_iso3
from python.util.check_uri import clean_and_encode_uri, is_valid_uri
from python.util.Namespaces import ONT, WD, WDT, RDFS, SKOS


def add_region(uri:URIRef, region: str, g: Graph):
    if region is not None:
        g.add((uri, ONT.region, Literal(region)))


"""
def add_country(uri:URIRef, country_code: str, g: Graph, mapping_country: pd.DataFrame):
    if country_code is not None and not pd.isna(country_code) and country_code not in ["nan", "None"]:
        try:
            country = get_country_by_by_code_iso3(mapping_country, country_code)
            country_uri = URIRef(country)
            g.add((uri, ONT.isLocalizedIn, country_uri))
        except Exception as e:
            #print(f"the country code {country_code} was not found in the mapping")
            a=1


def add_city(uri:URIRef, city:str, country_code: str, g: Graph, mapping_city: pd.DataFrame):
    if city is not None and not pd.isna(city) and city not in ["nan", "None"]:
        try:
            city_ = get_city_by_label_and_code3(mapping_city, city, country_code)
            city_uri = URIRef(city_)
            g.add((uri, ONT.isLocalizedIn, city_uri))
        except Exception as e:
            #print(f"the city {city} in {country_code} was not found in the mapping")
            a=1

        #puique le mapping marche pas bien, on place la ville dans une dataproperty en plus
        g.add((uri, ONT.cityName, Literal(city)))
"""

def add_linkedin(uri: URIRef, linkedin: str, g: Graph) -> str:
    """initialement, on ajoutait les linkedin des orga et des personnes,
    mais bcp d'orga ont le linkedin de leur fondateur,
    onc ça donne des orga sameAs des personnes
    ==> mettre le linkedin pour les personnes uniquement OU rajouter une règle pour verifier que le linkedin est celui d'une personne ou d'une orga"""
    try:
        if linkedin:
            # Nettoyage et encodage de l'URL Linkedin
            cleaned_linkedin_url = clean_and_encode_uri(linkedin)
            linkedin_uri = URIRef(cleaned_linkedin_url)
            # Vérification de la validité de l'URI
            if is_valid_uri(linkedin_uri):
                g.add((uri, OWL.sameAs, linkedin_uri))
                return str(linkedin_uri)
            else:
                # L'URI nettoyé n'est pas valide
                return ""
        else:
            return ""
    except Exception as e:
        # En cas d'erreur, on peut loguer l'exception ici (ex: logging.error(...))
        # print(f"Erreur lors du traitement de l'URL Linkedin '{linkedin}': {e}")
        return ""
