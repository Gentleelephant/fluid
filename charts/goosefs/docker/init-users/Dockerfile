FROM alpine:3.24

RUN apk add --no-cache bash shadow net-tools

COPY *.sh /

RUN chmod +x /*.sh

ENTRYPOINT ["/entrypoint.sh"]
