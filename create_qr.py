import subprocess
import qrcode
import os
# Verificar si estamos conectados a una red WiFi o por cable
result = subprocess.run("netsh interface show interface", capture_output=True, text=True)
if "Wi-Fi" not in result.stdout:
    print("No estás conectado a una red.")
    exit(1)

# print("Conectado a una red.")

# Obtener el nombre de la red WiFi
result = subprocess.run("netsh wlan show interfaces", capture_output=True, text=True)
wifi_name = None
for line in result.stdout.splitlines():
    if "SSID" in line:
        wifi_name = line.split(":")[1].strip()
        break

if not wifi_name:
    print("No se pudo obtener el nombre de la red WiFi.")
    exit(1)

# Obtener la contraseña utilizando "netsh wlan show profile" y filtrar la salida
result = subprocess.run(f"netsh wlan show profile name=\"{wifi_name}\" key=clear", capture_output=True, text=True)
wifi_password = None
for line in result.stdout.splitlines():
    if "Contenido de la clave" in line:
        wifi_password = line.split(":")[1].strip()
        break

if not wifi_password:
    print("No se pudo obtener la contraseña de la red WiFi.")
    exit(1)

# print(f"Nombre de la red WiFi: {wifi_name}")
# print(f"Contraseña de la red WiFi: {wifi_password}")

# Generar el código QR con la información de configuración del WiFi
data = f"WIFI:T:WPA;S:{wifi_name};P:{wifi_password};;"
qr_code = qrcode.make(data)

# Guardar el código QR en un archivo
qr_code_filename = "qr.png"
qr_code.save(qr_code_filename)
# print(f"Código QR generado y guardado en {qr_code_filename}.")
os.system(qr_code_filename)