#!/usr/bin/env sh
set -e
export PGUSER=${POSTGRES_USER}
export PGPASSWORD=${POSTGRES_PASSWORD}
cd /message-db && database/install.sh
