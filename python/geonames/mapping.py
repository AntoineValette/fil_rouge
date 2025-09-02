import pandas as pd
import unicodedata
import re
from SPARQLWrapper import SPARQLWrapper, JSON

GRAPHDB_ENDPOINT = "http://localhost:7200/repositories/Fil_Rouge_DB"

def normalize_text(text):
    """
    Normalise une chaîne : conversion en minuscules, suppression des accents et espaces superflus.
    """
    text = str(text)
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return re.sub(r'\s+', ' ', text).strip()

def create_mapping_from_graphdb(iso_type="iso3"):
    """
    Interroge GraphDB pour récupérer les données de mapping pour les villes.
    
    Paramètre :
      - iso_type : "iso3" (par défaut) ou "iso2". 
         Selon la valeur, la requête SPARQL récupère soit le code ISO3 soit le code ISO2 du pays.
    
    Retourne un DataFrame avec les colonnes :
      - city_uri : URI de la ville
      - name : nom officiel (SKOS.prefLabel)
      - alternatenames : liste de noms alternatifs (issus de ns1:Alternate)
      - country_uri : URI du pays (via ns1:aPourPays)
      - <iso_type> : code ISO (ISO3 ou ISO2) du pays (via ns1:code_iso3 ou ns1:code_iso2)
    """
    if iso_type == "iso3":
        code_property = "ns1:code_iso3"
        iso_var = "iso3"
    elif iso_type == "iso2":
        code_property = "ns1:code_iso2"
        iso_var = "iso2"
    else:
        raise ValueError("iso_type must be either 'iso3' or 'iso2'")
    
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)
    query = f"""
    PREFIX ns1: <http://www.semanticweb.org/fil_rouge_AntoineValette_GuillaumeRamirez/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

    SELECT ?city ?name ?alt ?country ?{iso_var}
    WHERE {{
        ?city a ns1:City .
        ?city skos:prefLabel ?name .
        OPTIONAL {{ ?city ns1:Alternate ?alt . }}
        ?city ns1:inCountry ?country .
        ?country {code_property} ?{iso_var} .
    }}
    GROUP BY ?city ?name ?alt ?country ?{iso_var}
    """
    
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    data = []
    for result in results["results"]["bindings"]:
        city_uri = result["city"]["value"]
        name = result["name"]["value"]
        alt_str = result.get("alt", {}).get("value", "")
        alternatenames = [n.strip() for n in alt_str.split(",") if n.strip()] if alt_str else []
        country_uri = result["country"]["value"]
        iso_code = result[iso_var]["value"]
        
        data.append({
            "city_uri": city_uri,
            "name": name,
            "alternatenames": alternatenames,
            "country_uri": country_uri,
            iso_var: iso_code
        })
    mapping_df = pd.DataFrame(data)
    return mapping_df

def build_country_dict(mapping_df: pd.DataFrame, iso_type="iso3"):
    """
    Construit un dictionnaire pour les pays à partir du DataFrame de mapping.
    
    Paramètre :
      - iso_type : "iso3" (par défaut) ou "iso2".
      
    Le dictionnaire aura pour clé la valeur de la colonne correspondante (iso3 ou iso2)
    et pour valeur l'URI du pays.
    """
    # On élimine les doublons pour n'avoir qu'une entrée par pays
    df = mapping_df.drop_duplicates(subset=["country_uri", iso_type])
    return df.set_index(iso_type)["country_uri"].to_dict()

def build_city_dicts(mapping_df: pd.DataFrame):
    """
    Construit deux dictionnaires à partir du DataFrame de mapping pour les villes.
    
    - official_dict : Clés = (country_uri, nom_officiel_normalisé), Valeur = city_uri.
    - alternate_dict : Clés = (country_uri, nom_alternate_normalisé), Valeur = city_uri.
    """
    official_dict = {}
    alternate_dict = {}
    for _, row in mapping_df.iterrows():
        country_uri = row["country_uri"]
        # Ajout du nom officiel
        norm_official = normalize_text(row["name"])
        key_official = (country_uri, norm_official)
        official_dict[key_official] = row["city_uri"]
        # Ajout des noms alternatifs
        for alt in row["alternatenames"]:
            norm_alt = normalize_text(alt)
            key_alt = (country_uri, norm_alt)
            alternate_dict[key_alt] = row["city_uri"]
    return official_dict, alternate_dict

def match_country(country_dict, enterprise_iso3: str):
    """
    Renvoie l'URI du pays à partir du code ISO3 via le dictionnaire country_dict.
    """
    if not enterprise_iso3:
        return None
    return country_dict.get(enterprise_iso3, None)

def match_city(official_dict, alternate_dict, enterprise_city: str, country_uri: str = None):
    """
    Renvoie l'URI de la ville en cherchant dans les dictionnaires officiels et alternatifs 
    via une correspondance exacte.
    
    Si country_uri est fourni, la recherche se fait sur la clé (country_uri, nom_normalisé).
    Sinon, une recherche sur toutes les clés est effectuée.
    
    :param official_dict: Dictionnaire des noms officiels.
    :param alternate_dict: Dictionnaire des noms alternatifs.
    :param enterprise_city: Nom de la ville fourni par l'entreprise.
    :param country_uri: (Optionnel) URI du pays pour restreindre la recherche.
    :return: L'URI de la ville (str) si trouvé, sinon None.
    """
    norm_city = normalize_text(enterprise_city)
    
    if country_uri:
        result = official_dict.get((country_uri, norm_city))
        if result:
            return result
        result = alternate_dict.get((country_uri, norm_city))
        if result:
            return result
    else:
        # Recherche sur l'ensemble des dictionnaires si aucune restriction de pays
        for (c_uri, name), city_uri in official_dict.items():
            if name == norm_city:
                return city_uri
        for (c_uri, name), city_uri in alternate_dict.items():
            if name == norm_city:
                return city_uri
    return None

if __name__ == "__main__":
    df=create_mapping_from_graphdb()
    print(df)