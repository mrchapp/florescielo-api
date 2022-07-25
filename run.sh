#!/bin/bash -e

BASEDIR="$(dirname "$(readlink -f "$0")")"
#DATADIR="$(readlink -e "${BASEDIR}/../data/web/")"
#PRIVDIR="$(readlink -e "${BASEDIR}/../priv/web/")"
DATADIR="${BASEDIR}/localdatapriv"
PRIVDIR="${BASEDIR}/localdatapriv"

docker run -it \
    --rm \
    --name docker-florescielo-api.service \
    -v /etc/localtime:/etc/localtime:ro \
    -v ${PRIVDIR}/config.json:/app/config.json \
    -v ${DATADIR}/florescielo_api.db:/app/florescielo_api.db \
    -v ${BASEDIR}/images/:/app/images/ \
    -p 0.0.0.0:80:8090 \
    -e PORT=8090 \
    florescielo-api

# For debugging and testing:
#    -v ${BASEDIR}/florescielo-api/:/app/florescielo-api/
