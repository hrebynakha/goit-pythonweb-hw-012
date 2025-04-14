include .env

db:
	docker run --name hw08 -p 5432:5432 -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} -d postgres
migration:
	alembic revision --autogenerate -m $$m
migrate:
	alembic upgrade head
f:
	black . --exclude=venv
run:
	python main.py
up:
	poetry export --without-hashes -f requirements.txt --output requirements.txt
	docker-compose up -d
migr:
	@img=$$(docker ps -aqf "name=goit-pythonweb-hw-10_app") && \
	docker exec -it $$img sh -c "alembic upgrade head"
