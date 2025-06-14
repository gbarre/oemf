#!/bin/sh

export GUNICORN_CMD_ARGS="--error-logfile - --workers=$WORKERS --timeout=$TIMEOUT"

if [ "${DB_MIGRATE}" = "upgrade" ] || [ "${DB_MIGRATE}" = "downgrade" ]; then
    FLASK_APP=run.py python -m flask db "${DB_MIGRATE}"
fi

export GUNICORN_CMD_ARGS="${GUNICORN_CMD_ARGS} --bind=0.0.0.0:5000 -k uvicorn.workers.UvicornWorker"

exec gunicorn run:connexion_app
