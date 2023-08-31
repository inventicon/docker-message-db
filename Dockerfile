# syntax=docker/dockerfile:1
ARG BASE_IMAGE=postgres:15-alpine
FROM ${BASE_IMAGE}

COPY docker-entrypoint.sh /usr/local/bin/

ARG MESSAGE_DB_TAG=v1.3.0
ADD --chown=postgres:postgres https://github.com/message-db/message-db.git#${MESSAGE_DB_TAG} /message-db

ENTRYPOINT [ "docker-entrypoint.sh" ]
CMD [ "postgres" ]
