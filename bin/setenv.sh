#!/bin/sh

export MONGODB_URI=mongodb://localhost/congress
export MONGODB_DB=congress
export CONGRESS_SECRET='verysecret'
export CELSO_SAMPLES=/tmp/samples
export CELSO_UNKNOWN=/tmp/unknown
export EMAIL_SERVER_USER=apikey
export EMAIL_SERVER_PASSWORD=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
export EMAIL_SERVER_PORT=587
export EMAIL_SERVER_HOST=smtp.sendgrid.net
export EMAIL_FROM='congreso@congreso.com'
export NEXTAUTH_URL=http://192.168.1.181:3000
export FLASK_APP=faces/__main__.py