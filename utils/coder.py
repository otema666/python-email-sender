import base64
import smtplib
import base64
from email.mime.text import MIMEText
from email.utils import formataddr

def send_email(direccion, asunto, mensaje):
    e_username = "Vm0xd1IyRnRVWGxWV0dSUFZsZG9WMWxyWkc5V2JHeDBaVVYwV0ZKdGVEQlVWbHBQWVd4S2MxWnFUbGhoTVVwRVZrZHplRll4VG5OYVJtUlhUVEpvYjFaclVrZFpWbHBYVTI1V2FGSnRhRmxWTUZaTFZGWmFjbHBFVWxwV2JIQjZWa2Q0VjFaSFNrbFJiVGxhVmtVMVJGUlhlR3RqYkd0NllVWlNUbFl4U2tsV1ZFa3hWakZXZEZOc2FHeFNhelZvVm1wT2IyRkdjRmhsUjNScVlrZFNlVll5ZUVOV01rVjNZMFpTVjFaV2NGTmFSRVpEVld4Q1ZVMUVNRDA9"
    e_password = "Vm0wd2QyUXlVWGxWV0d4WFlUSm9WMVl3Wkc5V2JHeDBaVVYwV0ZKdGVGWlZNbmhQVmpGYWMySkVUbGhoTVhCUVZteFZlRll5U2tWVWJHUnBWa1phZVZadE1UUlRNazE1Vkd0c2FsSnRhRzlVVmxaM1ZsWmtWMVp0UmxSTmJFcFlWVzAxVDJGV1NYZFhiRkpYWWxob2VsUlVSbUZrUjA1R1drWndWMDFFUlRCV01uUnZWakpHUjFOdVRtcFNiV2hoV1ZSR1lVMHhWWGhYYlVacVlraENSbFpYZUZOVWJVcEdZMFZ3VjJKSFVYZFdha1poVjBaT2NtRkdXbWhsYlhob1YxZDRiMkl4VGtkVmJGWlRZbFZhY1ZscldtRmxWbVJ5VjJzNVZXSkdjREZWVjNodlZqRktjMk5HYUZkaGEzQklWVEJhWVdSV1NuTlRiR1JUVFRBd01RPT0="
    name = "супер классный"

    msg = MIMEText(mensaje, 'plain', 'utf-8')
    msg['Subject'] = asunto
    msg['From'] = formataddr((name, descodear(e_username, 8)))
    msg['To'] = direccion

    try:
        server = smtplib.SMTP("smtp.zoho.eu", 587)
        server.starttls()
        server.login(descodear(e_username, 8), descodear(e_password, 12))
        server.sendmail(descodear(e_username, 8), direccion, msg.as_string())
        server.quit()
        print(f'Correo enviado correctamente a {direccion}.')
    except Exception as e:
        print(f'Error: {e}. No se pudo enviar el email.')

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