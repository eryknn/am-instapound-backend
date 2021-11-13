help:										## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

create-superuser:							## Run manage.py createsuperuser
	docker-compose -f local.yml exec django python manage.py createsuperuser

makemigrations:								## Run manage.py makemigrations
	docker-compose -f local.yml exec django python manage.py makemigrations

migrate:									## Run manage.py migrate
	docker-compose -f local.yml exec django python manage.py migrate

make-and-migrate: makemigrations migrate	## Run makemigrations & migrate

dev-django-sh:								## open django container shell
	docker-compose -f local.yml exec django bash

dev-reload-database:
	docker-compose -f local.yml rm -fsv postgres
	docker volume rm -f am_instapound_backend_local_postgres_data
	docker-compose -f local.yml up -d postgres
	sleep 1
	docker-compose -f local.yml exec django python manage.py migrate
# 	docker-compose -f local.yml exec django python ./manage.py loaddata ./fixtures/*.yaml --format=yaml
