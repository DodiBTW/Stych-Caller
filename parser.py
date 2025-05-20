from collections import defaultdict

def trier_et_afficher_cours_par_lieu(data, lieux):
    """
    Prend un JSON avec 'rowsPointDeCours' et 'rowsProposition',
    trie les cours par lieu, puis affiche proprement.
    """
    

    for id_lac, cours in data.items():
        lieu = lieux.get(id_lac, {})
        nom_lieu = lieu.get("intitule", "Lieu inconnu")
        adresse = lieu.get("adresse_cp_ville", "Adresse inconnue")

        print(f"\n📍 {nom_lieu} - {adresse}")
        print("-" * 60)

        cours_sorted = sorted(cours, key=lambda x: (x["info_date"], x["heure_debut"]))
        for c in cours_sorted:
            date = c.get("info_date", "Date inconnue")
            heure = c.get("heure_debut_fr", "Heure inconnue")
            print(f"📅 {date} à 🕒 {heure}")

def extraire_cours_par_lieu(data):
    """
    Extrait les cours par lieu à partir des données JSON.
    """
    lieux = {row["id_liste_adresse_cours"]: row for row in data["rowsPointDeCours"]}
    cours_par_lieu = defaultdict(list)

    for prop in data["rowsProposition"]:
        id_lac = prop["id_lac"]
        cours_par_lieu[id_lac].append(prop)
    return cours_par_lieu, lieux

if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) < 2:
        print("Usage: python tri_cours.py chemin_vers_fichier.json")
        exit(1)

    chemin_fichier = sys.argv[1]
    with open(chemin_fichier, "r", encoding="utf-8") as f:
        json_data = json.load(f)
    data, lieux = extraire_cours_par_lieu(json_data)
    trier_et_afficher_cours_par_lieu(data, lieux)
