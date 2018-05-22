::SET mypath=%~dp0
::SET FLPATH=%mypath%app.py
::echo %FLPATH%
::SET FLASK_APP=%FLPATH%
set FLASK_ENV=development
set FLASK_APP=app.py
python -m flask run
timeout /t 50