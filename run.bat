cls
@ECHO OFF
@pushd %~dp0
echo Working Please wait...
Call "%cd%\.env\scripts\activate.bat"
Call python run.py
@popd
pause
