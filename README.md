# Gestionnaire de Contacts

Un gestionnaire de contacts simple développé en Python avec Flask et SQLAlchemy. Ce projet permet aux utilisateurs de s'inscrire, de se connecter et de gérer leurs contacts personnels.

## Fonctionnalités

- **Authentification :**
  - Inscription d'utilisateurs avec mot de passe sécurisé.
  - Connexion et déconnexion sécurisées.
  
- **Gestion des Contacts :**
  - Ajouter un nouveau contact avec un nom, un email et un numéro.
  - Modifier les informations d'un contact existant.
  - Supprimer un contact.
  - Afficher la liste des contacts associés à un utilisateur connecté.

- **Validation :**
  - Empêche la duplication des contacts avec le même numéro pour un utilisateur.

## Prérequis

- Python 3.8 ou version supérieure.
- Un environnement PostgreSQL configuré.
- Les bibliothèques Python suivantes :
  - Flask
  - Flask-SQLAlchemy
  - Werkzeug

## Installation

1. Clonez le dépôt :
   ```bash
   git clone <URL_DU_DEPOT>
   cd gestionnaire-de-contacts
   ```

2. Créez un environnement virtuel et activez-le :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sous Windows : venv\Scripts\activate
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Configurez la base de données PostgreSQL :
   - Assurez-vous que PostgreSQL est installé et en cours d'exécution.
   - Modifiez `app.config["SQLALCHEMY_DATABASE_URI"]` dans le fichier principal pour refléter vos identifiants PostgreSQL.

5. Créez les tables de la base de données :
   ```bash
   flask shell
   db.create_all()
   exit
   ```

## Lancer l'application

Exécutez l'application en mode de développement :
```bash
python app.py
```

L'application sera accessible à l'adresse : [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Structure du Projet

```
gestionnaire-de-contacts/
├── app.py              # Fichier principal de l'application
├── templates/          # Dossier des templates HTML
├── static/             # Fichiers CSS et JavaScript
├── venv/               # Environnement virtuel Python
├── requirements.txt    # Liste des dépendances Python
└── README.md           # Documentation du projet
```

## Contributions

Les contributions sont les bienvenues ! Veuillez soumettre vos propositions via des pull requests.

## Licence

Ce projet est sous licence MIT. Consultez le fichier `LICENSE` pour plus d'informations.
