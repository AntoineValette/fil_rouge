from rdflib import Graph, URIRef, OWL
from python.util.Namespaces import ONT, WD, WDT, RDFS, SKOS
from python.util.insert_graph import insert_graph
from python.util.query_graphDB import sparql_to_dict


def split_name(name: str):
    """
    Divise le nom en prénom et nom de famille.
    On considère que le prénom est le premier token et le nom de famille le dernier token.
    Si le nom ne contient qu'un token, le prénom sera une chaîne vide.
    """
    tokens = name.strip().split()
    if len(tokens) >= 2:
        return tokens[0], tokens[-1]
    else:
        return "", name.strip()


def recon_personnes(data: dict):
    """
    Parcourt le dictionnaire (contenant la clé "rows") et, pour chaque personne, compare son nom (clé "name1")
    avec ceux des autres personnes.
    - D'abord, on teste l'égalité stricte après normalisation (strip et lower).
    - Si aucune correspondance stricte n'est trouvée, on découpe le nom en prénom et nom de famille
      et on vérifie :
        * Soit que les deux prénoms et les deux noms de famille sont identiques,
        * Soit que l'un des prénoms est indiqué par une initiale (une lettre suivie d'un point, donc de longueur 2)
          et que les premières lettres des prénoms concordent, et que les noms de famille sont identiques.
    Les messages sont affichés et écrits dans le fichier "output_reco_personnes.txt".
    """

    base_crunch="https://www.crunchbase.com"
    base_semantic="https://www.semanticscholar.org"
    base_inpi="http://inpi.fr"

    with open("output_reco_personnes.txt", "w", encoding="utf-8") as f:
        rows = data.get("rows", [])
        print(len(rows))
        g = Graph()

        # Parcourir chaque personne dans les lignes du dictionnaire
        for idx, row in enumerate(rows):
            current_name = row['name1']
            current_norm = current_name.strip().lower()
            current_uri = row['p1']
            found_strict = False
            found_split = False

            # Première passe : comparaison stricte (nom complet après normalisation)
            current_first, current_last = split_name(current_norm)
            #print(f"Analyse: {current_first} {current_last}")

            for idx2, row2 in enumerate(rows):
                 if idx != idx2:
                     if (base_crunch in current_uri and base_crunch not in row2['p1']) or (
                             base_semantic in current_uri and base_semantic not in row2['p1']) or (
                             base_inpi in current_uri and base_inpi not in row2['p1']):

                        other_name = row2['name1']
                        other_norm = other_name.strip().lower()
                        # Comparaison stricte des noms complets
                        if current_norm == other_norm:
                            msg = (f"L'URI {current_uri} (nom: '{current_name}') est identique à l'URI "
                                   f"{row2['p1']} (nom: '{other_name}') (strict).")
                            print(msg)
                            f.write(msg + "\n")
                            g.add((URIRef(current_uri), OWL.sameAs, URIRef(row2['p1'])))
                            found_strict = True
                        else:
                            other_first, other_last = split_name(other_norm)
                            # Vérification que les deux prénoms sont non vides
                            if len(current_first) > 0 and len(other_first) > 0:
                                # Cas 1 : comparaison stricte des deux composantes (prénom et nom)
                                if current_first == other_first and current_last == other_last and len(current_first) > 2 and len(other_last) > 2:
                                    msg = (f"L'URI {current_uri} (nom: '{current_name}') correspond par split à l'URI "
                                           f"{row2['p1']} (nom: '{other_name}').")
                                    print(msg)
                                    f.write(msg + "\n")
                                    g.add((URIRef(current_uri), OWL.sameAs, URIRef(row2['p1'])))
                                    found_split = True
                                else:
                                    # Cas 2 : au moins l'un des prénoms est une initiale (ex: "A.")
                                    if (len(current_first) == 2 or len(other_first) == 2) and current_last == other_last:
                                        if current_first and other_first and current_first[0] == other_first[0]:
                                            msg = (f"L'URI {current_uri} (nom: '{current_name}') correspond par initiale à l'URI "
                                                   f"{row2['p1']} (nom: '{other_name}').")
                                            print(msg)
                                            f.write(msg + "\n")
                                            g.add((URIRef(current_uri), ONT.similarTo, URIRef(row2['p1'])))
                                            found_split = True

            if not found_strict and not found_split:
                msg = f"Aucune correspondance trouvée pour la personne '{current_name}'."
                print(msg)
                f.write(msg + "\n")

            # insert graph à chaque boucle
            if idx % 100 == 0:
                insert_graph(g)
                g = Graph()

        # insert final
        insert_graph(g)

# Exemple d'utilisation
def essai():
    # Exemple de dictionnaire (issu par exemple d'une requête SPARQL)
    data = {
        "columns": ["p1", "name1"],
        "rows": [
            {"p1": "http://example.org/p1", "name1": "Alice Johnson"},
            {"p1": "http://example.org/p2", "name1": "alice johnson"},
            {"p1": "http://example.org/p3", "name1": "A. Johnson"},
            {"p1": "http://example.org/p4", "name1": "Bob Smith"},
            {"p1": "http://example.org/p5", "name1": "Alice-Marie Johnson"},
            {"p1": "http://example.org/p6", "name1": "Alice Marie Johnson"}
        ]
    }
    recon_personnes(data)

if __name__ == '__main__':
    query="""
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX : <http://www.semanticweb.org/fil_rouge_AntoineValette_GuillaumeRamirez/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    
    SELECT DISTINCT ?p1 ?name1 WHERE {
      ?p1 a :Person .
          ?p1 skos:prefLabel ?name1 .
      FILTER(contains(LCASE(STR(?p1)), "http://inpi.fr/") || contains(LCASE(STR(?p1)), "https://www.crunchbase") || contains(LCASE(STR(?p1)), "https://www.semanticscholar"))
    }
    """

    ppl = sparql_to_dict(query)

    recon_personnes(ppl)




