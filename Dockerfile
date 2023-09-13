ARG CORS_ALLOWED_ORIGIN
ARG NAME
ARG APP_ENV
# FROM python:3.11-alpine
FROM python:3.11-slim-bullseye

WORKDIR /app
# Set environment variables
ENV CORS_ALLOWED_ORIGIN=${CORS_ALLOWED_ORIGIN}

# Set flask environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=false
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_APP_NAME="nimble"

RUN apt-get update && apt-get install -y supervisor

RUN mkdir -p /var/log/supervisor
RUN mkdir -p /etc/supervisor/conf.d

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf


COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

VOLUME /var/log

EXPOSE 5000 5672 15672

RUN printenv | grep -v "no_proxy" >> /etc/environment
# CMD ["/usr/bin/supervisord"]
CMD ["python", "-u", "app.py"]