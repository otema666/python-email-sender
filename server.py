from http.server import BaseHTTPRequestHandler, HTTPServer
import json

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
        else:
            self.send_error(404, 'File not found')

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

            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'status': 'success'}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_error(404, 'File not found')


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Puerto {port} en escucha (minimice esta ventana)...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
