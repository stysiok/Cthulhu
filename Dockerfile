FROM python:3.9.4-alpine3.12 AS python

WORKDIR /app
COPY . .

ENV KRAKEN_KEY_PATH='/app/kraken.key' \
    SETTINGS_PATH='/app/settings.json'

RUN sh scripts/requirements.sh \
    chmod +x scripts/run.sh \
    echo '*/1 * * * * sh /app/scripts/run.sh' > /etc/crontabs/root 

CMD crond -l 2 -f