FROM python:3.10.8-alpine3.16
WORKDIR /usr/src/app
RUN apk add socat py3-pycryptodome && mv /usr/lib/python3.10/site-packages/Crypto/ /usr/local/lib/python3.10/site-packages/Crypto
COPY . .
CMD ["sh", "./runit"]