from rdflib import Graph, URIRef, Literal, Namespace, RDF
from python.util.Namespaces import ONT, WD, WDT, RDFS, SKOS
from urllib.parse import quote_plus

SS = Namespace("http://SemanticScholar.org/")


def add_publication_venue(paper_uri:URIRef, pubVenue: {}, g: Graph):
    if pubVenue is not None:
        publicationid = pubVenue.get("id", "unknown")  # Évite les valeurs None

        # Vérification et encodage de l'URL pour éviter les erreurs
        pub_url_raw = pubVenue.get("url")
        if isinstance(pub_url_raw, str) and pub_url_raw.strip():
            try:
                pub_url = URIRef(quote_plus(pub_url_raw, safe=":/"))  # Encode les caractères spéciaux
            except Exception as e:
                print(f"⚠️ URL invalide ignorée : {pub_url_raw} → {e}")
                pub_url = URIRef(SS + publicationid)  # Utiliser un URI de secours
        else:
            pub_url = URIRef(SS + publicationid)  # URI fallback si aucune URL valide

        g.add((pub_url, RDF.type, ONT.PublicationVenue))
        g.add((paper_uri, ONT.isPublishedIn, pub_url)) # on lie le paper à la pulicationVenue

        g.add((pub_url, ONT.publicationid, Literal(publicationid)))

        pub_name= pubVenue.get("name")
        g.add((pub_url, SKOS.prefLabel, Literal(pub_name)))
        for i in pubVenue.get("alternate_names" ,[]):
            g.add((pub_url, SKOS.altLabel, Literal(i)))

        issn =pubVenue.get("issn")
        g.add((pub_url, ONT.issn, Literal(issn)))
        for i in pubVenue.get("alternate_issns" ,[]):
            g.add((pub_url, ONT.issn, Literal(i)))