from rdflib import Graph, URIRef, Literal, Namespace, RDF, OWL

from python.util.check_uri import clean_and_encode_uri, is_valid_uri
from python.util.Namespaces import ONT, WD, WDT, RDFS, SKOS


def add_name(orga_uri:URIRef, name: str, g: Graph):
    if name is not None:
        g.add((orga_uri, SKOS.prefLabel, Literal(name)))


def add_description(orga_uri:URIRef, description: str, g: Graph):
    if description is not None:
        g.add((orga_uri, ONT.description, Literal(description)))


def add_primary_role(orga_uri: URIRef, role: str, g: Graph):
    if role is not None:
        if role == "company":
            g.add((orga_uri, RDF.type, ONT.Company))
        elif role == "investor":
            g.add((orga_uri, RDF.type, ONT.Investor))
        elif role == "school":
            g.add((orga_uri, RDF.type, ONT.School))
        else :
            print("error : the crunchbase organization does not have a clearly defined role")


def add_domain(orga_uri: URIRef, domain: str, g: Graph):
    if domain is not None:
        base_domain = "http://"
        cleaned_domain_url = clean_and_encode_uri(base_domain + str(domain))
        domain_uri = URIRef(cleaned_domain_url)
        if is_valid_uri(domain_uri):
            g.add((domain_uri, RDF.type, ONT.Organization))
            # Indiquer que les deux URI réfèrent à la même ressource
            g.add((orga_uri, OWL.sameAs, domain_uri))
        else:
            #print(f"{domain_uri} is not a valid URI")
            domain_uri = ""
    else :
        domain_uri = ""
    return domain_uri



