format:
	poetry run black app
	poetry run isort app

lint:
	poetry run black --check app
	poetry run isort --check-only app
	poetry run mypy app
	poetry run flake8 app

dev-run:
	docker compose up -d --build

dev-stop:
	docker compose down -v

restart:
	docker compose down
	docker compose up -d --build

run-test-db:
	docker run --env POSTGRES_USER=user --env POSTGRES_PASSWORD=password --env POSTGRES_DB=test_database --name test_backend_postgres -p 45432:5432 -d postgres:15.2-alpine
	docker run --name rtest_backend_redis -p 46379:6379 -d redis:7.0.11-alpine redis-server user user on +@all ~* &* >password

test:
	coverage run -m pytest -s ./app/tests
	coverage html

stop-test-db:
	docker rm --force test_backend_postgres
	docker rm --force test_backend_redis

build-backend:
	docker build --file=docker/Dockerfile --target=production .

prod-run: build-backend
	docker compose -f docker-compose.yaml up -d --build

prod-stop:
	docker compose -f docker-compose.yaml down -v
