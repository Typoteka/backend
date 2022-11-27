FROM python:3.11.0-alpine3.16
LABEL maintainer="typoteka"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
ARG USER_ID=1000
ARG GROUP_ID=1000
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
    then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    # adduser \
    #     --disabled-password \
    #     # --no-create-home \
    #     django-user
    groupadd -g 1000 -o && useradd -u 1000 -d /home/django-user -m -k /etc/skel -g 1000 django-user

ENV PATH="/py/bin:$PATH"

USER django-user