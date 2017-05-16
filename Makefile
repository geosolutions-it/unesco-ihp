# bring up the services
up:
	docker-compose up -d

build:
	docker-compose build django
	docker-compose build celery

# set up the database tables
sync:
	docker-compose run django python manage.py makemigrations --noinput
	docker-compose exec django python manage.py migrate account --noinput
	docker-compose run django python manage.py migrate --noinput

wait:
	sleep 5

logs:
	docker-compose logs --follow

down:
	docker-compose down

test:
	docker-compose run django python manage.py test --failfast

reset: down up wait sync

hardreset: pull build reset
