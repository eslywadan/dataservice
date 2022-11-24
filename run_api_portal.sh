#!/bin/bash
gunicorn --bind 0.0.0.0:8080 api_portal:app --log-file /app/dataservice/ext/gunicorn.log --timeout 900 -preload