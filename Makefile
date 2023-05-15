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
	sleep 3  # ждем запуск постгрес для применения миграций
	docker compose exec backend alembic upgrade head
	docker compose exec backend python3 db_insert_initial_data.py

dev-stop:
	docker compose down -v

restart:
	docker compose down
	docker compose up -d --build

run-test-db:
	docker compose -f docker-compose.test.yaml --env-file .env.test up -d test-backend-postgres test-backend-redis
	sleep 3  # ждем запуск постгрес для применения миграций
	docker compose -f docker-compose.test.yaml --env-file .env.test build test-backend
	docker compose -f docker-compose.test.yaml --env-file .env.test run --rm test-backend alembic upgrade head


test:
	poetry run coverage run -m pytest -s ./app/tests
	poetry run coverage html

test-in-docker:
	docker compose -f docker-compose.test.yaml --env-file .env.test build test-backend
	docker compose -f docker-compose.test.yaml --env-file .env.test run --rm test-backend coverage run -m pytest -s ./tests

stop-test-db:
	docker compose -f docker-compose.test.yaml --env-file .env.test down -v

build-backend:
	docker build --file=docker/Dockerfile --target=production .

prod-run: build-backend
	docker compose -f docker-compose.yaml up -d --build

prod-stop:
	docker compose -f docker-compose.yaml down -v
