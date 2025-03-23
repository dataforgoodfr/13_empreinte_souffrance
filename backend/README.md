# Contributing to the Suffering Footprint project

The French version of this README is available here: [README_FR.md](README_FR.md).

## Install pre-commit

Follow the [official documentation](https://pre-commit.com/), or simply run:

    pip install pre-commit

Then, in the project's root directory (`13_empreinte_souffrance`), install the pre-commit hooks:

    pre-commit install

## (Optional but highly recommended) Installing pyenv

Pyenv is a tool that allows you to manage multiple Python versions easily.\
For more information, visit [pyenv](https://github.com/pyenv/pyenv-installer).

You can then select the Python version you want to use with the following commands:

    pyenv install 3.13
    pyenv global 3.13

## Installing uv

Follow one of the several [installation methods](https://docs.astral.sh/uv/getting-started/installation/) that are described in uv's documentation.

## Installing dependencies

Navigate to the `backend` directory and run:

    uv sync --all-groups

This will create a `.venv` virtual environment in the backend folder.

## Using the virtual environment in your IDE

To ensure your IDE automatically uses the virtual environment and finds the project dependencies, you need to configure it.

### If you are using VSCode

Open the command palette (Ctrl/Cmd + Shift + P), search for `Python: Select Interpreter`, then choose `Enter interpreter path` and type:

For Windows:

    backend/.venv/Scripts/Python.exe

For macOS and Linux:

    backend/.venv/bin/python

### If you are using PyCharm

Go to Settings, then Python Interpreter, click on Add Interpreter, select Existing venv, and choose `uv`, then specify the path to the Python executable in `.venv`:

For Windows:

    backend/.venv/Scripts/Python.exe

For macOS and Linux:

    backend/.venv/bin/python

## Using the virtual environment with uv

If you have configured your IDE, your shell should automatically use the virtual environment, allowing you to run commands that depend on it like this:

    pytest
    pre-commit run --all-files

If this is not the case, or if you encounter an issue, you can use `uv run` to execute a command (if you are in the backend directory).

    uv run your_command

Some examples used in this project:

    uv run pytest
    uv run pre-commit run --all-files

## Running pre-commit hooks locally

    uv run pre-commit run --all-files

## Installing Task for task management

Follow the official documentation [here](https://taskfile.dev/installation/).

## Generating or updating translations

Navigate to the `backend` directory and run:

    task translations-compile

If you add new translatable strings to the project, use:

    task translations-all

to generate and update translations.

If you're on Windows, you must run these commands in a [Git Bash](https://gitforwindows.org/).

## Run the tests

Navigate to the `backend` directory and run:

    task tests

## Alternative: Using pytest to test your code

Navigate to the `backend` directory and run:

    uv run pytest

## Running the server

Navigate to the `backend` directory and run:

    task run-server

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

    tests/app/api/open_food_facts/test_routes.py

Test files should start with `test_`, and test function names should also start with `test_` to be detected by pytest.

## Scripts

The `scripts/` directory contains various utility scripts for the project.

## uv and Dependency Management

This project uses uv to manage dependencies (`pyproject.toml` and `uv.lock`).

## Automation

- `Taskfile.yml`: Defines automated tasks (e.g., running the server or generating translations).
- `tox.ini`: Configuration for running tests with Tox.
- `.pre-commit-config.yaml`: Configuration for pre-commit hooks.
