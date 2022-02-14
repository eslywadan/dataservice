# syntax=docker /dockerfile:1
FROM python:3.9-alpine
WORKDIR /app
ENV FLASK_APP=api_portal
ENV FLASK_RUN_HOST=0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
RUN apk add build-base
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8080
COPY . .
# CMD ["flask", "run"]