from rdflib import Graph
import requests

def insert_graph(g: Graph):
    # Serialize the graph to Turtle format
    turtle_data = g.serialize(format="turtle")

    # Build the SPARQL INSERT DATA query using the Turtle data
    # Note: The Turtle data already contains valid RDF statements,
    # so we wrap it in an INSERT DATA {} clause.
    sparql_update = f"""
    INSERT DATA {{
    {turtle_data}
    }}
    """

    graphdb_endpoint = "http://localhost:7200/repositories/Fil_Rouge_DB/statements"
    headers = {"Content-Type": "application/sparql-update"}

    # Send the SPARQL update request to GraphDB
    response = requests.post(graphdb_endpoint, data=sparql_update.encode("utf-8"), headers=headers)

    if response.status_code != 204:
        print(response.status_code)
        print(response.text)
    else:
     print("[insert_graph] sparql query inserted")