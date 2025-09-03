@echo off
set FLASK_APP=app.py
set FLASK_ENV=development
set FLASK_DEBUG=1

echo Starting Flask development server...
python -m flask run --host=0.0.0.0 --port=5000
