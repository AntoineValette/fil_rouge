import validators
import urllib.parse

def clean_and_encode_uri(uri: str) -> str:
    # Supprimer les espaces et les guillemets superflus
    uri = str(uri).strip().strip('\'"')
    # Analyser l'URI
    parsed = urllib.parse.urlsplit(uri)
    # Encoder le chemin et la query
    path = urllib.parse.quote(parsed.path)
    # Pour la query, on souhaite conserver certains caractères comme '=' et '&'
    query = urllib.parse.quote(parsed.query, safe="=&")
    # Reconstruire l'URI
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, path, query, parsed.fragment))


def is_valid_uri(uri: str) -> bool:
    """
    Vérifie si une chaîne de caractères est un URI (URL) valide.

    :param uri: La chaîne à vérifier.
    :return: True si l'URI est valide, False sinon.
    """
    result = validators.url(uri)
    if result==False:
        print(f"{uri} is not a valid URI.")
    return bool(result)

if __name__ == '__main__':
    # Exemple d'utilisation
    uris = [
        "http://example.com",
        "https://www.example.com/some/path?query=param#fragment",
        "http://letsgive.dk/\"",
        "invalid_uri"
    ]

    for uri in uris:
        print(f"{uri}: {is_valid_uri(uri)}")