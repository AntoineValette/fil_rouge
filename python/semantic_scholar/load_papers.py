from rdflib import Graph, URIRef, Literal, Namespace, RDF

from python.semantic_scholar.semantic_functions.abstract import add_abstract_keywords
from python.semantic_scholar.semantic_functions.authors import add_authors, add_coauthors
from python.semantic_scholar.semantic_functions.fields import add_fields_primary, add_fields_secondary
from python.semantic_scholar.semantic_functions.paper_ids import add_external_ids
from python.semantic_scholar.semantic_functions.publication_date import add_publication_date
from python.semantic_scholar.semantic_functions.publication_venue import add_publication_venue
from python.util.insert_graph import insert_graph
from python.semantic_scholar.papers_query import get_data_JSON
from python.util.Namespaces import ONT, WD, WDT, RDFS, SKOS

def load_semantic_scholar(batch_size=5000, year=2020):
    # Create a new RDFlib Graph
    g = Graph()

    # Get JSON from Semantic Scholar
    papers = get_data_JSON(year)

    
    batch_count = 0  # Pour suivre le nombre de batches envoyés

    for i, p in enumerate(papers, start=1):
        paper_uri = URIRef(p["url"])  # L'URI du papier est son URL semantic scholar
        g.add((paper_uri, RDF.type, ONT.ScholarlyWork))  # paper est de type fabio:ScholarlyWork

        title = p["title"]
        g.add((paper_uri, ONT.title, Literal(title)))

        paper_id = p["paperId"]
        g.add((paper_uri, ONT.paperid, Literal(paper_id)))

        add_external_ids(paper_uri, p.get("externalId", {}), g)
        add_publication_venue(paper_uri, p.get("publicationVenue", {}), g)
        add_abstract_keywords(paper_uri, p.get("abstract"), g)

        add_authors(paper_uri, p["authors"], g)
        add_coauthors(paper_uri, p["authors"], g)

        add_publication_date(paper_uri, p.get("publicationDate", {}), g)
        add_fields_primary(paper_uri, p.get("fieldsOfStudy"), g)
        add_fields_secondary(paper_uri, p.get("s2FieldsOfStudy"), g)

        # 🛑 Quand on atteint le batch_size, on envoie à GraphDB et on vide la mémoire
        if i % batch_size == 0:
            insert_graph(g)  # Import du batch dans GraphDB
            print(f"📤 Batch {batch_count + 1} envoyé ({i} articles importés)")
            g = Graph()  # Réinitialise le graphe pour libérer la mémoire
            batch_count += 1

    # Importer les restants s'il y en a
    if len(g) > 0:
        insert_graph(g)
        print(f"📤 Dernier batch envoyé ({len(g)} articles restants)")

    print("✅ Importation terminée avec succès.")

if __name__ == "__main__":
    #load_semantic_scholar(batch_size=5000, year=2020)
    load_semantic_scholar(batch_size=5000, year=2021)
    load_semantic_scholar(batch_size=5000, year=2022)
    # load_semantic_scholar(batch_size=5000, year=2023)
    # load_semantic_scholar(batch_size=5000, year=2024)