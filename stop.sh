#!/bin/bash -e

instance=$(docker ps -a --no-trunc --filter name=docker-florescielo-api.service --filter status=running --format "{{.ID}}")
docker stop ${instance}
