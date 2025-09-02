from SPARQLWrapper import SPARQLWrapper, POST

# Endpoint
GRAPHDB_ENDPOINT = "http://localhost:7200/repositories/Fil_Rouge_DB/statements"


def clear_all_triples():
    """
    pour vider la BDD de GraphDB
    """
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)
    # To delete all triples from all graphs:
    sparql.setQuery("CLEAR ALL")
    # Clear only the default graph, use:
    # sparql.setQuery("CLEAR DEFAULT")

    sparql.setMethod(POST)

    try:
        sparql.query()
        print("All triples have been successfully deleted from the database.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    """
    pour vider la BDD de GraphDB - SUPPRESSION définitive
    """
    clear_all_triples()