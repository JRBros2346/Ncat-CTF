FROM alpine:latest
RUN apk add --no-cache python3 socat
WORKDIR /crack-the-hash
COPY . .
CMD socat -T60 TCP-LISTEN:1137,reuseaddr,fork EXEC:"python3 hash.py"
