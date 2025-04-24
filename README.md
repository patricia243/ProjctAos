# 🎓 API Flask – Gestion des Étudiants et de leurs Notes

Cette application est une API REST développée avec **Flask**. Elle permet :
- ✅ L’inscription des étudiants.
- ✅ La gestion de leurs notes (ajout, récupération).
- ✅ Le stockage des données dans une base **SQLite**.
- ✅ Le déploiement via [Render](https://render.com).

---

## ⚙️ Étapes de création du projet

### 1. Création de l'environnement virtuel

```bash
python -m venv venv
venv\Scripts\activate  # Windows

2. Installation des dépendances

pip install flask flask_sqlalchemy
pip install flask_migrate Flask-Cors gunicorn
pip install python-dotenv

3. Création des fichiers principaux
1.main.py

2.models.py

3.Dossier routes/ avec :

    .students.py
    
    .grades.py

.4. config.py

5. .env

4. Initialisation de la base de données
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

Versionnement avec Git

git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/patricia243/ProjctAos.git
git push -u origin master

☁️ Déploiement sur Rende

1. Étapes
Créer un compte sur Render

Créer un nouveau Web Service connecté à ton repo GitHub

Définir les options :

Build Command :

bash
Copier
Modifier
pip install -r requirements.txt
Start Command :

bash
Copier
Modifier
gunicorn main:app
Render détectera automatiquement le fichier render.yaml

2. Contenu du fichier render.yaml

yaml
Copier
Modifier
services:
  - type: web
    name: flask-student-api
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "gunicorn main:app"
    envVars:
      - key: FLASK_ENV
        value: production
      - key: DATABASE_URL
        value: sqlite:///students.db
🔗 Lien vers le dépôt GitHub : https://github.com/patricia243/ProjctAos















