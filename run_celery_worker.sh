#!/bin/bash
python3 -m celery -A taskman.celerytask worker --loglevel=INFO --logfile=ext/logs/%p.log --concurrency=2