#!/bin/sh
FOLDER=$(dirname "${0}")/src/static
ssh-keygen -t rsa -b 4096 -m PEM -N '' -C 'alcoholic' -q -f "${FOLDER}"/id_rsa << y
openssl rsa -in "${FOLDER}"/id_rsa -pubout -outform PEM -out "${FOLDER}"/id_rsa.pub



