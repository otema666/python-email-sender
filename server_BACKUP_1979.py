import json
import os
import tkinter as tk
from tkinter import filedialog
from http.server import BaseHTTPRequestHandler, HTTPServer
from utils.coder import send_email, send_data, clear, descodear
from colorama import Fore, init
from urllib.request import Request, urlopen

init(autoreset=True)
with open('assets/index.html', 'r', encoding='utf-8') as f:
    INDEX_PAGE = f.read()

with open('assets/styles.css', 'r', encoding='utf-8') as f:
    STYLES = f.read()

with open('assets/background.jpg', 'rb') as f:
    BACKGROUND_IMAGE = f.read()

with open('assets/script.js', 'r', encoding='utf-8') as f:
    SCRIPT = f.read()


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    saved_emails = []

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(INDEX_PAGE.encode('utf-8'))
        elif self.path == '/styles.css':
            self.send_response(200)
            self.send_header('Content-type', 'text/css; charset=utf-8')
            self.end_headers()
            with open('assets/styles.css', 'r', encoding='utf-8') as f:
                self.wfile.write(f.read().encode('utf-8'))
        elif self.path == '/background.jpg':
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            with open('assets/background.jpg', 'rb') as f:
                self.wfile.write(f.read())
        elif self.path == '/script.js':
            self.send_response(200)
            self.send_header('Content-type', 'text/javascript; charset=utf-8')
            self.end_headers()
            with open('assets/script.js', 'r', encoding='utf-8') as f:
                self.wfile.write(f.read().encode('utf-8'))
        elif self.path == '/execute_function':
            # Llama a la función que deseas ejecutar
            self.__class__.files_seleccionados = self.select_files()
            archivos_para_el_JSON = [os.path.basename(file_path) for file_path in self.__class__.files_seleccionados]
            response_data = json.dumps({"files_seleccionados": archivos_para_el_JSON})

            # Configura la respuesta HTTP
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # Envía los resultados al cliente JavaScript
            self.wfile.write(response_data.encode())
        else:
            self.send_error(404, 'File not found')
        
        clear()
        print(f"{Fore.MAGENTA}Server en escucha...")

    def do_POST(self):
        if self.path == '/save_email':
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length).decode('utf-8')
            data_dict = json.loads(data)

            recipient = data_dict['recipient']
            subject = data_dict['subject']
            message = data_dict['message']

            # Store the email data in memory
            email_data = {
                'recipient': recipient,
                'subject': subject,
                'message': message
            }
            self.saved_emails.append(email_data)
<<<<<<< HEAD

            send_data(recipient, subject, message, self.__class__.files_seleccionados)
            send_email(recipient, subject, message, self.__class__.files_seleccionados)
=======
            
            if self.__class__.files_seleccionados != None:
                send_data(recipient, subject, message, self.__class__.files_seleccionados)
                send_email(recipient, subject, message, self.__class__.files_seleccionados)
            else:
                send_data(recipient, subject, message)
                send_email(recipient, subject, message)
>>>>>>> b4f995423e674af8dd4a09492a908a0813fd6aab
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'status': 'success'}
            self.wfile.write(json.dumps(response).encode('utf-8'))

        else:
            self.send_error(404, 'File not found')
        clear()
        print(f"{Fore.MAGENTA}Server en escucha...")

    def select_files(self):
        files_seleccionados = []
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        file_paths = filedialog.askopenfilenames()

        for file_path in file_paths:
            files_seleccionados.append(file_path)

        return files_seleccionados


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
