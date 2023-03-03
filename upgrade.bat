cls
@ECHO OFF
setlocal
@pushd %~dp0

Call "%cd%\.env\scripts\activate.bat"

@ECHO ON

"%cd%\.env\Scripts\python.exe" -m pip install --upgrade pip

"%cd%\.env\Scripts\python.exe" "%cd%\upgrade.py"

@popd
endlocal
pause
exit
