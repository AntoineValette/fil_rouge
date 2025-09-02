import pandas as pd
from rdflib import URIRef, Graph, Namespace, Literal, RDF
from python.geonames.mapping import match_country

from python.util.Namespaces import ONT, WD, WDT, RDFS, SKOS
from python.util.check_uri import clean_and_encode_uri, is_valid_uri

Base_url="http://inpi.fr/"


def add_title(patent_uri:URIRef, title:str, g: Graph):
    """ajoute titre title du brevet qui a pour URIpatent_uri au graph g """
    #print(title)
    if title is not None:
        g.add((patent_uri, ONT.title, Literal(title)))
        #print(f"{patent_uri} ----- {title}")


def add_applicant(patent_uri: URIRef, applicant_name:str, g: Graph, country_dict, applicant_country):
    """
    ajoute le sponsor du brevet qui a pour URI patent_uri au graph g
    créer un URI fictif pour le sponsor
    ajoute les data properties (name via soks:prefLabel) au graph g
    ajoute l'objectProperty isLocalizedIn (du pays) au graph g grâce à maaping_country
    """
    # print(applicant_name)
    # print(applicant_country)
    if applicant_name is not None:
        applicant = normalize_string(applicant_name)
        applicant_uri = (Base_url + applicant)
        """pas d'id pour les applicants, donc on en fabrique un"""
        applicant_uri = URIRef(clean_and_encode_uri(applicant_uri))
        if is_valid_uri(applicant_uri):
            g.add((applicant_uri, RDF.type, ONT.Organization))
            print(f"applicant with URI {applicant_uri} added to local graph")

            # relation entre un brevet et une company/orga
            g.add((patent_uri, ONT.hasSponsor, applicant_uri))

            # add applicant_name
            g.add((applicant_uri, SKOS.prefLabel, Literal(applicant_name)))

            if applicant_country is not None:
                country = match_country(country_dict, applicant_country)
                country_uri = URIRef(country)
                g.add((applicant_uri, ONT.inCountry, country_uri))
        else:
            print(f"applicant {applicant_uri} is invalid")


def add_inventors(patent_uri: URIRef, inventors:[], g: Graph, country_dict):
    """
    ajoute les inventors du brevet qui a pour URI patent_uri au graph g
    créé un URI fictif pour les inventors
    ajoute les data properties (first name, last name, prefLabel) au graph g
    ajoute l'objectProperty isLocalizedIn (du pays) au graph g grâce à maaping_country
    """
    if inventors is not None:
        for i in inventors:
            inventor = normalize_string(i['prenom'] + i['nom'])
            if inventor is not None and inventor != "":
                inventor_uri = (Base_url + inventor)
                inventor_uri = URIRef(clean_and_encode_uri(inventor_uri))
                if is_valid_uri(inventor_uri):
                    """pas d'id pour les inventors, donc on en fabrique un"""
                    g.add((inventor_uri, RDF.type, ONT.Inventor))
                    print(f"inventor with URI {inventor_uri} added to local graph")

                    #lien entre inventor et brevet
                    g.add((inventor_uri, ONT.isInventorOf, patent_uri))

                    # first name, last name, prefLabel
                    # print(f"first name : {i['prenom']}, last name : {i['nom']}")
                    if i['prenom'] is not None and i['nom'] != "":
                        g.add((inventor_uri, ONT.firstName, Literal(i['prenom'])))
                    if i['nom'] is not None and i['nom'] != "":
                        g.add((inventor_uri, ONT.lastName, Literal(i['nom'])))
                    if (i['prenom'] is not None and i['nom'] != "") or (i['nom'] is not None and i['nom'] != ""):
                        g.add((inventor_uri, SKOS.prefLabel, Literal(i['prenom'] + " " + i['nom'])))

                    if i['inventor_country'] is not None and i['inventor_country'] != "":
                        country = match_country(country_dict, i['inventor_country'])
                        country_uri = URIRef(country)
                        g.add((inventor_uri, ONT.inCountry, country_uri))
                else:
                    print(f"inventor {inventor_uri} is invalid")


def add_abstract(patent_uri: URIRef, abstract:str, g: Graph):
    """ajoute l'abstract du brevet qui a pour URI patent_uri au graph g"""
    #print(abstract)
    if abstract is not None:
        g.add((patent_uri, ONT.abstract, Literal(abstract)))



def normalize_string(s: str) -> str:
    """fonction utilisée pour créer des URI fictifs pour applicants et inventors"""
    # "split()" divise la chaîne par tous les espaces (y compris les tabulations, retours à la ligne, etc.)
    # puis "join" reconstruit la chaîne sans espaces
    return "".join(s.split()).lower()



if __name__ == "__main__":
    # Exemple d'utilisation
    exemple = " Bonjour le Monde! "
    print(normalize_string(exemple))  # Affichera "bonjourlemonde!"