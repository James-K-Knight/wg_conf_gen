cls
@ECHO OFF
setlocal
@pushd %~dp0
echo Working Please wait...
if not exist "%cd%\.env" virtualenv "%cd%\.env"
pause
Call "%cd%\.env\scripts\activate.bat"
"%cd%\.env\Scripts\python.exe" -m pip install --upgrade pip
"%cd%\.env\scripts\python.exe" -m pip install -r requirements.txt
@popd
endlocal
pause
exit
