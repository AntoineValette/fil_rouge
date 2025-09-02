### construct chercheur-inventeur
'''
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX : <http://www.semanticweb.org/fil_rouge_AntoineValette_GuillaumeRamirez/>

CONSTRUCT {
  ?person a :Researcher .
  ?person :isAuthorOf ?doc .
  ?doc :title ?titleDoc .
  
  ?person a :Inventor .
  ?person skos:prefLabel ?name .
  ?person :isInventorOf ?patent .
  ?patent :title ?titlePatent .
}
WHERE {
  ?person a :Researcher .
  ?person :isAuthorOf ?doc .
  ?doc :title ?titleDoc .

  ?person a :Inventor .
  ?person skos:prefLabel ?name .
  ?person :isInventorOf ?patent .
  ?patent :title ?titlePatent .
}
'''
###construct orga qualcom
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX : <http://www.semanticweb.org/fil_rouge_AntoineValette_GuillaumeRamirez/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

CONSTRUCT {
  ?org ?p ?o .
}
WHERE {
  {
    SELECT ?org WHERE {
      {
        # On sélectionne l'organisation de départ dont le libellé contient "Rakuten"
        SELECT ?startOrg WHERE {
          ?startOrg a :Organization ;
                    skos:prefLabel ?name .
          FILTER(CONTAINS(LCASE(STR(?name)), "qualcom"))
        }
      }
      # On récupère la fermeture transitve sur les relations owl:sameAs et :similar
      ?startOrg (owl:sameAs|:relatedTo)* ?org .
    }
  }
  ?org ?p ?o .
}
'''

### construct orga Rakuten
'''
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX : <http://www.semanticweb.org/fil_rouge_AntoineValette_GuillaumeRamirez/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

CONSTRUCT {
  ?org ?p ?o .
}
WHERE {
  {
    SELECT ?org WHERE {
      {
        # On sélectionne l'organisation de départ dont le libellé contient "Rakuten"
        SELECT ?startOrg WHERE {
          ?startOrg a :Organization ;
                    skos:prefLabel ?name .
          FILTER(CONTAINS(LCASE(STR(?name)), "rakuten"))
        }
      }
      # On récupère la fermeture transitive sur les relations owl:sameAs et :relatedTo
      ?startOrg (owl:sameAs|:relatedTo)* ?org .
    }
  }
  ?org ?p ?o .
  FILTER(?p != rdf:type && ?p != :inCountry && ?p != :inCity)
}
'''

### construct person christopher martin
'''
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX : <http://www.semanticweb.org/fil_rouge_AntoineValette_GuillaumeRamirez/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

CONSTRUCT {
  ?org ?p ?o .
}
WHERE {
  {
    SELECT ?org WHERE {
      {
        # On sélectionne l'organisation de départ dont le libellé contient "Rakuten"
        SELECT ?startOrg WHERE {
          ?startOrg a :Organization ;
                    skos:prefLabel ?name .
          FILTER(CONTAINS(LCASE(STR(?name)), "rakuten"))
        }
      }
      # On récupère la fermeture transitive sur les relations owl:sameAs et :relatedTo
      ?startOrg (owl:sameAs|:relatedTo)* ?org .
    }
  }
  ?org ?p ?o .
  FILTER(?p != rdf:type && ?p != :inCountry && ?p != :inCity)
}
'''

### select orga similarTo
''''
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX : <http://www.semanticweb.org/fil_rouge_AntoineValette_GuillaumeRamirez/>

SELECT DISTINCT ?name1 ?name2
WHERE {
    ?org1 a :Organization .
    ?org2 a :Organization .
    ?org1 skos:prefLabel ?name1 .
    ?org2 skos:prefLabel ?name2.
    ?org1 :similarTo ?org2 .
''''

### select orga not olw:sameAs
''''
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX : <http://www.semanticweb.org/fil_rouge_AntoineValette_GuillaumeRamirez/>

SELECT DISTINCT ?org1 ?org2 ?name
WHERE {
  ?org1 a :Organization ;
        skos:prefLabel ?name .
  ?org2 a :Organization ;
        skos:prefLabel ?name .
  FILTER NOT EXISTS { ?org1 owl:sameAs ?org2 }
}
''''

###select chercheur entrepreneurs
''''
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX : <http://www.semanticweb.org/fil_rouge_AntoineValette_GuillaumeRamirez/>

SELECT DISTINCT ?name ?doc ?titleDoc ?company ?nameCo
WHERE {
  ?person a :Researcher .
  ?person :isAuthorOf ?doc .
  ?doc :title ?titleDoc .
  ?person skos:prefLabel ?name .
  ?person :isFounderOf ?company .
  ?company skos:prefLabel ?nameCo .
}
''''

### select chercheurs investiiseurs
''''
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX : <http://www.semanticweb.org/fil_rouge_AntoineValette_GuillaumeRamirez/>

SELECT DISTINCT ?name ?doc ?titleDoc ?patent ?titlePatent
WHERE {
  ?person a :Researcher .
  ?person :isAuthorOf ?doc .
  ?doc :title ?titleDoc .

  ?person a :Inventor .
  ?person skos:prefLabel ?name .
  ?person :isInventorOf ?patent .
  ?patent :title ?titlePatent .
}
''''
