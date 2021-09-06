#!/bin/bash

podman ps -a | grep bmc
if [ $? -eq 0 ]
then
    podman stop bmc
    podman rm bmc
fi
podman build --tag atareao/bmc .
podman run -d --name bmc \
              -v ${PWD}/database:/app/database \
              -v ${PWD}/templates:/app/templates \
              -p 5000:5000 atareao/bmc
podman logs -f bmc
