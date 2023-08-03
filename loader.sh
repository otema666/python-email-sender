#!/bin/bash
echo "Checking installed packages..."

if pip list | grep -i "selenium" > /dev/null 2>&1; then
    echo "selenium OK"
else
    echo "Installing selenium..."
    pip install --disable-pip-version-check selenium > /dev/null 2>&1
fi

if pip list | grep -i "qrcode" > /dev/null 2>&1; then
    echo "qrcode OK"
else
    echo "Installing qrcode..."
    pip install --disable-pip-version-check qrcode > /dev/null 2>&1
fi

if pip list | grep -i "colorama" > /dev/null 2>&1; then
    echo "colorama OK"
else
    echo "Installing colorama..."
    pip install --disable-pip-version-check colorama > /dev/null 2>&1
fi

echo "All installations complete."
python main.py