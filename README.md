# dxlab
	dxlab challenge

## Stack

* Python3.8
* Django3
* Docker
* MySQL

## Dependencies

* dj_database_url
* docker-compose
* djangorestframework
* drf-generators
* [wait-for-it](https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh)
* [docker-python38-ubuntu](https://github.com/matthewfeickert/Docker-Python3-Ubuntu)

## Setup for development env
	$ python manage.py loaddata dxlab/apps/core/fixtures/fixtures.json

	$ python manage.py dumpdata appname --indent=4 --output=<path-to-your-output-file>

## Admin Painel
[Login](http://127.0.0.1:8000/admin/)	

## API Access

Default store user credentials:
* username: diogosimao@gmail.com
* password: lembrar

[Local login](http://127.0.0.1:8000/core/api/auth/login/) or https://pure-reef-43194.herokuapp.com/core/api/auth/login

## API Doc

OpenAPI Documentation:
* [Local API Doc](http://127.0.0.1:8000/core/api/docs/swagger-ui/) or https://pure-reef-43194.herokuapp.com/core/api/docs/swagger-ui/


## Docker

It will need some extras. See requirements/docker.txt

	$ pip install -r requirements/docker.txt

	$ . ./bin/start-docker-development-server.sh

## Travis

[CI](https://travis-ci.org/github/disimao/dxlab/)

## Heroku

[CD](https://pure-reef-43194.herokuapp.com/)
