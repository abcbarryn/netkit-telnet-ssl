#!/bin/bash

if [ -e "$1" ]
then
	echo "File \"$1\" already exists. Exiting."
	exit 0
fi
touch "$1"
if [ ! -e "$1" ]
then
	echo "Invalid file path \"$1\"!"
	exit 1
fi
# Define certificate parameters
CERT_NAME=`hostname -f`
CERT_DAYS=3650 # Validity period in days
KEY_BITS=4096 # RSA key strength
TMPCERT="/tmp/cert$$"

# Generate the private key and self-signed certificate
openssl req -x509 -newkey rsa:${KEY_BITS} -nodes \
	-keyout "${TMPCERT}.key" -out "${TMPCERT}.crt" \
	-days ${CERT_DAYS} \
	-subj "/CN=${CERT_NAME}"

cat  "${TMPCERT}.key"  "${TMPCERT}.crt" >"$1"

rm -f "${TMPCERT}.key" "${TMPCERT}.crt"
