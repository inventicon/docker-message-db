# == SETUP == #
FROM debian:bullseye-slim as setup

WORKDIR /

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y curl
RUN curl -L https://github.com/message-db/message-db/archive/refs/tags/v1.2.6.tar.gz --output message-db.tar.gz \
    && mkdir message-db \
    && tar -xvf message-db.tar.gz -C message-db --strip-components=1

# == FINAL == #
FROM {{ base_image }}

COPY --from=setup /message-db /opt/message-db
COPY ./install-message-db.sh /docker-entrypoint-initdb.d/
