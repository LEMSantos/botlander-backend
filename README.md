# botlander

Your package short description.

## Docker Quickstart

This app can be run completely using `Docker` and `docker-compose`. **Using Docker is recommended, as it guarantees the application is run using compatible versions of Python**. You can find out more at [Compose command-line reference](https://docs.docker.com/compose/reference/).

### Basics

To build and start a service running in background
```bash
docker-compose up -d service_name
```

To execute a command with a service container
```bash
docker-compose exec service_name [COMMAND]
```

To stop a service
```bash
docker-compose stop service_name
```

To stop and a service and remove its container
```bash
docker-compose down service_name
```

### Production

To run the production version of the project

```bash
docker-compose up -d prod
```

To run the botlander module of the project

```bash
docker-compose exec prod python -m botlander
```

### Development

To run the project development environment

```bash
docker-compose up -d dev
```

To execute botlander development routines

```bash
# [FOLDERS] = folder1 folder2 folder3 (optional to limit validation)
docker-compose exec dev flake8 --max-complexity=10 [FOLDERS]
docker-compose exec dev pytest --cov=botlander [MODULES_FOLDER] [TESTS_FOLDER]
docker-compose exec dev python -m botlander
```

## Features

* TODO

## Credits
* Lucas Eliaquim <lucas_m-santos@hotmail.com>
