FROM python:3.8-slim-buster

ENV PATH="/scripts:${PATH}"

COPY backend/requirements.txt /requirements.txt
RUN apt-get update \
&& apt-get -y install gcc libc-dev \
&& apt-get clean
RUN pip install -r /requirements.txt

RUN mkdir /app
COPY ./backend /app
WORKDIR /app

COPY ./scripts /scripts
RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/

RUN adduser --disabled-password user
RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web

USER user

CMD ["entrypoint.sh"]
