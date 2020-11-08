FROM ubuntu:latest

RUN /bin/bash -c "\
    apt update && \
    apt install -y python3 python3-pip && \
    apt clean \
"

ADD bootstrap.sh /tmp/scripts/
RUN ["chmod", "a+x", "/tmp/scripts/bootstrap.sh"]
ADD .sqliterc /root

ENTRYPOINT ["/tmp/scripts/bootstrap.sh"]
