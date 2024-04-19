FROM python:3.11.5-slim-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY app /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y gettext