#!/bin/bash

LIBRARY_ID="35843"
API_KEY="0dab2b0e-9bf9-4dec-aadaeca930b4-cf5e-4324"
COLLECTION_ID="f53a2ad0-2ffe-430f-abd8-6004bac5751c"

# Récupérer les vidéos
videos=$(curl -s "https://video.bunnycdn.com/library/$LIBRARY_ID/videos?page=1&itemsPerPage=100&collection=$COLLECTION_ID" \
  -H "AccessKey: $API_KEY")

# Parser et renommer chaque vidéo qui commence par un numéro
echo "$videos" | jq -r '.items[] | "\(.guid)|\(.title)"' | while IFS='|' read -r guid title; do
  
  # Extraire le numéro au début du titre (ex: "1-La-regle" -> "1")
  if [[ $title =~ ^([0-9]+)[-_] ]]; then
    num="${BASH_REMATCH[1]}"
    
    # Formater sur 2 chiffres
    new_num=$(printf "%02d" "$num")
    
    # Construire le nouveau titre
    new_title="${title/#$num/$new_num}"
    
    if [ "$title" != "$new_title" ]; then
      echo "Renommage: $title"
      echo "       -> $new_title"
      
      # Appel API pour renommer
      curl -s -X POST "https://video.bunnycdn.com/library/$LIBRARY_ID/videos/$guid" \
        -H "AccessKey: $API_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"title\": \"$new_title\"}"
      
      echo "✅ OK"
      echo ""
    fi
  fi
done

echo "Terminé !"
