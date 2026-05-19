#!/bin/bash

openssl genrsa -out rsaPrivateKey.pem 2048
openssl pkcs8 -topk8 -inform PEM -outform PEM -in rsaPrivateKey.pem -out privateKey.pem -nocrypt
openssl rsa -in rsaPrivateKey.pem -pubout -outform PEM -out publicKey.pem

mkdir -p src/main/resources/certs
mv publicKey.pem src/main/resources/certs/
mv privateKey.pem src/main/resources/certs/
rm rsaPrivateKey.pem

echo "---------------------------------------------"
echo "Success"
echo "Public key: src/main/resources/publicKey.pem"
echo "Private key: ./privateKey.pem"
echo "---------------------------------------------"