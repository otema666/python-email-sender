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

pip list | find /i "Flask-Cors" >nul 2>&1
if not errorlevel 1 (
    echo Flask-Cors OK
) else (
    echo Installing Flask-Cors...
    pip install --disable-pip-version-check Flask-Cors >nul 2>&1
)

pip list | find /i "Flask" >nul 2>&1
if not errorlevel 1 (
    echo Flask OK
) else (
    echo Installing Flask...
    pip install --disable-pip-version-check Flask >nul 2>&1
)

echo All installations complete.
cls

:Menu
echo Choose an option:
echo 1. Run main.py
echo 2. Run gui.py
echo 3. Run extension_server.py
echo 4. Exit

set /p choice=Enter option number: 

if "%choice%"=="1" (
    python main.py
) else if "%choice%"=="2" (
    python gui.py
) else if "%choice%"=="3" (
    python extension_server.py
) else if "%choice%"=="4" (
    exit /b 0
) else (
    echo Invalid option. Please try again.
    goto Menu
)