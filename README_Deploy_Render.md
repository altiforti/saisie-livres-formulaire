# Déploiement de l'Application de Saisie de Livres (Formulaire Complet)

Cette application Flask permet de saisir des informations sur des livres (EAN, État, Rayon, Sous-rayon, Prix Mini, Prix Maxi) via un formulaire web et de les enregistrer dans une base Airtable.

## Structure des Fichiers

L'archive `book_entry_form_app.zip` que vous avez reçue contient le dossier `src/` avec la structure suivante :

```
src/
├── main.py               # Logique du serveur Flask (backend)
├── requirements.txt      # Dépendances Python
├── static/               # Dossier pour les fichiers statiques (CSS, JS, images - vide pour l'instant)
└── templates/
    └── index.html        # Page HTML du formulaire (frontend)
```

## Prérequis

*   Un compte [Render.com](https://render.com/) (ou une autre plateforme d'hébergement supportant Python/Flask).
*   Vos identifiants Airtable :
    *   Clé API Airtable (API Key)
    *   ID de votre Base Airtable (Base ID)
    *   Nom exact de votre Table Airtable (par défaut "SAISIE DE LIVRES" dans le code, mais configurable via variable d'environnement).
*   Un compte GitHub (ou GitLab/Bitbucket) pour héberger le code.

## Étapes de Déploiement sur Render.com

1.  **Préparer votre dépôt GitHub :**
    *   Créez un nouveau dépôt GitHub (par exemple, `saisie-livres-formulaire`).
    *   Décompressez l'archive `book_entry_form_app.zip` sur votre ordinateur.
    *   Copiez **tout le contenu du dossier `src`** (c'est-à-dire `main.py`, `requirements.txt`, le dossier `static` et le dossier `templates`) directement à la racine de votre nouveau dépôt GitHub.
    *   Poussez ces fichiers sur GitHub.

2.  **Créer un Web Service sur Render.com :**
    *   Connectez-vous à votre tableau de bord Render.
    *   Cliquez sur "New +" > "Web Service".
    *   Connectez votre compte GitHub et sélectionnez le dépôt que vous venez de créer (par exemple, `saisie-livres-formulaire`).
    *   Configurez les paramètres suivants :
        *   **Name :** Donnez un nom à votre application (ex: `saisie-livres-form`).
        *   **Region :** Choisissez une région (ex: Frankfurt).
        *   **Branch :** `main` (ou la branche où se trouve votre code).
        *   **Root Directory :** Laissez vide (car `main.py` est à la racine de votre dépôt).
        *   **Runtime :** `Python 3` (Render devrait le détecter).
        *   **Build Command :** `pip install -r requirements.txt` (Render le propose souvent par défaut).
        *   **Start Command :** `gunicorn main:app` (Gunicorn est un serveur WSGI robuste pour la production. Si vous préférez utiliser le serveur de développement Flask pour des tests simples, vous pouvez mettre `python main.py`, mais Gunicorn est recommandé. Le port est géré par Render).

3.  **Configurer les Variables d'Environnement :**
    *   Dans les paramètres de votre Web Service sur Render, allez dans la section "Environment".
    *   Ajoutez les variables d'environnement suivantes (cliquez sur "Add Environment Variable") :
        *   `AIRTABLE_API_KEY` : Votre clé API Airtable.
        *   `AIRTABLE_BASE_ID` : L'ID de votre base Airtable.
        *   `AIRTABLE_TABLE_NAME` : Le nom de votre table (par défaut, le code utilise "SAISIE DE LIVRES" si cette variable n'est pas définie, mais il est préférable de la spécifier ici).
        *   `PYTHON_VERSION` : `3.11` (pour correspondre à l'environnement de développement).

4.  **Déployer :**
    *   Cliquez sur "Create Web Service".
    *   Render va construire et déployer votre application. Cela peut prendre quelques minutes.
    *   Une fois le déploiement réussi, Render vous fournira une URL publique pour accéder à votre application (quelque chose comme `https://votre-nom-app.onrender.com`).

## Utilisation

Une fois l'application déployée :

1.  Ouvrez l'URL fournie par Render dans votre navigateur.
2.  Le formulaire de "SAISIE DE LIVRES avec ean" s'affichera.
3.  Remplissez les champs EAN, État, Rayon, sous rayon (optionnel), Prix Mini (optionnel) et Prix Maxi (optionnel).
4.  Cliquez sur "Envoyer".
5.  Un message de succès ou d'erreur s'affichera.
6.  Le bouton "Effacer le formulaire" permet de réinitialiser tous les champs.

## Notes importantes

*   Le port utilisé dans le code (`main.py`) est 5002 par défaut si la variable `PORT` n'est pas définie par l'environnement. Render.com gère généralement l'assignation du port automatiquement.
*   Assurez-vous que les noms des champs dans Airtable (`EAN`, `ETAT`, `RAYON`, `sous rayon`, `PRIX MINI`, `PRIX MAXI`) correspondent exactement à ceux définis dans le fichier `main.py` (variables `FIELD_...`).
*   Les champs `PRIX MINI` et `PRIX MAXI` dans Airtable doivent être de type **Devise (Currency)** ou **Numérique (Number)** pour que l'application fonctionne correctement.

N'hésitez pas si vous avez des questions lors du déploiement !
