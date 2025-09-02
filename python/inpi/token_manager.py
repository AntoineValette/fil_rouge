import os
from dotenv import load_dotenv


def get_inpi_tokens():
    # Charger le fichier .env
    load_dotenv()
    # Récupérer les tokens
    TOKEN = os.getenv("XSRF-TOKEN")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

    # Récupération des secrets depuis les settings
    secrets = [TOKEN, ACCESS_TOKEN, REFRESH_TOKEN]

    return secrets

if __name__ == "__main__":
    print(get_inpi_tokens())