import requests
from parser import trier_et_afficher_cours_par_lieu, extraire_cours_par_lieu
import os
import sys
import json

url = "https://www.stych.fr/elearning/planning-conduite/get-planning-proposition"
if not os.path.exists("env/data.json"):
    os.makedirs("env", exist_ok=True)
    if not os.path.exists("env/data.json"):
        with open("env/data.json", "w", encoding="utf-8") as f:
            json.dump({}, f)
    print("Veuillez renseigner le fichier env/data.json avec les headers nécessaires.")
    sys.exit(1)
with open("env/data.json", "r", encoding="utf-8") as f:
    headers = json.load(f)

response = requests.get(url, headers=headers)

if response.ok:
    # Nous avons bien fetch les données de cours
    cours_par_lieux, lieux = extraire_cours_par_lieu(response.json())
    trier_et_afficher_cours_par_lieu(cours_par_lieux, lieux)
else:
    print(f"Erreur lors de la récupération des données : code {response.status_code}")