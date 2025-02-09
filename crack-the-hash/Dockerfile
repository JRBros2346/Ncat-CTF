FROM alpine:latest
RUN apk add --no-cache python3 socat
WORKDIR /crack-the-hash
COPY . .
CMD socat -T60 TCP-LISTEN:1337,reuseaddr,fork EXEC:"python3 hash.py"
