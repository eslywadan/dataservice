#FROM python:3.9-alpine
#FROM dataservice:latest
FROM dataservice:basev001
#RUN useradd --create-home app
#USER app
WORKDIR /app
ENV PYTHONFAULTHANDLER=1
EXPOSE 8060
ENTRYPOINT [ "./run_celery_flower.sh" ]
# ENTRYPOINT ["python3"]
# During debugging, this entry point will be overridden. For more information, refer to https://aka.ms/vscode-docker-python-debug
# CMD ["celery", "-A", "taskman.celerytask", "worker", "--loglevel=INFO", "--logfile=ext\logs\%p.log"]
# CMD ["gunicorn", "--bind", "0.0.0.0:8080", "api_portal:app", \
#    "--log-file", "/app/ext/gunicorn.log", \
#    "--timeout", "900", "-preload"]