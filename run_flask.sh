#!/bin/bash
echo "http://localhost:5000/run"
export FLASK_ENV=development
FLASK_APP=app.py flask run --host 127.0.0.1
#python -m flask run --host 192.168.1.53
