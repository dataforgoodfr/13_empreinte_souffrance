# Contributing to the Suffering Footprint project

The French version of this README is available here: [README_FR.md](README_FR.md).

## Installing Poetry

Several [installation methods](https://python-poetry.org/docs/#installation) are described in Poetry's documentation, including:

- Using pipx
- Using the official installer

Each method has its pros and cons. For example, the pipx method requires installing pipx beforehand, while the official installer uses `curl` to download a script that must then be executed and includes specific instructions for enabling Poetry command completion depending on the shell used (bash, zsh, etc.).

The advantage of pipx is that its installation is well-documented for Linux, Windows, and macOS. Additionally, tools installed with pipx benefit from an isolated execution environment, ensuring reliability. Finally, installing Poetry (and other tools) is relatively simple with pipx.

### Installing Poetry with pipx

Follow the instructions to [install pipx](https://pipx.pypa.io/stable/#install-pipx) according to your platform (Linux, Windows, etc.).

For example, on Ubuntu 23.04+:

```
sudo apt update
sudo apt install pipx
pipx ensurepath
```

[Install Poetry using pipx](https://python-poetry.org/docs/#installing-with-pipx):

```
pipx install poetry
```

### Installing Poetry with the official installer

Since this method requires additional steps, refer to the [official documentation](https://python-poetry.org/docs/#installing-with-the-official-installer).

## (Optional) Installing pyenv

Pyenv is a tool that allows you to manage multiple Python versions easily.\
For more information, visit [pyenv](https://github.com/pyenv/pyenv-installer).

You can then select the Python version you want to use with the following commands:

```
pyenv install 3.13
pyenv local 3.13
```

## Using Poetry

To install dependencies:

```
poetry install --with dev
```

Ignore the following message:

```
Warning: The current project could not be installed: No file/folder found for package suffering-footprint
```

## Running pre-commit hooks locally

[Install pre-commit](https://pre-commit.com/)

```
pre-commit run --all-files
```

## Installing Task for task management

Follow the official documentation [here](https://taskfile.dev/installation/).

## Generating or updating translations

Navigate to the `backend` directory and run:

```
task translations-compile
```

If you add new translatable strings to the project, use:

```
task translations-all
```

to generate and update translations.

If you're on Windows, you must run these commands in a [Git Bash](https://gitforwindows.org/).

## Using Tox to test your code

Navigate to the `backend` directory and run (currently not working, see alternative below):

```
tox -vv
```

## Using pytest to test your code

Navigate to the `backend` directory and run:

```
python -m pytest -vv
```

## Running the server

Navigate to the `backend` directory and run:

```
task run-server
```

## Accessing the API

Example: <http://127.0.0.1:8000/off/v1/knowledge-panel/1?lang=fr>


# Project Architecture

## Backend

The `backend/` directory contains the main implementation of the backend application.

- `app/api/`: Defines API endpoints.
  - `app/api/open_food_facts/`: Defines the API that interacts with OFF.
  - In the future, there will also be a directory for our site's API.
- `app/business/`: Handles business logic **(*)**.
- `app/config/`: Contains configuration files.
- `app/locales/`: Manages localization and translations.
- `app/models/`: Defines data models.

The `business` and `models` directories should follow the same structure as the API directory. So, if you add business logic for the OFF API, it should go in `app/business/open_food_facts`. The same applies to models.

If there is shared business logic (e.g., a score calculator), it can be placed in `app/business/common`, for example.

**(*)** Business logic represents all the rules, processing, and calculations specific to the application's functional domain. It defines how data is manipulated and decisions are made to meet user needs, independently of the interface or data storage.

## Tests

The `tests/` directory contains unit tests to ensure project stability.

The directory structure mirrors that of the backend. Example: If you're testing a route from `backend/app/api/open_food_facts/routes.py`, your test should be placed in:

```
tests/app/api/open_food_facts/test_routes.py
```

Test files should start with `test_`, and test function names should also start with `test_` to be detected by pytest.

## Scripts

The `scripts/` directory contains various utility scripts for the project.

## Poetry and Dependency Management

This project uses Poetry to manage dependencies (`pyproject.toml` and `poetry.lock`).

## Automation

- `Taskfile.yml`: Defines automated tasks (e.g., running the server or generating translations).
- `tox.ini`: Configuration for running tests with Tox.
- `.pre-commit-config.yaml`: Configuration for pre-commit hooks.
