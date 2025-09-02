from SPARQLWrapper import SPARQLWrapper, POST
import sys

# Endpoint
GRAPHDB_ENDPOINT = "http://localhost:7200/repositories/Fil_Rouge_DB/statements"

def clear_objects_by_type(object_type):
    """
    Supprime tous les objets d'un certain type donné.
    :param object_type: URI du type des objets à supprimer (ex: 'ex:exemple')
    """
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)
    query = f"""
    DELETE WHERE {{
        ?s a <{object_type}> ; ?p ?o .
    }}
    """
    sparql.setQuery(query)
    sparql.setMethod(POST)

    try:
        sparql.query()
        print(f"All objects of type {object_type} have been successfully deleted from the database.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python clear_object.py <object_type>")
        sys.exit(1)
    
    object_type = sys.argv[1]
    clear_objects_by_type(object_type)
