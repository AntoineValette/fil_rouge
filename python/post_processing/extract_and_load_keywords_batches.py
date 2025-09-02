import json
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, URIRef, Literal
from python.util.Namespaces import ONT, WD, WDT, RDFS, SKOS
from python.util.insert_graph import insert_graph
from mistralai import Mistral
from dotenv import load_dotenv
import os
import time
import re

# Charge automatiquement le .env dans le répertoire courant
load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")
model = "mistral-small-latest"
client = Mistral(api_key=api_key)

# Endpoint GraphDB
GRAPHDB_ENDPOINT = "http://localhost:7200/repositories/Fil_Rouge_DB"

def add_keywords_in_batches(query, batch_size=50):
    g = Graph()
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    sparql.addParameter("sameAs", "false")
    results = sparql.query().convert()
    result = results['results']['bindings']

    # Traitement par lots
    for batch_start in range(0, len(result), batch_size):
        batch = result[batch_start:batch_start + batch_size]
        uris = []
        descriptions = []
        for item in batch:
            uris.append(URIRef(item['s']['value']))
            descriptions.append(item['o']['value'])

        # Création du prompt avec le séparateur " ||| " et mise en forme pour un output JSON
        # Chaque description est entourée de guillemets pour plus de clarté.
        joined_descriptions = " ||| ".join([f'"{desc}"' for desc in descriptions])
        print(joined_descriptions)
        prompt = (f"""
            For each description between quotes and separated by ' ||| ', determine a list of exactly 5 keywords and nothing else,
            separated by commas, that describe the company's activity and sector or the article's subject of research, including terms related to technology and computing.
            Please output the result as a JSON array of arrays, where each inner array corresponds to the keywords for each description in order.\n\n
            {joined_descriptions}
            """
        )

        # Appel au LLM pour le batch courant
        chat_response = client.chat.complete(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        print(chat_response.choices[0].message.content)

        # Nettoyage initial de la réponse
        response_text = chat_response.choices[0].message.content.strip()

        # Extraction de la partie JSON en utilisant une expression régulière
        match = re.search(r'(\[.*\])', response_text, re.DOTALL)
        if match:
            json_str = match.group(1)
        else:
            json_str = response_text

        # Tentative de décodage du JSON
        try:
            keywords_lists = json.loads(json_str)
        except Exception as e:
            print("Erreur lors du parsing du JSON:", e)
            print("Contenu de la réponse extraite:", json_str)
            continue

        print(keywords_lists)

        # Vérification que le nombre de listes obtenues correspond au nombre de descriptions
        if len(keywords_lists) != len(uris):
            print("Nombre de résultats différent du nombre de descriptions dans le batch")
            continue

        # Association des mots clés à chaque URI
        for uri, keywords in zip(uris, keywords_lists):
            for keyword in keywords:
                g.add((uri, ONT.hasKeyWord, Literal(keyword)))

        # Pause pour éviter un appel trop rapide
        time.sleep(1.2)

    print(g)

    insert_graph(g)
    print('Graph added')

if __name__ == "__main__":
    query_company = """
    PREFIX ns1: <http://www.semanticweb.org/fil_rouge_AntoineValette_GuillaumeRamirez/>

    SELECT * WHERE {
        ?s a ns1:Company .
        ?s ns1:description ?o .
    } LIMIT 100
    """
    query_article = """
    PREFIX ns1: <http://www.semanticweb.org/fil_rouge_AntoineValette_GuillaumeRamirez/>
    
    SELECT * WHERE {
        ?s a ns1:ScholarlyWork .
        ?s ns1:abstract ?o .
    } LIMIT 100
    """
    add_keywords_in_batches(query_company, batch_size=50)
    add_keywords_in_batches(query_article, batch_size=50)