from rdflib import Graph, URIRef, Literal, Namespace, RDF
from datetime import datetime
from python.util.Namespaces import ONT, WD, WDT, RDFS, SKOS


def add_publication_date(paper_uri:URIRef, date: str, g: Graph):
    if date is not None:
        publicationDate = datetime.strptime(date, "%Y-%m-%d")
        g.add((paper_uri, ONT.publicationDate, Literal(publicationDate)))