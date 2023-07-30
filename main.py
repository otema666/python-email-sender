import os
import time
from selenium import webdriver
from colorama import Fore, init

# Inicio colorama con autoreset
init(autoreset=True)
# Defino los principales colores
G = Fore.GREEN
R = Fore.RED
B = Fore.BLUE

def main():
	if "geckodriver.log" in os.listdir():
		rm_FirefoxLog()
	print("Qué navegador desea usar?")
	print()
	print(f"{G}1. Google Chrome")
	print(f"{G}2. Brave Browser")
	print(f"{G}3. Firefox\n")
	nav = int(input(f"Respuesta: {B}"))
	# execute_browser(nav, get_pwd())
	execute_browser_a_la_nazi(nav, "http://localhost:8000/")
	abrir_data()
	correo, asunto, mensaje = process_data()


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

def abrir_data():
	file_path = "data"
	while not os.path.exists(file_path):
		print(f"{B}El path esta en escucha a la espera de los datos...\n")
		time.sleep(0.5)
		clear()
	clear()
	
def process_data():
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
	print(f"{R}'data' ha sido eliminado.")
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



if __name__ == "__main__":
	clear()
	if os.name == "nt":
		os.system("start start_server.bat")
	else:
		os.system("start start_server.sh")
	main()