@echo off
title main python script
echo Checking installed packages...

pip list | find /i "selenium" >nul 2>&1
if not errorlevel 1 (
    echo selenium OK
) else (
    echo Installing selenium...
    pip install --disable-pip-version-check selenium 2>nul
)

pip list | find /i "qrcode" >nul 2>&1
if not errorlevel 1 (
    echo qrcode OK
) else (
    echo Installing qrcode...
    pip install --disable-pip-version-check qrcode 2>nul
)

pip list | find /i "colorama" >nul 2>&1
if not errorlevel 1 (
    echo colorama OK
) else (
    echo Installing colorama...
    pip install --disable-pip-version-check colorama 2>nul
)

echo All installations complete.
python main.py