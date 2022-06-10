#!/bin/bash
set -e

export PGUSER=${POSTGRES_USER}
export PGPASSWORD=${POSTGRES_PASSWORD}

cd /opt/message-db && database/install.sh
