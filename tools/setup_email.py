"""
setup_email.py — Configure l'envoi d'emails une seule fois.
Lance avec : python setup_email.py
"""
import json
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "email_config.json"

print("""
===========================================
  Configuration Email — Claude Code
===========================================

Pour envoyer des emails depuis ton compte Gmail, tu as besoin
d'un "Mot de passe d'application" Google (différent de ton vrai mdp).

Comment l'obtenir (2 minutes) :
1. Va sur : myaccount.google.com/security
2. Active la "Validation en 2 étapes" si pas encore fait
3. Cherche "Mots de passe des applications"
4. Crée une appli : sélectionne "Autre" → nomme-la "Claude Code"
5. Google te donne un code de 16 lettres — copie-le ici
""")

app_password = input("Colle ton mot de passe d'application Gmail (16 caractères) : ").strip().replace(" ", "")

if len(app_password) != 16:
    print(f"Attention : le mot de passe fait {len(app_password)} caractères (attendu : 16)")

config = {
    "sender_email": "acollenne@gmail.com",
    "gmail_app_password": app_password,
    "default_recipient": "acollenne@gmail.com"
}

with open(CONFIG_PATH, "w") as f:
    json.dump(config, f, indent=2)

print(f"\nConfiguration sauvegardee dans {CONFIG_PATH}")
print("Test d'envoi...")

import smtplib
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("acollenne@gmail.com", app_password)
    print("Connexion Gmail reussie ! Les emails seront envoyes automatiquement.")
except Exception as e:
    print(f"Erreur de connexion : {e}")
    print("Verifie ton mot de passe d'application.")
