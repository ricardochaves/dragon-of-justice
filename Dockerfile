FROM python:3.6.2rc2

ADD . /bot

WORKDIR /bot

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install -r requirements_dev.txt