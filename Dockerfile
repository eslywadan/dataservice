#FROM python:3.9-alpine
#FROM dataservice:latest
FROM python:3.9-buster
#RUN useradd --create-home app
#USER app
WORKDIR /app
#WORKDIR /home/app

COPY . .

ENV FLASK_APP=api_portal
ENV FLASK_RUN_HOST=0.0.0
#ENV PYTHONPATH=/home/app
ENV PYTHONPATH=/app
#RUN apk add --no-cache gcc musl-dev linux-headers
#RUN apk add build-base
# RUN apt install hdf5-dev
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080

ENV PYTHONFAULTHANDLER=1
ENTRYPOINT [ "./run_celery_worker.sh" ]
# ENTRYPOINT ["python3"]
# During debugging, this entry point will be overridden. For more information, refer to https://aka.ms/vscode-docker-python-debug
# CMD ["celery", "-A", "taskman.celerytask", "worker", "--loglevel=INFO", "--logfile=ext\logs\%p.log"]
# CMD ["gunicorn", "--bind", "0.0.0.0:8080", "api_portal:app", \
#    "--log-file", "/app/ext/gunicorn.log", \
#    "--timeout", "900", "-preload"]