# Foodgram - Продуктовый помощник

Foodgram — это онлайн-сервис, где пользователи могут публиковать рецепты, подписываться на других авторов, добавлять рецепты в избранное и формировать список покупок для приготовления выбранных блюд.

## Технологии

- Python 3.12
- Django 5.1
- Django REST Framework 3.15
- djoser (аутентификация по токенам)
- PostgreSQL
- Docker & Docker Compose
- Nginx
- GitHub Actions (CI/CD)

## Локальный запуск проекта (без Docker)

1. **Клонируйте репозиторий:**
   ```bash
   git clone git@github.com:Tashastr/foodgram.git
   cd foodgram
   ```

2. **Создайте виртуальное окружение и активируйте его:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate   # для Linux/Mac
   # или venv\Scripts\activate для Windows
   ```

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Создайте файл `.env` в папке `backend` (скопируйте `.env.example` и заполните):**
   ```bash
   cp .env.example .env
   ```
   Пример содержимого `.env`:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Выполните миграции и создайте суперпользователя:**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Загрузите ингредиенты из CSV:**
   ```bash
   python manage.py load_ingredients
   ```

7. **Запустите сервер разработки:**
   ```bash
   python manage.py runserver
   ```

8. **Проект будет доступен по адресу:** `http://127.0.0.1:8000`

## Запуск в контейнерах Docker (продакшен)

1. **Создайте файл `.env` в корневой папке проекта (не в `backend`!) на основе `.env.example`.**
   Пример содержимого:
   ```
   SECRET_KEY=ваш-секретный-ключ
   DEBUG=False
   ALLOWED_HOSTS=ваш-домен,158.160.227.215
   POSTGRES_DB=foodgram
   POSTGRES_USER=foodgram_user
   POSTGRES_PASSWORD=secure_password
   DB_HOST=db
   DB_PORT=5432
   DOCKER_USERNAME=ваш_логин_на_docker_hub
   ```

2. **Запустите контейнеры:**
   ```bash
   docker-compose -f docker-compose.production.yml up -d
   ```

3. **Выполните миграции и соберите статику:**
   ```bash
   docker exec foodgram-backend python manage.py migrate
   docker exec foodgram-backend python manage.py collectstatic --noinput
   ```

4. **Создайте суперпользователя (при необходимости):**
   ```bash
   docker exec -it foodgram-backend python manage.py createsuperuser
   ```

5. **Проект будет доступен по IP вашего сервера или домену.**

## API и документация

После запуска проекта документация API доступна по адресу:  
`/api/docs/` (например, `http://localhost/api/docs/`).

### Основные эндпоинты

- `POST /api/users/` – регистрация пользователя
- `POST /api/auth/token/login/` – получение токена
- `GET /api/users/me/` – профиль текущего пользователя
- `GET /api/tags/` – список тегов
- `GET /api/ingredients/` – список ингредиентов (с поиском по `name`)
- `GET /api/recipes/` – список рецептов (с фильтрацией по тегам, избранному, корзине, автору)
- `POST /api/recipes/` – создание рецепта (только для авторизованных)
- `POST /api/recipes/{id}/favorite/` – добавить рецепт в избранное
- `POST /api/recipes/{id}/shopping_cart/` – добавить рецепт в список покупок
- `GET /api/recipes/download_shopping_cart/` – скачать список покупок (файл .txt)

## Примеры запросов

**Регистрация пользователя:**
   ```bash
   curl -X POST http://localhost/api/users/ \
    -H "Content-Type: application/json" \
    -d '{"email":"user@example.com","username":"user","first_name":"Иван","last_name":"Иванов","password":"pass123"}'
   ```

**Получение токена:**
   ```bash
   curl -X POST http://localhost/api/auth/token/login/ \
    -H "Content-Type: application/json" \
    -d '{"email":"user@example.com","password":"pass123"}'
   ```
