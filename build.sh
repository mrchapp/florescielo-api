#!/bin/bash -e

export LANG=C

if [[ ! -f Dockerfile || Dockerfile -ot Dockerfile.in || Dockerfile -ot $0 ]]; then
    arch=$(uname -m | cut -c1-3)
    [[ ${arch} == "arm" ]] && from="resin/rpi-raspbian:jessie-20160831"
    [[ ${arch} == "x86" ]] && from="debian:bullseye"

    cat <(echo "FROM ${from}") Dockerfile.in > Dockerfile
fi

docker build --tag=florescielo-api .
