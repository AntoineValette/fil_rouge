## Description de l'arborescence du projet

```sh
Fil_Rouge
├── README.md
├── ROR/                                            # Données de ROR
├── crunchbase/                                     # Données de Crunchbase
├── docker-compose.yaml                             # Fichier de configuration Docker Compose
├── init_graphDB.sh                                 # Script d'initialisation du repo et de l'ontologie
├── inpi/                                           # Connexion à l'API de l'inpi
├── onto/                                           # Ontologie
├── places/                                         # Données de Geonames
├── python/                                         # Répertoire de tous les scripts python
│   ├── ROR/                                        # Scripts d'import de ROR
│   ├── crunchbase/                                 # Scripts d'import de Crunchbase
│   ├── geonames/                                   # Scripts d'import de Geonames, villes et pays
│   ├── inpi/                                       # Scripts d'import des brevets de l'inpi
│   ├── post_processing/                            # Scripts de post processing (reconciliation des noms, extractions mots-clés)
│   ├── semantic_scholar/                           # Scripts d'import des articles scientifiques
│   ├── test/                                       # Test d'utilisation de LLMs en local (GTP-neo-1B)
│   ├── util/                                       # Fonctions diverses pour la gestion de GraphDB (supprimer, insérer graphs...)
│   └── wikidata/                                   # Scripts d'import de wikidata (ancienne gestion de la geographie)
├── repo/                                           # Fichier de configuration du repository GraphDB
├── visualisation/                                  # Quelques notebooks de visualisation de résultats
└── Rapport.pdf                                     # Rapport du projet au format PDF intéractif