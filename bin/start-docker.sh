#!/usr/bin/env bash
export DOCKER_CONFIG=${DOCKER_CONFIG:-docker/docker-compose.yml}
docker-compose -f $DOCKER_CONFIG up 
# Database migrations
echo "Create database migrations"
docker-compose -f $DOCKER_CONFIG run django python3 manage.py makemigrations
echo "Apply database migrations"
docker-compose -f $DOCKER_CONFIG run django python3 manage.py migrate
docker-compose -f $DOCKER_CONFIG run django python3 manage.py tests
docker-compose -f $DOCKER_CONFIG run django python3 manage.py loaddata ./dxlab/apps/core/fixtures/fixtures.json
docker-compose -f $DOCKER_CONFIG run -p 8000:8000 django python3 manage.py runserver
