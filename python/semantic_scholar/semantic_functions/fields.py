from rdflib import Graph, URIRef, Literal, Namespace, RDF
from python.util.Namespaces import ONT, WD, WDT, RDFS, SKOS

def add_fields_primary(paper_uri:URIRef, fields: [], g: Graph):
    if fields is not None:
        for field in fields:
            g.add((paper_uri, ONT.Domain, Literal(field)))

def add_fields_secondary(paper_uri:URIRef, fields: [], g: Graph):
    if fields is not None:
        for field in fields:
            g.add((paper_uri, ONT.Domain, Literal(field["category"])))