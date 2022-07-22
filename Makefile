test-flake8:
	docker-compose run --rm filemon flake8 .

test-mypy:
	docker-compose run --rm filemon mypy .

test-pytest:
	docker-compose run --rm filemon pytest .

reload-deps:
	docker-compose build

alembic-init:
	docker-compose run --rm filemon alembic init alembic

alembic-autogenerate:
	docker-compose run --rm filemon alembic revision --autogenerate -m "Change me!"

alembic-upgrade:
	docker-compose run --rm filemon alembic upgrade head

alembic-downgrade:
	docker-compose run --rm filemon alembic downgrade -1

ec2-stop:
	sudo docker stop $$(sudo docker ps -aq)

ec2-pull:
	git pull

ec2-build:
	sudo docker-compose build api

ec2-migrate:
	sudo docker-compose run --rm filemon alembic upgrade head

ec2-run:
	sudo docker-compose up --detach api

ec2-manual-deploy:
	make ec2-stop && make ec2-pull && make ec2-build && make ec2-migrate && make ec2-run
