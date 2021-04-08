FROM python:3.9.4-alpine3.12 AS python

WORKDIR /app
COPY . .
COPY scripts/run.sh scripts/run

ENV KRAKEN_KEY_PATH='/app/kraken.key' 
ENV SETTINGS_PATH='/app/settings.json'

RUN sh scripts/requirements.sh 
RUN chmod +x scripts/run 

RUN echo '*/1 * * * * /app/scripts/run' > /etc/crontabs/root 

CMD crond -l 3 -f 