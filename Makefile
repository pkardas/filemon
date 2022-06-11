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
