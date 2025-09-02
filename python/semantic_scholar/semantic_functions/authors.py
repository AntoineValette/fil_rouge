from rdflib import Graph, URIRef, Literal, Namespace, RDF
import json

import requests
from python.util.Namespaces import ONT, WD, WDT, RDFS, SKOS

def add_authors(paper_uri:URIRef, authors: [], g: Graph):
    """
    ajoute les auteurs au graphe
    """
    list_ids=[] #on fabrique une liste des id des auteurs
    if authors is not None:
        for author in authors:
            authorID=author["authorId"]
            name=author["name"]
            #print(name)

            base_URL="https://www.semanticscholar.org/author/"
            author_uri = URIRef(base_URL + str(authorID))

            g.add((author_uri, RDF.type, ONT.Researcher))
            g.add((author_uri, SKOS.prefLabel, Literal(name)))

            g.add((author_uri, ONT.isAuthorOf, paper_uri))

        """faudrait rajouter un module pour récupérer les ORCID"""


def add_coauthors(paper_uri:URIRef, authors: [], g: Graph):
    base_URL = "https://www.semanticscholar.org/author/"
    if authors is not None:
        for i in range(0,len(authors)):
            IDi=authors[i]["authorId"]
            URIi=URIRef(base_URL + str(IDi))
            for j in range(i+1,len(authors)):
                IDj=authors[j]["authorId"]
                URIj=URIRef(base_URL + str(IDj))
                g.add((URIi, ONT.coauthor, URIj))
