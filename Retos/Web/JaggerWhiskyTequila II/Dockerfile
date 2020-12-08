FROM python:3.7-alpine
COPY src/ /src
COPY generate.sh /
COPY requirements.txt /
WORKDIR /src
RUN apk update && \
    apk add --no-cache openssl openssl-dev openssh-keygen libffi-dev build-base gcc && \
    rm -rf /var/cache/apk/* && \
    pip install -r /requirements.txt && \
    sh /generate.sh
EXPOSE 8000
ENTRYPOINT ["gunicorn", "-w 4", "-b 0.0.0.0:8000", "server:app"]