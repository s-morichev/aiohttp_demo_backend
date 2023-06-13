help:              ## Показать помощь
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'


format:            ## Отформатировать код
	poetry run black app
	poetry run isort app

lint:              ## Запустить линтеры (mypy, flake8)
	poetry run black --check app
	poetry run isort --check-only app
	poetry run mypy app
	poetry run flake8 app

dev-run:           ## Запустить dev-версию (должен быть compose override)
	docker compose up -d --build
	sleep 3  # ждем запуск постгрес для применения миграций
	docker compose exec backend alembic upgrade head
	docker compose exec backend python3 db_insert_initial_data.py

dev-stop:          ## Остановить dev-версию (с удалением volume)
	docker compose down -v

restart:           ## Перезапустить dev-версию
	docker compose down
	docker compose up -d --build

run-test-db:       ## Запустить БД для тестов (постгрес, редис)
	docker compose -f docker-compose.test.yaml --env-file .env.test up -d test-backend-postgres test-backend-redis
	sleep 3  # ждем запуск постгрес для применения миграций
	docker compose -f docker-compose.test.yaml --env-file .env.test build test-backend
	docker compose -f docker-compose.test.yaml --env-file .env.test run --rm test-backend alembic upgrade head


test:              ## Запустить тесты (при установленных зависимостях)
	poetry run coverage run -m pytest ./app/tests
	poetry run coverage html

test-in-docker:    ## Запустить тесты в докере
	docker compose -f docker-compose.test.yaml --env-file .env.test build test-backend
	docker compose -f docker-compose.test.yaml --env-file .env.test run --rm test-backend coverage run -m pytest ./tests

stop-test-db:      ## Удалить БД для тестов (с удалением volume)
	docker compose -f docker-compose.test.yaml --env-file .env.test down -v

build-backend:
	docker build --file=docker/Dockerfile --target=production .

prod-run: build-backend
	docker compose -f docker-compose.yaml up -d --build

prod-stop:
	docker compose -f docker-compose.yaml down -v
