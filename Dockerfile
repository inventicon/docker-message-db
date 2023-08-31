# syntax=docker/dockerfile:1
ARG BASE_IMAGE=postgres:15-alpine
FROM ${BASE_IMAGE}

ARG MESSAGE_DB_TAG=v1.3.0
ADD --chown=postgres:postgres https://github.com/message-db/message-db.git#${MESSAGE_DB_TAG} /message-db

COPY install-message-db.sh /docker-entrypoint-initdb.d/install-message-db.sh
