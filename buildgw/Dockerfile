#FROM python:3.9-alpine
#FROM dataservice:latest
#FROM python:3.9-buster
FROM dataservice:basev001
#RUN useradd --create-home app
#USER app
WORKDIR /app
#WORKDIR /home/app

EXPOSE 8020

ENV PYTHONFAULTHANDLER=1
# During debugging, this entry point will be overridden. For more information, refer to https://aka.ms/vscode-docker-python-debug
 CMD ["gunicorn", "--bind", "0.0.0.0:8080", "api_portal:app", \
    "--log-file", "/app/ext/gunicorn.log", \
    "--timeout", "900", "-preload"]