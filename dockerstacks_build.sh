#!/bin/bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

CONTAINER=${DIR##*/}
DOCKERFILE="mariadb_kernel/tests/docker/dockerstacks_Dockerfile"
docker rmi -f ${CONTAINER}
docker pull $(awk '/FROM/{ print $2 }' $DOCKERFILE)
docker build --rm $1 -t ${CONTAINER} -f $DOCKERFILE . && echo "Finished building ${CONTAINER}"
if [ "$1" != "--no-cache" ]
then
   echo "For final build use: $0 --no-cache!"
fi
