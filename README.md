### Тестовое задание

Демо бэкенд на aiohttp

### Стэк

Aiohttp, SQLAlchemy, PostgreSQL, Redis, Docker, pytest

### Функционал

Используются автоформатирование кода с помощью black и
isort, проверки линтерами mypy (с флагом strict) и wemake-python-styleguide
(с некоторыми исключениями), измеряется покрытие тестами (coverage + pytest).

- Таблицы Users(Имя, Фамилия, логин, пароль, Дата Рождения, Дата регистрации,
роль), Roles(имя роли), History(id, old, new)
- При старте приложения создаются роли Admin, User и добавлется администратор
- На таблицу Users повешен триггер, который сохраняет изменения в
таблице History
- Авторизация по логину и паролю
- CRUD операции на таблицы Users, Roles
- Используются сессии (хранятся в редисе)
- Настроены разрешения: пользователь работает только с таблицей users со своим
аккаунтом, администратор со всеми таблицами
- Есть возможность использовать CRUD не точечно (частично, только read)
- Запуск в docker compose
- Используется Makefile для выполнения основных команд
- Написаны тесты (частично, см. бэклог), тесты можно запускать локально и в докере
- Подключены миграции alembic

Swagger не сделан, можно добавить с помощью aiohttp-swagger, пример моего опыта
по написанию swagger документации можно посмотреть [тут](https://github.com/s-morichev/async_api_and_auth/blob/main/auth/docs/openapi.yaml)


### Бэклог

- Добавить тесты на ошибки, сейчас проверяется в основном нормальное функционирование
приложения ("хорошие" входные данные)
- Добавить пагинацию при чтении сразу нескольких объектов
- Добавить nginx

### Запуск

Создать env файлы
- `cp .env.example .env` используется для запуска приложения
- `cp .env.local.example .env.local` используется в алембике для подключения к постгресу
при создании миграций
- `cp .env.test.example .env.test` используется для тестирования в докере
- `cp .env.test.local.example .env.test.local` используется для тестирования на хосте

Создать acl для редиса
- `cp redis.acl.example redis.acl`

Запустить и остановить приложение с удалением контейнеров
- `make dev-run`
- `make dev-stop`

Запустить и удалить контейнеры с тестовыми базами данных
- `make run-test-db`
- `make stop-test-db`

Выполнить тесты (при запущенных тестовых базах)
- `make test-in-docker`

### Миграции

Для создания миграций алембику необходимо соединение c базой данных,
поэтому нужно экспортировать переменную окружения BACKEND_PG_DSN
перед запуском команд алембика либо создать локальный .env.local
файл и загружать переменную из него. Также должен быть установлен
psycopg2.

 - Создать миграцию `alembic revision --autogenerate -m "migration name"`
 - Применить все миграции `alembic upgrade head`
