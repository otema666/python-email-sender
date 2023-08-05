import os
import json
import subprocess	
import base64
import asyncio
from colorama import Fore, init

#email
from utils.coder import clear
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr


# Inicio colorama con autoreset
init(autoreset=True)
# Defino los principales colores
G = Fore.GREEN
R = Fore.RED
B = Fore.BLUE

async def run():
	if "geckodriver.log" in os.listdir():
		rm_FirefoxLog()
	if "qr.png" in os.listdir():
		rm_qr_img()

	# execute_browser(nav, get_pwd())
	qr = str(input(f"{Fore.MAGENTA}Deseas generar un código qr de la red actual? (y/n): {B}")).lower()
	if qr == "y" or qr == "s":
		if os.name == "nt":
			os.system("python utils/create_qr.py")

		else:
			os.system("python3 utils/create_qr.py")
	else:
		pass
	clear()
	nav = openNav()
	if qr == "y" or qr == "s":
		rm_qr_img()
	execute_browser_a_la_nazi(nav, "http://localhost:8000/")
		 
async def start_server():
    if os.name == "nt":
        # En Windows, usa subprocess para ocultar la ventana de la consola.
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.Popen(["python", "server.py"], startupinfo=startupinfo)
    else:
        subprocess.Popen(["python3", "server.py"])


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

async def main():
    # Creating tasks for both functions
    task1 = asyncio.create_task(start_server())
    task2 = asyncio.create_task(run())

    # Wait for both tasks to complete
    await asyncio.gather(task2, task1)

# Run the main function asynchronously
clear()
asyncio.run(main())