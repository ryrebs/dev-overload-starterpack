## Django alternative structure

Using this project as a project template.

`$ django-admin startproject --template=PATH/TO/Collection-of-boilerplates/django-appp <project-name>`

\*_Notes_

- Placeholder files `foldername+placeholder` e.g. _logplaceholder_ are there to emphasize that the dir should be present, thus must be included in the repo.

---

A. Setup

1.  Install python [poetry](https://python-poetry.org/)

2.  Install dependencies:

        $ poetry install

B. Creating apps

1.  On your apps folder: `project_name/apps/`

        $ ../manage.py startapp apps/<app-name>

C. Running

1. Local: `poetry run ./manage.py runserver`

2. Prod: `poetry run gunicorn config.wsgi`
