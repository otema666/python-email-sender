#!/bin/bash
echo "Checking installed packages..."

if pip list | grep -i "requests" > /dev/null 2>&1; then
    echo "requests OK"
else
    echo "Installing requests..."
    pip install --disable-pip-version-check requests > /dev/null 2>&1
fi

if pip list | grep -i "names" > /dev/null 2>&1; then
    echo "names OK"
else
    echo "Installing names..."
    pip install --disable-pip-version-check names > /dev/null 2>&1
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

if pip list | grep -i "pyqt6" > /dev/null 2>&1; then
    echo "pyqt6 OK"
else
    echo "Installing pyqt6..."
    pip install --disable-pip-version-check pyqt6 > /dev/null 2>&1
fi

if pip list | grep -i "Flask-Cors" > /dev/null 2>&1; then
    echo "Flask-Cors OK"
else
    echo "Installing Flask-Cors..."
    pip install --disable-pip-version-check Flask-Cors > /dev/null 2>&1
fi

if pip list | grep -i "Flask" > /dev/null 2>&1; then
    echo "Flask OK"
else
    echo "Installing Flask..."
    pip install --disable-pip-version-check Flask > /dev/null 2>&1
fi

echo "All installations complete."

while true; do
    clear
    echo "Choose an option:"
    echo "1. Run main.py"
    echo "2. Run gui.py"
    echo "3. Run extension_server.py"
    echo "4. Exit"
    
    read -p "Enter option number: " choice
    
    case $choice in
        1)
            python3 main.py
            ;;
        2)
            python3 gui.py
            ;;
        3)
            python3 extension_server.py
            ;;
        4)
            exit 0
            ;;
        *)
            echo "Invalid option. Please try again."
            ;;
    esac
done

python3 main.py