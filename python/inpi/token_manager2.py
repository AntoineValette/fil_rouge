#!/usr/bin/env python3
import os
import csv


def get_inpi_tokens(cookie_file="../../inpi/cookie.txt"):
    """
    Lit le fichier cookie.txt et extrait les tokens requis pour l'API INPI.
    Le fichier doit être au format Netscape HTTP Cookie File.

    Le format attendu pour chaque ligne (après les lignes de commentaire) est :
      domaine, flag, chemin, sécurisé, expiration, nom, valeur

    Les tokens recherchés sont :
      - XSRF-TOKEN
      - access_token
      - refresh_token

    Args:
        cookie_file (str): Chemin vers le fichier cookie.txt. Par défaut, "cookie.txt".

    Returns:
        list: Une liste contenant [xsrf_token, access_token, refresh_token]
    """
    tokens = {}

    # Ouvrir le fichier cookie.txt en lecture
    with open(cookie_file, "r", encoding="utf-8") as f:
        # Utilisation du module csv pour traiter le fichier avec tabulation comme séparateur
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            # Ignorer les lignes vides ou qui commencent par '#' (lignes de commentaires)
            if not row :
                continue
            # Vérifier que la ligne contient au moins 7 colonnes
            if len(row) < 7:
                continue
            # Extraction du nom et de la valeur du token (colonnes 6 et 7, index 5 et 6)
            token_name = row[5].strip()
            token_value = row[6].strip()
            # Stocker le token si son nom correspond à l'un de ceux recherchés (en comparant en minuscules)
            if token_name.lower() in ["xsrf-token", "access_token", "refresh_token"]:
                tokens[token_name.lower()] = token_value

    # Récupération des tokens dans l'ordre requis
    xsrf_token = tokens.get("xsrf-token")
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")

    return [xsrf_token, access_token, refresh_token]


if __name__ == "__main__":
    # Récupération des tokens depuis le fichier cookie.txt
    tokens = get_inpi_tokens()
    print("Tokens récupérés :", tokens)