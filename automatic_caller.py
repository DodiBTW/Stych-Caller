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
    example_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Referer": "https://www.stych.fr/",
        "Cookie": ""
    }
    with open("env/data.json", "w", encoding="utf-8") as f:
        json.dump(example_headers, f, indent=4, ensure_ascii=False)
    print('Le fichier env/data.json a été créé avec un exemple de headers. Veuillez compléter le champ "Cookie" avec vos informations de cookie (voir README).')
    exit(1)
with open("env/data.json", "r", encoding="utf-8") as f:
    headers = json.load(f)
