#!/bin/bash
python3 -m celery -A taskman.celerytask flower --loglevel=INFO --logfile=ext/logs/%p.log --address=0.0.0.0 --port=8020