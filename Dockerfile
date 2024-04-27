FROM python:3.12.3-alpine3.19
LABEL maintainer='hameddjf33@gmail.com'
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /tmp/requirements.txt
COPY ./ZzzInn /ZzzInn
WORKDIR /ZzzInn
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        hameddjf && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R hameddjf:hameddjf /vol && \
    chmod -R 755 /vol && \
USER hameddjf

CMD ["run.sh"]