#!/bin/bash

#echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
#docker push USER/REPO


docker ps
docker container ls
sudo docker login --username $HEROKU_DOCKER_USERNAME --password $HEROKU_AUTH_TOKEN registry.heroku.com
sudo docker tag pure-reef-43194:latest registry.heroku.com/pure-reef-43194/django
sudo docker inspect --format='{{.Id}}' registry.heroku.com/pure-reef-43194/django
if [ $TRAVIS_BRANCH == "master" ] && [ $TRAVIS_PULL_REQUEST == "false" ]; then sudo docker push registry.heroku.com/pure-reef-43194/django; fi

#    - heroku addons:create heroku-postgresql:hobby-dev -a mywebapp0

#    - heroku run container:release web -a webapp-dpdth
#    - heroku run python manage.py makemigrations -a webapp-dpdth
#    - heroku run python manage.py migrate -a webapp-dpdth
chmod +x heroku-container-release.sh

sudo chown $USER:docker ~/.docker
sudo chown $USER:docker ~/.docker/config.json
sudo chmod g+rw ~/.docker/config.json

./heroku-container-release.sh