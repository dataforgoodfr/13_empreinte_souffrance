# Template DataForGood

This file will become your README and also the index of your
documentation.

# Contributing

## Installer Poetry

Plusieurs [méthodes d'installation](https://python-poetry.org/docs/#installation) sont décrites dans la documentation de poetry dont:

- avec pipx
- avec l'installateur officiel

Chaque méthode a ses avantages et inconvénients. Par exemple, la méthode pipx nécessite d'installer pipx au préable, l'installateur officiel utilise curl pour télécharger un script qui doit ensuite être exécuté et comporte des instructions spécifiques pour la completion des commandes poetry selon le shell utilisé (bash, zsh, etc...).

L'avantage de pipx est que l'installation de pipx est documentée pour linux, windows et macos. D'autre part, les outils installées avec pipx bénéficient d'un environment d'exécution isolé, ce qui est permet de fiabiliser leur fonctionnement. Finalement, l'installation de poetry, voire d'autres outils est relativement simple avec pipx.

Cependant, libre à toi d'utiliser la méthode qui te convient le mieux ! Quelque soit la méthode choisie, il est important de ne pas installer poetry dans l'environnement virtuel qui sera créé un peu plus tard dans ce README pour les dépendances de la base de code de ce repo git.

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
Pour plus d'information, voir [pyenv](https://pyenv.run/)

Vous pourrez ensuite choisir la version de python que vous voulez utiliser en utilisant la commande suivante:

    pyenv install 3.13
    pyenv local 3.13

## Utiliser Poetry

Installer les dépendances:

    poetry install --with dev

Ne pas tenir compte du message suivant:

`Warning: The current project could not be installed: No file/folder found for package suffering-footprint`

## Lancer les precommit-hook localement

[Installer les precommit](https://pre-commit.com/)

    pre-commit run --all-files

## Installer task pour gérer les tâches

Suivre la documentation officielle: https://taskfile.dev/installation/

## Générer ou updater les traductions

Aller dans le dossier `backend`, puis:

Dans l'ordre :

    task translations-extract
    task translations-update
    task translations-compile

Ou, pour tout faire d'un coup :
    
    task translations-all

## Utiliser Tox pour tester votre code

Aller dans le dossier `backend`, puis (ne fonctionne pas actuellement, voir méthode alternative ci-dessous):

    tox -vv

## Utiliser pytest pour tester votre code

Aller dans le dossier `backend`, puis:

    python -m pytest -vv

## Lancer le serveur

Aller dans le dossier `backend`, puis:

    task run-server

## Accéder à l'api

Exemple: http://127.0.0.1:8000/off/v1/knowledge-panel/1?lang=fr