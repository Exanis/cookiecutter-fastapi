# cookiecutter-fastapi
A simple and lightweight cookiecutter template for FastAPI

## Features

- [x] Docker
- [x] Github pipelines for test, build and release
- [x] Pre-commit hooks
- [x] Automatic changelog generation
- [x] Postgres support with simple migration-like system

## Usage

```bash
pip install cookiecutter
cookiecutter gh:Exanis/cookiecutter-fastapi
cd my-new-project
poetry install --only=dev
```

## Options

- `repo_name`: Name of your repository / your project (will be the name of the folder created by the cookiecutter)
- `description`: A short description of your project. Mostly used in the README.md
- `full_name`: Your full name
- `email`: Your email
- `registry`: The registry where you want to push your docker image
- `generate_changelog`: If set to yes, the release workflow will generate a changelog file (see below)
- `update_version_on_release`: If set to yes, the release workflow will update the version number on release (see below)
- `use_openapi`: If set to yes, the openapi endpoint will be enabled
- `use_docs`: If set to yes, the docs endpoint will be enabled
- `use_redoc`: If set to yes, the redoc endpoint will be enabled

## Changelog

If you set `generate_changelog` to yes, the release workflow will generate a changelog file. The changelog will be generated from the commit messages. The commit messages must follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.

For this step to work, you must generate a `PUBLISH_TOKEN` (see below).

## Version

If you set `update_version_on_release` to yes, the release workflow will update the version number on release. The version number will be updated in the `pyproject.toml` file and in the `__init__.py` file at the root of the project.

For this step to work, you must generate a `PUBLISH_TOKEN` (see below).

## Github secrets

If you have enabled the changelog or the version update, you must generate a `PUBLISH_TOKEN` and add it to your repository secrets. This token must have the `repo` and `workflow` scope. This can be done by going to your Github's settings => Developer settings => Personal access tokens => Generate new token.

## Workflows

### Tests

This workflow will run the tests and the linter on every pull request on the repository.

It includes the following steps:
 - Testing your code using `pytest` (with the default configuration, that includes a coverage test with a minimum of 100% - you can change that in the `pyproject.toml` file)
 - Use `pylint` to check the code quality
 - Use `mypy` to check typing
 - Use `bandit` to check for (some) security issues

### Build

This workflow will build the docker image and push it to the registry. It is triggered on every push to the `main` branch. The image will be tagged as "edge".

### Release

This workflow will build the docker image and push it to the registry. It may also
create a changelog and update the version (creating a new pull request) if you have
enabled those options. It is triggered when you push a tag starting with "v".

## Choices

### Poetry

Poetry is used to manage the dependencies and the virtual environment. It is a very good alternative to pipenv and pip-tools.

### Pre-commit

Pre-commit is used to run the linters and the formatters before each commit.

### Migrations / Databases

We are not using Alembic, neither SQLAlchemy, in this cookiecutter. We are using a very simple migration-like system. The idea is to have a `migrations` folder where you can put your migrations. Each migration is a SQL file. The migrations are applied in alphabetical order. The migrations are applied when the application starts.

The reason for this choice is that while SQLAlchemy is a real good ORM, as any ORM built for multiple databases support, it is not very good at handling specificities of each database. For example, it is not possible to use the `RETURNING` clause in PostgreSQL with SQLAlchemy. This is a very useful clause that allows you to get the inserted row in the same query as the insert. This is not possible with SQLAlchemy. This is why we are not using it.

This cookiecutter is made to be used with PostgreSQL. If you want to use another database, you will have to change the `migrations` folder and the `tools/migrate.py` file.

### Healthcheck

The default router included in the fastapi app is the healthcheck router. It is meant both as a healthcheck endpoint and as a documentation endpoint. However, this healthcheck is not used in the Dockerfile, you will have to add it yourself if you want to.

The reason behind this choice is that using an healthcheck in Docker require to install curl (or create a custom equivalent in python). However, this lead to an increase in the image's size that may be unwanted (especially if you are doing the healthcheck in a Kubernetes cluster).