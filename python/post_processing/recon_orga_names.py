import re
from rdflib import Graph, URIRef, OWL

from python.util.insert_graph import insert_graph
from python.util.query_graphDB import sparql_to_dict
from python.util.Namespaces import ONT, WD, WDT, RDFS, SKOS


def recon_orga(data: dict):
    """
    Parcourt le dictionnaire contenant les résultats (avec la clé "rows")
    et, pour chaque organisation, compare son nom (clé "name1") avec ceux des autres organisations.
    - Compare avec une égalité stricte (après normalisation).
    - Compare si le nom apparaît comme un mot complet dans le nom d'une autre organisation.
    Les messages sont affichés et écrits dans le fichier "output_reco_orga.txt".
    """

    with open("output_reco_orga.txt", "w", encoding="utf-8") as f:
        rows = data.get("rows", [])
        g = Graph()

        # Parcourir chaque organisation dans les lignes du dictionnaire
        for idx, row in enumerate(rows):
            current_name = row['name1']
            current_norm = current_name.strip().lower()  # Normalisation pour la comparaison stricte
            current_uri = row['org1']
            found_strict = False
            found_regex = False

            # Construction du motif regex pour vérifier si current_name apparaît comme un mot complet
            # (^|\s) : début de chaîne ou espace avant, ($|\s) : fin de chaîne ou espace après.
            pattern = r'(^|\s)' + re.escape(current_name) + r'($|\s)'

            # Parcourir les autres organisations
            for idx2, row2 in enumerate(rows):
                if idx != idx2:
                    other_name = row2['name1']
                    other_norm = other_name.strip().lower()

                    # Vérification de l'égalité stricte (après normalisation)
                    if current_norm == other_norm:
                        msg = (f"L'URI {current_uri} (nom: '{current_name}') est identique à l'URI "
                               f"{row2['org1']} (nom: '{other_name}') (strict).")
                        print(msg)
                        f.write(msg + "\n")
                        g.add((URIRef(current_uri), OWL.sameAs, URIRef(row2['org1'])))
                        found_strict = True

                    # Vérification par regex : current_name apparaît en tant que mot complet dans other_name,
                    # mais uniquement si les noms ne sont pas exactement identiques et que le nom a au moins 5 caractères.
                    if re.search(pattern, other_name, re.IGNORECASE) and current_norm != other_norm and len(current_norm) > 4:
                        msg = (f"L'URI {current_uri} (nom: '{current_name}') est contenu dans l'URI "
                               f"{row2['org1']} (nom: '{other_name}').")
                        print(msg)
                        f.write(msg + "\n")
                        g.add((URIRef(current_uri), ONT.similarTo, URIRef(row2['org1'])))
                        found_regex = True

            # Si aucune correspondance n'est trouvée pour current_name
            if not found_strict and not found_regex:
                msg = f"Aucune organisation n'a exactement le nom '{current_name}' (strict) OU ne contient le nom '{current_name}' en tant que mot complet (regex)."
                print(msg)
                f.write(msg + "\n")

            #insert graph à chaque boucle
            if idx%100 == 0:
                insert_graph(g)
                g=Graph()

        #insert final
        insert_graph(g)



# Exemple d'utilisation
def essai():
    # Exemple de dictionnaire (issu d'une requête SPARQL par exemple)
    data = {
        "columns": ["org1", "name1"],
        "rows": [
            {"org1": "http://example.org/org1", "name1": "Harvard University"},
            {"org1": "http://example.org/org2", "name1": "harvard university"},
            {"org1": "http://example.org/org3", "name1": "University of Harvard and MIT"},
            {"org1": "http://example.org/org4", "name1": "harvard"},
            {"org1": "http://example.org/org5", "name1": "vard"}
        ]
    }
    recon_orga(data)

if __name__ == '__main__':
    #recon_orga_test()
    query = """
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX : <http://www.semanticweb.org/fil_rouge_AntoineValette_GuillaumeRamirez/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>

        SELECT DISTINCT ?org1 ?name1 WHERE {
        ?org1 a :Organization .
        ?org1 skos:prefLabel ?name1 .
            FILTER(contains(LCASE(STR(?org1)), "https://ror") || contains(LCASE(STR(?org1)), "https://www.crunchbase") || contains(LCASE(STR(?org1)), "http://inpi.fr/"))
        }
        """

    orga = sparql_to_dict(query)

    recon_orga(orga)



