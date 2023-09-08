APP_ENV=local
APP_DEBUG=true
APP_URL=http://localhost
LOCAL_CORS_ALLOWED_ORIGINS="*"
CORS_ALLOWED_ORIGINS="example.com"

build:
	docker compose build --build-arg CORS_ALLOWED_ORIGINS=${LOCAL_CORS_ALLOWED_ORIGINS} --build-arg APP_ENV=${APP_ENV} --build-arg APP_DEBUG=${APP_DEBUG}

run:
	docker compose up -d --build=true

stop:
	docker compose down