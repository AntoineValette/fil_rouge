#!/bin/sh

echo "📦 Attente du démarrage de GraphDB..."
sleep 5

REPO_ID="Fil_Rouge_DB"
REPO_FILE="/repo/Fil_Rouge_DB.ttl"
REPO_URL="http://graphdb:7200/repositories/${REPO_ID}"

echo "🛠️  Création du repository depuis $REPO_FILE..."
curl -X POST \
  -H "Content-Type: multipart/form-data" \
  -F config=@"$REPO_FILE" \
  http://graphdb:7200/rest/repositories

echo "✅ Repository $REPO_ID créé."

# Import de toutes les ontologies présentes dans /data/
for file in /data/*.ttl /data/*.rdf /data/*.owl; do
  if [ -f "$file" ]; then
    echo "🔄 Import de $file..."
    case "$file" in
      *.ttl) MIME="text/turtle" ;;
      *.rdf|*.owl) MIME="application/rdf+xml" ;;
      *) echo "❌ Format non reconnu : $file" ; continue ;;
    esac

    curl -X POST -H "Content-Type: $MIME" \
         --data-binary @"$file" \
         "$REPO_URL/statements"

    echo "✅ $file importé."
  fi

done
