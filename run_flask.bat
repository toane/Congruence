::SET mypath=%~dp0
::SET FLPATH=%mypath%app.py
::echo %FLPATH%
::SET FLASK_APP=%FLPATH%
set FLASK_ENV=development
set FLASK_APP=app.py
python -m flask run --host 192.168.1.53
timeout /t 50