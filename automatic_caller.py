import requests
import os
import json
import time
import smtplib
from email.mime.text import MIMEText
from parser import trier_et_afficher_cours_par_lieu, extraire_cours_par_lieu
from dotenv import load_dotenv
if not os.path.exists(".env"):
    with open(".env", "w", encoding="utf-8") as f:
        f.write("EMAIL_HOST_USER=\nEMAIL_HOST_PASSWORD=\nEMAIL_TO=\n")
    print("Veuillez renseigner le fichier .env avec les informations d'email nécessaires.")
    exit(1)
# Load environment variables from .env file
load_dotenv()

EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_FROM = os.getenv('EMAIL_FROM', EMAIL_HOST_USER)
EMAIL_TO = os.getenv('EMAIL_TO')

CHECK_INTERVAL = 300 
SEEN_FILE = 'env/seen_propositions.json'

url = "https://www.stych.fr/elearning/planning-conduite/get-planning-proposition"
if not os.path.exists("env"):
    os.makedirs("env", exist_ok=True)
if not os.path.exists(SEEN_FILE):
    with open(SEEN_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)
if not os.path.exists("env/data.json"):
    print("Veuillez renseigner le fichier env/data.json avec les headers nécessaires.")
    exit(1)
with open("env/data.json", "r", encoding="utf-8") as f:
    headers = json.load(f)

def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, 'r', encoding='utf-8') as f:
            return set(json.load(f))
    return set()

def save_seen(seen):
    with open(SEEN_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(seen), f)

def send_email(subject, body, html_body=None):
    if html_body:
        msg = MIMEText(html_body, 'html', 'utf-8')
    else:
        msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            server.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())
        print(f"Email envoyé à {EMAIL_TO}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")

def format_new_propositions(new_props, lieux):
    # Plain text version
    lines = []
    for prop in new_props:
        id_lac = prop["id_lac"]
        lieu = lieux.get(id_lac, {})
        nom_lieu = lieu.get("intitule", "Lieu inconnu")
        adresse = lieu.get("adresse_cp_ville", "Adresse inconnue")
        date = prop.get("info_date", "Date inconnue")
        heure = prop.get("heure_debut_fr", "Heure inconnue")
        lines.append(f"📍 {nom_lieu} - {adresse}\n📅 {date} à 🕒 {heure}\n")
    text = '\n'.join(lines)

    # HTML version
    html = '''<html><body style="font-family:sans-serif; background:#f9f9f9;">
    <h2 style="color:#2d7be5;">Nouvelles propositions de cours Stych</h2>
    <table style="border-collapse:collapse; width:100%; background:#fff;">
      <thead>
        <tr style="background:#eaf3fb;">
          <th style="border:1px solid #b6d4f7; padding:8px;">Lieu</th>
          <th style="border:1px solid #b6d4f7; padding:8px;">Adresse</th>
          <th style="border:1px solid #b6d4f7; padding:8px;">Date</th>
          <th style="border:1px solid #b6d4f7; padding:8px;">Heure</th>
        </tr>
      </thead>
      <tbody>
    '''
    for prop in new_props:
        id_lac = prop["id_lac"]
        lieu = lieux.get(id_lac, {})
        nom_lieu = lieu.get("intitule", "Lieu inconnu")
        adresse = lieu.get("adresse_cp_ville", "Adresse inconnue")
        date = prop.get("info_date", "Date inconnue")
        heure = prop.get("heure_debut_fr", "Heure inconnue")
        html += f'''<tr>
          <td style="border:1px solid #b6d4f7; padding:8px;">{nom_lieu}</td>
          <td style="border:1px solid #b6d4f7; padding:8px;">{adresse}</td>
          <td style="border:1px solid #b6d4f7; padding:8px;">{date}</td>
          <td style="border:1px solid #b6d4f7; padding:8px;">{heure}</td>
        </tr>'''
    html += '''</tbody></table>
    <p style="color:#888; font-size:12px; margin-top:20px;">Ceci est un message automatique. Merci de ne pas répondre directement à cet email.</p>
    </body></html>'''
    return text, html

def get_prop_key(prop):
    """Return a unique key for a proposition based on its main fields."""
    return f"{prop.get('id_user','')}|{prop.get('info_date','')}|{prop.get('heure_debut','')}|{prop.get('heure_fin','')}|{prop.get('id_lac','')}"

def main_loop():
    seen = load_seen()
    print("Démarrage du monitoring des propositions de cours...")
    while True:
        try:
            response = requests.get(url, headers=headers)
            if response.ok:
                data = response.json()
                cours_par_lieux, lieux = extraire_cours_par_lieu(data)
                all_props = [prop for cours in cours_par_lieux.values() for prop in cours]
                new_props = [p for p in all_props if get_prop_key(p) not in seen]
                if new_props:
                    print(f"{len(new_props)} nouvelle(s) proposition(s) détectée(s) ! Envoi d'un email...")
                    text, html = format_new_propositions(new_props, lieux)
                    send_email("Nouvelles propositions de cours Stych", text, html_body=html)
                    for p in new_props:
                        seen.add(get_prop_key(p))
                    save_seen(seen)
                else:
                    print("Aucune nouvelle proposition.")
            else:
                print(f"Erreur lors de la récupération des données : code {response.status_code}")
        except Exception as e:
            print(f"Erreur lors de l'exécution : {e}")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main_loop()
