@echo off
echo Starting Rasa Actions Server...

set PORT=5056
set SQLALCHEMY_SILENCE_UBER_WARNING=1
set SQLALCHEMY_WARN_20=0
set PYTHONPATH=%PYTHONPATH%;%CD%

.\venv\Scripts\activate
rasa run actions --port %PORT%

pause 