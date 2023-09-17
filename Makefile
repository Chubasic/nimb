APP_ENV=local
APP_URL=http://localhost
CORS_ALLOWED_ORIGINS="*"

build:
	docker compose build --build-arg CORS_ALLOWED_ORIGINS=${CORS_ALLOWED_ORIGINS} --build-arg APP_ENV=${APP_ENV}

run:
	docker compose up -d --build=true

stop:
	docker compose down

test:
	pytest