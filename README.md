# Stych Caller - Suivi et Notification de Propositions de Cours

Ce projet vous permet de surveiller automatiquement les nouvelles propositions de cours de conduite Stych et d'être notifié par email dès qu'une nouvelle proposition apparaît.

## Prérequis
- Un ordinateur avec Windows, Mac ou Linux
- [Python 3](https://www.python.org/downloads/) installé (vérifiez avec `python --version` dans le terminal)
- Un compte Gmail (ou autre SMTP) pour recevoir les notifications par email

## Installation rapide
1. **Téléchargez le dossier du projet** sur votre ordinateur.
2. **Ouvrez un terminal** (cmd, PowerShell ou Terminal sur Mac/Linux) dans le dossier du projet.
3. Installez les dépendances nécessaires :
   ```sh
   pip install -r requirements.txt
   ```
   Si le fichier `requirements.txt` n'existe pas, lancez simplement :
   ```sh
   pip install requests python-dotenv
   ```

## Configuration de l'email
1. **Créez un mot de passe d'application** pour Gmail (voir plus bas si besoin d'aide).
2. **Ouvrez le fichier `.env`** dans le dossier du projet.
3. **Remplissez les champs** avec vos informations :
   ```env
   EMAIL_HOST_USER=votre_email@gmail.com
   EMAIL_HOST_PASSWORD=mot_de_passe_application
   EMAIL_TO=destinataire@exemple.com
   ```
   (Vous pouvez laisser les autres valeurs par défaut)

## Récupération des données Stych
1. **Ouvrez le fichier `env/data.json`** et ajoutez vos en-têtes d'authentification (voir la documentation Stych ou copiez-les depuis votre navigateur connecté).

---

## Utilisation manuelle (affichage dans le terminal)
Pour afficher les propositions de cours actuelles dans le terminal :

```sh
python main.py
```

Vous verrez la liste des cours triés par lieu et par date.

---

## Utilisation automatique (notification par email)
Pour recevoir un email à chaque nouvelle proposition de cours :

```sh
python automatic_caller.py
```

- Le script vérifie toutes les 5 minutes s'il y a de nouvelles propositions.
- Si oui, vous recevez un email avec un tableau récapitulatif.
- Les propositions déjà vues ne déclenchent pas de nouvel email.

---

## FAQ

### Comment obtenir un mot de passe d'application Gmail ?
1. Activez la validation en deux étapes sur votre compte Google.
2. Rendez-vous sur https://myaccount.google.com/apppasswords
3. Générez un mot de passe pour "Mail" et "Autre" (nommez-le comme vous voulez).
4. Copiez le mot de passe généré dans le champ `EMAIL_HOST_PASSWORD` du fichier `.env`.

### Puis-je utiliser un autre service mail ?
Oui, modifiez les champs `EMAIL_HOST` et `EMAIL_PORT` dans `.env` selon votre fournisseur (ex : Outlook, Yahoo, etc).

### Je veux tester avec un fichier local
Vous pouvez utiliser le script `parser.py` pour afficher un fichier JSON local :
```sh
python parser.py chemin/vers/votre_fichier.json
```

---

## Support
Pour toute question, contactez : contact@adaoud.dev
