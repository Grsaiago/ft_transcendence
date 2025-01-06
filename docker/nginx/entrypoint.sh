#!/bin/bash

CERT_DIR="/etc/nginx/ssl"
CERT_FILE="$CERT_DIR/certificate.crt"
KEY_FILE="$CERT_DIR/private.key"
CERT_SIGN_REQUEST="$CERT_DIR/certificate_sign_request.csr"

mkdir -p "$CERT_DIR"

if [[ ! -f "$CERT_FILE" || ! -f "$KEY_FILE" ]]; then
    echo "Certificate or key file not found. Generating a new self-signed SSL certificate..."

    openssl genrsa -out $KEY_FILE 2048
    openssl req -new -key $KEY_FILE -out $CERT_SIGN_REQUEST -subj "/C=$COUNTRY/ST=$STATE/L=$LOCALITY/O=$ORGANIZATION/OU=$OUNITY/CN=$DOMAIN_NAME"
    openssl x509 -req -in $CERT_SIGN_REQUEST -signkey $KEY_FILE -out $CERT_FILE -days 365

    if [[ $? -ne 0 ]]; then
        echo "Failed to generate SSL certificate. Please check the OpenSSL configuration."
        exit 1
    fi
    echo "Certificates generated in $CERT_DIR!"
    echo "Certificate: $CERT_FILE"
    echo "Key: $KEY_FILE"
else
    echo "Certificate and key files already exist. No action taken."
fi

# Start the Nginx server
echo "Starting Nginx server..."
exec nginx -g "daemon off;"
