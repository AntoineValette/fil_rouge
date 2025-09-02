from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, URIRef, Literal
from python.util.Namespaces import ONT, WD, WDT, RDFS, SKOS
from python.util.insert_graph import insert_graph
from mistralai import Mistral
from dotenv import load_dotenv
import os
import time

# Charge automatiquement le .env dans le répertoire courant
load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")
model = "mistral-small-latest"

client = Mistral(api_key=api_key)

# Endpoint GraphDB
GRAPHDB_ENDPOINT = "http://localhost:7200/repositories/Fil_Rouge_DB"

def add_keywords(query):

    g = Graph()

    # Préparation de la requête SPARQL qui récupère, de manière distincte,
    # l'URI de l'entreprise et la latitude et longitude de la ville associée.
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    sparql.addParameter("sameAs", "false")
    results = sparql.query().convert()

    result = results['results']['bindings']

    for i in result:
        entity_uri = URIRef(i['s']['value'])
        description = i['o']['value']
        chat_response = client.chat.complete(
            model = model,
            messages = [
                {
                    "role": "user",
                    "content": f"Determine a list of exactly 5 keywords and nothing else, separated by comas, that describe the company's activity and sector, including terms related to technology and computing, based on this text : {description}",
                },
            ]
        )
        keywords = chat_response.choices[0].message.content
        keywords_list = [kw.strip() for kw in keywords.split(',')]
        print(keywords_list)
        for y in keywords_list:
            g.add((entity_uri, ONT.hasKeyWord, Literal(y)))
        time.sleep(2)

    insert_graph(g)
    print('graph added')


if __name__ == "__main__":
    query_company = """
    PREFIX ns1: <http://www.semanticweb.org/fil_rouge_AntoineValette_GuillaumeRamirez/>

    select * where {
        ?s a ns1:Company .
        ?s ns1:description ?o .
    } limit 10
    """
    query_article = """
    PREFIX ns1: <http://www.semanticweb.org/fil_rouge_AntoineValette_GuillaumeRamirez/>
    
    select * where {
        ?s a ns1:ScholarlyWork .
        ?s ns1:abstract ?o .
    } limit 10
    """
    add_keywords(query_company)
    add_keywords(query_article)