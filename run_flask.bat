::SET mypath=%~dp0
::SET FLPATH=%mypath%app.py
::echo %FLPATH%
::SET FLASK_APP=%FLPATH%
SET TEMPLATES_AUTO_RELOAD = True
SET FLASK_ENV = development
SET FLASK_APP = app.py
python -m flask run
timeout /t 50