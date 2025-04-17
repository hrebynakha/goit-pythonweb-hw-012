include .env

install:
	@echo "Installing dependencies..."
	docker compose up -d
	@echo "Installing database..."
	- docker compose exec db sh -c "psql -U postgres -c 'create database contacts_app'"
	@echo "Running migrations..."
	docker compose exec app sh -c "alembic upgrade head"
updb:
	docker run --name hw012 -p 5432:5432 -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} -d postgres
newdb:
	docker exec -it hw012 sh -c "psql -U postgres -c 'create database contacts_app'"
	alembic upgrade head
migration:
	alembic revision --autogenerate -m "$m"
migrate:
	alembic upgrade head
f:
	black . --exclude=venv
run:
	python main.py
up:
	poetry export --without-hashes -f requirements.txt --output requirements.txt
	docker compose up -d
migr:
	@img=$$(docker ps -aqf "name=goit-pythonweb-hw-012_app") && \
	docker exec -it $$img sh -c "alembic upgrade head"
upredis:
	docker run --name redis-hw012 -p 6379:6379 -d redis:8.0-rc1
docrq:
	poetry export --without-hashes -f requirements.txt --output docs/requirements.txt --only "docs"
tst:
	pytest -v tests
reptest:
	pytest --cov=src tests/ --cov-report=html 