import pandas as pd
from python.wikidata.countries_query import get_countries

bindings=get_countries()

def get_country_mapping():

    # Transformer les résultats en DataFrame en extrayant la valeur de chaque champ
    df = pd.DataFrame({
        "country": [item["country"]["value"] for item in bindings],
        "countryLabel": [item["countryLabel"]["value"] for item in bindings],
        "iso3": [item["iso3"]["value"] for item in bindings],
        "iso2": [item["iso2"]["value"] for item in bindings]
    })

    # Il manque HKG (qui doit être CHN dans le df) donc on le rajoute manuellement
    new_row = {'country': 'https://www.wikidata.org/wiki/Q8646', 'countryLabel': 'Hong Kong', 'iso3': 'HKG', 'iso2':'HK'}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    new_row = {'country': 'https://www.wikidata.org/wiki/Q218', 'countryLabel': 'Romania', 'iso3': 'ROM', 'iso2':'RO'}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    return df


def get_country_by_by_code_iso3(df, iso):
    filtered_df = df[(df['iso3'].str.lower() == str(iso).lower())]
    if not filtered_df.empty:
        return filtered_df.iloc[0]['country']
    else:
        return None

def get_country_by_by_code_iso2(df, iso):
    filtered_df = df[(df['iso2'].str.lower() == str(iso).lower())]
    if not filtered_df.empty:
        return filtered_df.iloc[0]['country']
    else:
        return None

if __name__ == '__main__':
    # Par exemple, pour obtenir l'identifiant Wikidata correspondant à "FRA"
    """
    print(get_country_by_by_code_iso3(get_country_mapping(),"FRA"))  # Doit afficher "wd:Q142"
    print(get_country_by_by_code_iso3(get_country_mapping(), "NLD"))
    print(get_country_by_by_code_iso3(get_country_mapping(), "USA"))

    print(get_country_by_by_code_iso3(get_country_mapping(), "AUT"))
    print(get_country_by_by_code_iso3(get_country_mapping(), "UKR"))
    print(get_country_by_by_code_iso3(get_country_mapping(), "JEY"))
    """

    print(get_country_by_by_code_iso2(get_country_mapping(), "FR"))  # Doit afficher "wd:Q142"
    print(get_country_by_by_code_iso2(get_country_mapping(), "NL"))
    print(get_country_by_by_code_iso2(get_country_mapping(), "US"))
