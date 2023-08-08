ARG BALLCHASING_TOKEN
FROM python:3.9.11


COPY . /ballchasing-client

WORKDIR ballchasing-client

RUN pip install -e .

ENTRYPOINT = ['extract-daily']