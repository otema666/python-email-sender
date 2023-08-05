@echo off
title main python script
echo Checking installed packages...

pip list | find /i "qrcode" >nul 2>&1
if not errorlevel 1 (
    echo qrcode OK
) else (
    echo Installing qrcode...
    pip install --disable-pip-version-check qrcode >nul 2>&1
)

pip list | find /i "names" >nul 2>&1
if not errorlevel 1 (
    echo names OK
) else (
    echo Installing names...
    pip install --disable-pip-version-check names >nul 2>&1
)

pip list | find /i "colorama" >nul 2>&1
if not errorlevel 1 (
    echo colorama OK
) else (
    echo Installing colorama...
    pip install --disable-pip-version-check colorama >nul 2>&1
)

pip list | find /i "pyqt6" >nul 2>&1
if not errorlevel 1 (
    echo pyqt6 OK
) else (
    echo Installing pyqt6...
    pip install --disable-pip-version-check pyqt6 >nul 2>&1
)

echo All installations complete.
python main.py