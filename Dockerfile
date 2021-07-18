FROM python:3.9.4-alpine3.12 AS build

WORKDIR /app
COPY . .

RUN mkdir settings
RUN mv ./settings.json ./settings/settings.json

COPY scripts/run.sh scripts/run

ENV KRAKEN_KEY_PATH='/app/kraken.key' 
ENV TELEGRAM_KEY_PATH='/app/telegram.key' 
ENV SETTINGS_PATH='/app/settings/settings.json'

RUN sh scripts/requirements.sh 


FROM build AS cthulhu
RUN chmod +x scripts/run 

RUN echo '0 16 * * * /app/scripts/run' > /etc/crontabs/root 

CMD crond -l 3 -f 


FROM build as telegram-bot

CMD python3 src/services/telegram.py