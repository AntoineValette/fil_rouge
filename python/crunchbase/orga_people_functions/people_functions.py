from rdflib import Graph, URIRef, Literal, Namespace, RDF
from python.util.Namespaces import ONT, WD, WDT, RDFS, SKOS

def add_name(person_uri:URIRef, first_name: str, last_name: str, g: Graph):
    try:
        if first_name is not None:
            g.add((person_uri, ONT.firstName, Literal(first_name)))
        if last_name is not None:
            g.add((person_uri, ONT.lastName, Literal(last_name)))
        if first_name is not None or last_name is not None:
            name=""+first_name+" "+last_name
            g.add((person_uri, SKOS.prefLabel, Literal(name)))
    except :
        print(f"first name ({first_name})(type : {type(first_name)}) last name ({last_name})(type : {type(last_name)})")



def add_role(person_uri:URIRef, role: str, orga_uri: URIRef, g: Graph):
    role=str(role).lower()
    if role is not None:
        foundAtLeastOneRole=False
        if "founder" in role:
            g.add((person_uri, ONT.isFounderOf, orga_uri))
            foundAtLeastOneRole=True
        if "owner" in role:
            g.add((person_uri, ONT.isOwnerOf, orga_uri))
            foundAtLeastOneRole = True
        if "CEO" in role or "chief executive officer" in role:
            g.add((person_uri, ONT.isCEOof, orga_uri))
            foundAtLeastOneRole = True
        if "CFO" in role or "chief financial" in role:
            g.add((person_uri, ONT.isCFOof, orga_uri))
            foundAtLeastOneRole = True
        if "CTO" in role or "chief technical" in role or "chief technology" in role:
            g.add((person_uri, ONT.isCTOof, orga_uri))
            foundAtLeastOneRole = True
        if "investor" in role:
            g.add((person_uri, ONT.isInvestorOf, orga_uri))
            foundAtLeastOneRole = True

        if "chief" in role and "officer" in role and "CEO" not in role \
                and "CFO" not in role and "CTO" not in role \
                and "chief executive officer" not in role and "chief financial" not in role \
                and "chief technical" not in role and "chief technology" not in role:
            g.add((person_uri, ONT.isOtherExec, orga_uri))
            foundAtLeastOneRole = True

        if "board" in role and "officer" not in role and "CEO" not in role \
                and "CFO" not in role and "CTO" not in role \
                and "chief executive officer" not in role and "chief financial" not in role \
                and "chief technical" not in role and "chief technology" not in role:
            g.add((person_uri, ONT.atBoardOf, orga_uri))
            foundAtLeastOneRole = True

        if foundAtLeastOneRole==False:
            # par défaut, si la personne n'est pas CEO, CFO,CTO, etc. elle travaille pour l'orga
            g.add((person_uri, ONT.worksFor, orga_uri))


