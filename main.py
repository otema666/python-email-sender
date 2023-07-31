import os
import time
import smtplib
import base64
from selenium import webdriver
from colorama import Fore, init

#email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr


# Inicio colorama con autoreset
init(autoreset=True)
# Defino los principales colores
G = Fore.GREEN
R = Fore.RED
B = Fore.BLUE

def main():
	if "geckodriver.log" in os.listdir():
		rm_FirefoxLog()
	if "qr.png" in os.listdir():
		rm_qr_img()

	# execute_browser(nav, get_pwd())
	qr = str(input("Deseas generar un código qr de la red actual? (y/n): ")).lower()
	if qr == "y" or qr == "s":
		if os.name == "nt":
			os.system("python create_qr.py")

		else:
			os.system("python3 create_qr.py")
	else:
		pass
	
	nav = openNav()
	rm_qr_img()
	execute_browser_a_la_nazi(nav, "http://localhost:8000/")
	while True:
		abrir_data()
		correo, asunto, mensaje = process_data()
		send_email(correo, asunto, mensaje)
		

def clear():
	os.system("cls") if os.name == "nt" else os.system("clear")

def get_pwd():
	if os.name == "nt":
		path = str(os.getcwd())
		path += "\index.html"
	else:
		pass
	return path

def rm_FirefoxLog():
	if os.name == "nt":
		os.system("del geckodriver.log")
	else:
		os.system("rm geckodriver.log")	

def rm_qr_img():
	if os.name == "nt":
		os.system("del qr.png")
	else:
		os.system("rm qr.png")

def openNav():
	print("Qué navegador desea usar?")
	print()
	print(f"{G}1. Google Chrome")
	print(f"{G}2. Brave Browser")
	print(f"{G}3. Firefox\n")
	print(f"{G}4. Omitir\n")
	nav = int(input(f"Respuesta: {B}"))
	return nav

def abrir_data():
	file_path = "data"
	print(f"{B}El path esta en escucha a la espera de los datos...\n")
	while not os.path.exists(file_path):
		time.sleep(0.5)
	
def process_data():
	file_path = "data"
	with open(file_path, 'r') as data:
		v = False
		for linea in data:
			if "C$o$r$r$e$o:" in linea:
				correo_array = linea.split(":")
				correo = correo_array[1]
				correo = correo.strip()
			if "A$s$u$n$t$o:" in linea:
				asunto_array = linea.split(":")
				asunto = asunto_array[1]
				asunto = asunto.strip()	
			if v:	
				mensaje += linea
			if "M$e$n$s$a$j$e:" in linea:
				mensaje_array = linea.split(":")
				mensaje = mensaje_array[1]
				v = True
			
		# print(f"El correo es {correo}, el asunto es {asunto} y el mensaje es:\n{mensaje}")
	os.remove(file_path)
	# print(f"{R}'data' ha sido eliminado.")
	return correo, asunto, mensaje

def execute_browser_a_la_nazi(nav, url):
	if nav == 1:
		if os.name == "nt":
			os.system(f"start chrome --incognito {url}")
		else:
			os.system(f"chrome --incognito {url}")
	elif nav == 2:
		if os.name == "nt":
			os.system(f"start brave-browser --incognito {url}")
		else:
			os.system(f"brave --incognito {url}")
	elif nav == 3:
		if os.name == "nt":
			os.system(f"start firefox --private {url}")
		else:
			os.system(f"firefox --private {url}")
	else: 
		pass
	

def execute_browser(nav, url):
    if nav == 1:
        # Configuramos el navegador GOOGLE CHROME
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--incognito")
        driver = webdriver.Chrome(options=options)
    
    elif nav == 2:
        # Configuramos el navegador Brave Browser
        options = webdriver.ChromeOptions()
        options.binary_location = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'
        options.add_argument("--start-maximized")
        options.add_argument("--incognito")
        driver = webdriver.Chrome(options=options)
    
    elif nav == 3:
        # Configuramos el navegador Firefox
        options = webdriver.FirefoxOptions()
        options.add_argument('--private-window')
        driver = webdriver.Firefox(options=options)
    
    driver.get(url)
    #driver.execute_script("alert()")
    input("esto es un breakpoint")

    #tokenGetter = open("getToken.js").read()
    # driver.execute_script(tokenGetter)


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
		print(f'{G}Correo enviado correctamente a {direccion}.')
	except Exception as e:
		print(f'Error: {e}. No se pudo enviar el email.')

def descodear(texto, veces):
	for a in range(veces):
		decoded = base64.b64decode(texto).decode('utf-8')
		texto = decoded
	return decoded

if __name__ == "__main__":
	clear()
	if os.name == "nt":
		os.system("start start_server.bat")
	else:
		os.system("start start_server.sh")
	main()