FROM alpine:latest

RUN apk add python3 socat

WORKDIR /bank-heist

COPY . .

CMD socat -T60 TCP-LISTEN:1237,reuseaddr,fork EXEC:"python3 heist.py"
