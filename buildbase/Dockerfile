FROM python:3.9-buster
WORKDIR /app

COPY . .

ENV FLASK_APP=api_portal
ENV FLASK_RUN_HOST=0.0.0
ENV PYTHONPATH=/app/dataservice
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080

ENV PYTHONFAULTHANDLER=1