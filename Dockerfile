FROM alpine:3.10

ENV TZ=Europe/Madrid
MAINTAINER Lorenzo Carbonell <a.k.a. atareao> "lorenzo.carbonell.cerezo@gmail.com"

ENV PYTHONUNBUFFERED=1

RUN echo "**** install Python ****" && \
    apk add --update --no-cache python3 tini tzdata sudo && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    \
    echo "**** install pip ****" && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    echo "**** install dependencies **** " && \
    pip3 install --no-cache-dir \
    flask \
    itsdangerous \
    requests \
    pyinotify  \
    werkzeug \
    markdown && \
    rm -rf /var/lib/apt/lists/* && \
    echo "**** create user ****" && \
    addgroup userpod && \
    adduser -h /app -G userpod -D userpod && \
    mkdir -p /app/database && \
    chown -R userpod:userpod /app && \
    echo "userpod ALL=(root) NOPASSWD: /bin/chown" > /etc/sudoers.d/userpod

VOLUME /app/templates
VOLUME /app/database
WORKDIR /app
USER userpod

COPY start.sh /start.sh
COPY ./app /app

ENTRYPOINT ["tini", "--"]
CMD ["/bin/sh", "/start.sh"]
