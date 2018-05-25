#!/bin/bash
echo "http://localhost:5000/run"
export FLASK_ENV=development
FLASK_APP=app.py flask run  --host 0.0.0.0
