#!/bin/bash
echo "http://localhost:5000/run"
export FLASK_ENV=development
FLASK_APP=app.py flask run --host 192.168.1.53
#python -m flask run --host 192.168.1.53
