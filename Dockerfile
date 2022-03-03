FROM python:3.9-alpine
#FROM dataservice:latest
WORKDIR /app
ENV FLASK_APP=api_portal
ENV FLASK_RUN_HOST=0.0.0
ENV PYTHONPATH=/app
RUN apk add --no-cache gcc musl-dev linux-headers
RUN apk add build-base
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8080
WORKDIR /app
COPY . .

# During debugging, this entry point will be overridden. For more information, refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "api_portal:app", \
    "--log-file", "/app/logs/gunicorn.log", \
    "--timeout", "900"]