ARG CORS_ALLOWED_ORIGIN
ARG NAME
ARG APP_ENV
ARG APP_DEBUG
FROM python:3.11-alpine

WORKDIR /app
# Set environment variables
ENV CORS_ALLOWED_ORIGIN=${CORS_ALLOWED_ORIGIN}

# Set flask environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=${APP_DEBUG}
ENV FLASK_RUN_HOST=0.0.0.0

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python", "app.py" ]