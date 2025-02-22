# Contribuer au projet Empreinte Souffrance

## Installer Poetry

Plusieurs [méthodes d'installation](https://python-poetry.org/docs/#installation) sont décrites dans la documentation de poetry dont:

- avec pipx
- avec l'installateur officiel

Chaque méthode a ses avantages et inconvénients. Par exemple, la méthode pipx nécessite d'installer pipx au préable, l'installateur officiel utilise curl pour télécharger un script qui doit ensuite être exécuté et comporte des instructions spécifiques pour la completion des commandes poetry selon le shell utilisé (bash, zsh, etc...).

L'avantage de pipx est que l'installation de pipx est documentée pour linux, windows et macos. D'autre part, les outils installées avec pipx bénéficient d'un environment d'exécution isolé, ce qui est permet de fiabiliser leur fonctionnement. Finalement, l'installation de poetry, voire d'autres outils est relativement simple avec pipx.

### Installation de Poetry avec pipx

Suivre les instructions pour [installer pipx](https://pipx.pypa.io/stable/#install-pipx) selon ta plateforme (linux, windows, etc...)

Par exemple pour Ubuntu 23.04+:

    sudo apt update
    sudo apt install pipx
    pipx ensurepath

[Installer Poetry avec pipx](https://python-poetry.org/docs/#installing-with-pipx):

    pipx install poetry

### Installation de Poetry avec l'installateur officiel

L'installation avec l'installateur officiel nécessitant quelques étapes supplémentaires,
se référer à la [documentation officielle](https://python-poetry.org/docs/#installing-with-the-official-installer).

## (Optionnel) Installer pyenv

Pyenv est un outil permettant de gerer plusieurs versions de python facilement. 
Pour plus d'information, voir [pyenv](https://github.com/pyenv/pyenv-installer).

Vous pourrez ensuite choisir la version de python que vous voulez utiliser en utilisant la commande suivante:

    pyenv install 3.13
    pyenv local 3.13

## Utiliser Poetry

Installer les dépendances:

    poetry install --with dev

Ne pas tenir compte du message suivant:

    Warning: The current project could not be installed: No file/folder found for package suffering-footprint

## Lancer les precommit-hook localement

[Installer les precommit](https://pre-commit.com/)

    pre-commit run --all-files

## Installer task pour gérer les tâches

Suivre la documentation officielle : https://taskfile.dev/installation/

## Générer ou updater les traductions

Aller dans le dossier `backend`, puis :
    
    task translations-compile

Si vous ajoutez de nouvelles strings à traduire au projet, vous devrez utiliser `task translations-all` pour générer et mettre à jour les traductions.

Si vous êtes sous windows, il vous faudra lancer ces commandes dans un [git bash](https://gitforwindows.org/)

## Utiliser Tox pour tester votre code

Aller dans le dossier `backend`, puis (ne fonctionne pas actuellement, voir méthode alternative ci-dessous) :

    tox -vv

## Utiliser pytest pour tester votre code

Aller dans le dossier `backend`, puis :

    python -m pytest -vv

## Lancer le serveur

Aller dans le dossier `backend`, puis :

    task run-server

## Accéder à l'api

Exemple: http://127.0.0.1:8000/off/v1/knowledge-panel/1?lang=fr


# Architecture du projet

## Backend

Le dossier backend/ contient l'implémentation principale de l'application backend.

- `app/api/` : Définit les endpoints de l'API.
  - `app/api/open_food_facts` : Défini l'API qui interragit avec OFF.
  - À terme, nous aurons également un dossier pour l'API de notre site.
- `app/business/` : Gère la logique métier*.
- `app/config/` : Contient les fichiers de configuration.
- `app/locales/` : Gère la localisation et les traductions.
- `app/models/` : Définit les modèles de données.

Les dossiers business et models doivent suivre la même architecture que celui de l'API. Donc si vous ajoutez de la logique métier pour l'API OFF, elle devra être dans `app/business/open_food_facts`. Idem pour les models.

S'il y a de la logique métier commune (par exemple, le calculateur du score), cela peut être placé dans `app/business/common`.

(*) La logique métier représente l'ensemble des règles, traitements et calculs propres au domaine fonctionnel de l'application. Elle définit comment les données sont manipulées et les décisions sont prises pour répondre aux besoins des utilisateurs, indépendamment de l'interface ou du stockage des données.

## Tests

Le dossier `tests/` contient les tests unitaires pour assurer la stabilité du projet. 

L'arborescence du dossier test suit celle du dossier backend. Exemple : Si vous testez une route du fichier `backend/app/api/open_food_facts/routes.py`, votre test devra se trouver dans `tests/app/api/open_food_facts/test_routes.py`

Veuillez noter que vos fichiers tests doivent commencer par `test_`, et le nom de vos fonctions de tests également, pour être prises en compte par pytest.

## Scripts

Le dossier `scripts/` contient divers scripts utiles au projet.

## Poetry et Gestion des Dépendances

Le projet utilise Poetry pour la gestion des dépendances (pyproject.toml et poetry.lock).

## Automatisation

- `Taskfile.yml` : Définit des tâches automatisées (pour lancer le serveur, ou générer les traductions par exemple).
- `tox.ini` : Configuration pour exécuter les tests avec tox.
- `.pre-commit-config.yaml` : Configuration des hooks pre-commit.