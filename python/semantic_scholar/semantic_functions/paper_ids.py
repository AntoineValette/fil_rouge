from rdflib import Graph, URIRef, Literal, Namespace, RDF
from python.util.Namespaces import ONT, WD, WDT, RDFS, SKOS

def add_external_ids(paper_uri:URIRef, external_ids:dict, g: Graph):
    if external_ids is not None:
        if external_ids.get("DOI") is not None:
            DOI=external_ids["externalIds"]["DOI"]
            g.add((paper_uri, ONT.doi, Literal(DOI)))

        if external_ids.get("CorpusId") is not None:
            CorpusId=external_ids["CorpusId"]
            g.add((paper_uri, ONT.corpusid, Literal(DOI)))

        if external_ids.get("DBLP") is not None:
            DBLP=external_ids["DBLP"]
            g.add((paper_uri, ONT.DBLP, Literal(DBLP)))

        if external_ids.get("MAG") is not None:
            MAG=external_ids["MAG"]
            g.add((paper_uri, ONT.MAG, Literal(MAG)))