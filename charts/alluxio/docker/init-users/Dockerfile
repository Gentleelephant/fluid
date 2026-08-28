FROM alpine:3.21

COPY *.sh /

RUN apk add --no-cache bash shadow net-tools

RUN chmod +x /*.sh

ENTRYPOINT ["/entrypoint.sh"]
