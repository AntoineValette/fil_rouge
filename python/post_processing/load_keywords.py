from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, Namespace,Literal, URIRef

from python.post_processing.extract_keywords import extract_keywords
from python.util.insert_graph import insert_graph
from python.util.Namespaces import ONT, WD, WDT, RDFS, SKOS

def get_abstracts():
    # URL of the GraphDB SPARQL endpoint
    sparql_endpoint = "http://localhost:7200/repositories/Fil_Rouge_DB"
    sparql = SPARQLWrapper(sparql_endpoint)

    query = """
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX : <http://www.semanticweb.org/guillaumeramirez/ontologies/2024/11/resaerchandstartups/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    
    SELECT DISTINCT ?paper ?abstract
    WHERE {
        ?paper dcterms:abstract ?abstract .
    }
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    sparql.setMethod('POST')

    # Set Accept header to request JSON results
    sparql.addCustomHttpHeader("Accept", "application/sparql-results+json")

    try:
        results = sparql.query().convert()
        nb = len(results["results"]["bindings"])
        print(f"nb lignes trouvées par la requete : {nb}")
    except Exception as e:
        print("An error occurred:", e)


    return results["results"]["bindings"]

if __name__ == "__main__":
    list = get_abstracts()

    for result in list:
        # Create a new RDFlib Graph
        g = Graph()

        paper = URIRef(result["paper"]["value"])
        abstract = result["abstract"]["value"]
        keywords = extract_keywords(abstract)

        #print(f"Paper: {paper}\nAbstract: {abstract}\n")
        #print(f"Keywords: {keywords}")

        for keyword in keywords:
            g.add((paper, ONT.keyword, Literal(keyword)))

        # insertion dans graph
        insert_graph(g)
        print(f"ajout de keywords for URI :{paper}")

