FROM python:3.8-slim-buster

ENV PATH="/scripts:${PATH}"

COPY backend/requirements.txt /requirements.txt
RUN apt-get update \
&& apt-get -y install gcc libc-dev libpq-dev python3-dev \
&& apt-get clean
RUN pip install -r /requirements.txt

RUN mkdir /app
COPY ./backend /app
WORKDIR /app

RUN rm -rf /app/env
RUN rm -rf /app/serve

COPY ./scripts /scripts
RUN chmod +x /scripts/*

RUN mkdir -p /serve/media
RUN mkdir -p /serve/static

RUN adduser --disabled-password user
RUN chown -R user:user /app
RUN chown -R user:user /serve
RUN chmod -R 755 /serve

USER user

CMD ["entrypoint.sh"]
