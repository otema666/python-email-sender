from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.coder import send_email, send_data, clear, animate_text
from colorama import Fore, init
import os 
import sys
init()


app = Flask(__name__)
CORS(app)

@app.route('/save_email', methods=['POST'])


def save_email():
    try:
        data = request.get_json()  # Lee los datos JSON del cuerpo de la solicitud
        address = data['address']
        subject = data['subject']
        message = data['message']
        # print(f"address: {address}\nsubject: {subject}\nmessage: {message}")
        
        send_data(address, subject, message)
        send_email(address, subject, message)

        response = {'message': 'Correo electrónico guardado exitosamente'}
        return jsonify(response), 200
    except Exception as e:
        error_response = {'error': str(e)}
        return jsonify(error_response), 400


if __name__ == '__main__':
    clear()
    animate_text("Servidor en escucha...", Fore.GREEN, 0.03)
    sys.stdout = open(os.devnull, 'w')
    app.run(port=5000, debug=False)
    
