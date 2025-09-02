from rdflib import Graph, URIRef, Literal, Namespace, RDF
from python.util.Namespaces import ONT, WD, WDT, RDFS, SKOS


def add_abstract_keywords(paper_uri:URIRef, abstract: str, g: Graph):
    if abstract is not None:
        g.add((paper_uri, ONT.abstract, Literal(abstract)))

        """
        ici, il faudra ajouter un module pour déterminer des mots clés
        """