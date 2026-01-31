# Project Management API

API REST de gestion de projets et de tâches développée avec **FastAPI**, intégrant une authentification **JWT**, une gestion des rôles et une base de données versionnée via **Alembic**.

Ce projet est un **projet personnel / portfolio**, conçu selon des pratiques proches d’un environnement professionnel.

---

## Fonctionnalités

- Authentification sécurisée par JWT
- Gestion des rôles :
  - **admin**
  - **manager**
  - **member**
- Gestion des utilisateurs (admin uniquement)
- Gestion des projets
- Gestion des tâches par projet
- Attribution des tâches aux utilisateurs
- Contrôle d’accès basé sur les rôles
- Base de données gérée exclusivement par Alembic
- Documentation interactive Swagger

---

## Stack technique

- Python **3.13.8**
- FastAPI
- SQLAlchemy
- Alembic (migrations)
- JWT (OAuth2 Password Flow)
- SQLite (par défaut)

---

## Structure du projet

```text
project-root/
│
├── backend/
│ ├── app/
│ │ ├── core/ # Configuration, sécurité, dépendances
│ │ ├── models/ # Modèles SQLAlchemy
│ │ ├── database/ # Session DB, engine, connexion
│ │ ├── schemas/ # Schémas Pydantic
│ │ ├── routers/ # Endpoints API
│ │ └── main.py # Point d’entrée FastAPI
│ │
│ ├── migrations/ # Migrations Alembic
│ ├── alembic.ini
│ └── create_admin.py # Script de création d’un compte admin
│
├── .env.example
├── requirements.txt
└── README.md
 ``` 

---

## Prérequis

- Git
- **Python 3.13.8**
- Terminal (PowerShell recommandé sous Windows)

---

## Installation et premier lancement

> ⚠️ Important  
> La base de données est **gérée uniquement par Alembic**.  
> Aucune table n’est créée automatiquement au démarrage.

### 


1️⃣ Cloner le dépôt

git clone <URL_DU_DEPOT>

2️⃣ Se placer dans le dossier du projet

cd <nom_du_dossier>

3️⃣ Créer un environnement virtuel Python

python -m venv <nom_de_la_vm>

4️⃣ Activer l’environnement virtuel (Windows)

.\<nom_de_la_vm>\Scripts\Activate

5️ Installer les dépendances

pip install -r requirements.txt



### Configuration de l’environnement :



1️⃣ Renommer le fichier d’exemple :

Rename-Item -Path .env.example -NewName .env

2️⃣ Puis éditer le fichier .env (exemple) :

DATABASE_URL=sqlite:///./app.db
SECRET_KEY=UNE_CLE_SECRETE_LONGUE_ET_ALEATOIRE
ACCESS_TOKEN_EXPIRE_MINUTES=60


📌 Le fichier .env :

n’est jamais versionné

est propre à chaque environnement

Initialisation de la base de données

3️⃣ Se placer dans le dossier backend :

cd backend

4️⃣ Appliquer les migrations :

alembic upgrade head

➡️ Cette commande crée toutes les tables nécessaires.

5️ Lancer l’API

uvicorn app.main:app --reload


API : http://127.0.0.1:8000

Documentation Swagger : http://127.0.0.1:8000/docs

- Création d’un compte administrateur

Un script dédié est fourni pour créer ou mettre à jour un compte administrateur.

Exemple (Windows PowerShell)

$env:ADMIN_EMAIL="admin@exemple.com"
$env:ADMIN_PASSWORD="MotDePasseLongEtSecurise123!"
python backend/create_admin.py


### Contraintes :

Mot de passe minimum : 12 caractères

Aucun identifiant codé en dur dans le code

Authentification API

Endpoint : POST /api/v1/auth/login

OAuth2 Password Flow

Le token JWT doit être transmis via l’en-tête HTTP :

Authorization: Bearer <access_token>

### Bonnes pratiques appliquées :

Secrets exclus du dépôt (.gitignore)

Aucun mot de passe codé en dur

Migrations de base de données contrôlées

Séparation claire des responsabilités

Code lisible et maintenable

Objectif du projet

Démontrer des compétences backend solides

Appliquer des pratiques professionnelles réalistes

Servir de base pour des évolutions futures

Être présentable dans un contexte portfolio / recrutement
