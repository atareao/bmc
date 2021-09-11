#!/bin/bash

podman ps -a | grep bmc
if [ $? -eq 0 ]
then
    podman stop bmc
    podman rm bmc
fi
source ENV.sh
podman build --tag atareao/bmc .
podman run -d --name bmc \
           -v ${PWD}/database:/app/database \
           -v ${PWD}/templates:/app/templates \
           -p 5000:5000 atareao/bmc \
           -e WEBHOOK=${WEBHOOK} \
           -e SERVER=${SERVER} \
           -e PORT=${PORT} \
           -e MAIL=${MAIL} \
           -e PASSWORD=${PASSWORD} \
           -e TO=${TO} \
           -e BMC_ACCESS_TOKEN=${BMC_ACCESS_TOKEN}
podman logs -f bmc
