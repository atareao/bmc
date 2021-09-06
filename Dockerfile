FROM alpine:3.10

ENV TZ=Europe/Madrid
MAINTAINER Lorenzo Carbonell <a.k.a. atareao> "lorenzo.carbonell.cerezo@gmail.com"

ENV PYTHONUNBUFFERED=1
ENV BMC_ACCESS_TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5MTI5ZDIwMC1kYTdkLTRjY2MtOWQzZC01ODA0MTU0ZTgyMjYiLCJqdGkiOiIxOGZjYjU0MzQ0MjQxODljMDgwNmMzMTNkMjk0MDcxZWEwM2RhYWFmYjQ1MmFkNTVmYjM3YmQ5OGJlY2NkZDIwNjAwMmIxYzc3NzUzNzQ1YiIsImlhdCI6MTYzMDg0MTE4OSwibmJmIjoxNjMwODQxMTg5LCJleHAiOjE2NDY0Nzk1ODksInN1YiI6Ijg1MzQ3NSIsInNjb3BlcyI6W119.FdFiHtBXtYYs2kRiklh6x35w9-AoXPc-vRi_Gbbm7qyPA_m-XKZFnIqNrw6lSCeyfo8iesbIfS841bJ5QB88dnaFJ0p78IDVY6-B508p_XPP0wp8BTMaf1sGpUfEHlTAXh1drxClNVDTZiOTTcXltNg7pF1GBwf9Y0zSvc788GQ7lKMel1zOKgXCJvEN-oK2jKG085a6nqVG0cUusFAqvGBOM7RTu0cPn5LI19cqKhyh-lj_VeIe1P2pQCv5EID7NOGCoAJOU5ksURBtlUNFUp12AMvDNgClTDrZLUSJq3_Q-Q7CQzLxuyxqwFl47aZ2J78dlTWiKgRNPdAe-UebYEoAoeUktCvTvjkSBqt-i1kp4dwKfNYabYuiPGh_bbeZPICvIyDHd307Lu1NhYaYmG8S897WItgGSeVHRCMWZxogANGC66CErm3nkPgQxIqVlxbrpSZVYNTRUJ-HAnB0NIYqHSdffIf-BBiLd2dlyQqAhfaPGVIBaFVFYvTDOE6-BWtFs6CQWAZcVqj9PB0sIuN9tkgWEEuYV070gDPjLUgcA-i-VkTouDb0SbWZx601npO8GR3tiVJV9AR7qae7thZ0zuvswe3R4Vc2XfuMpaYlhsD91NZ--IKQy5Vvzsa0kpyZTDixhmLPxwXJv4_4zkBPwTebZSPDInAYoX7uEyU"

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
    werkzeug && \
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
