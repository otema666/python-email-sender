import sys
import base64
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QSizePolicy,
    QPushButton, QVBoxLayout, QFormLayout, QMessageBox
)
from PyQt6.QtGui import QFont, QMovie, QPixmap
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QCoreApplication, QRect

class EmailSender(QThread):
    email_sent = pyqtSignal(bool, str)

    def __init__(self, recipient, subject, message, e_username, e_password):
        super().__init__()
        self.recipient = recipient
        self.subject = subject
        self.message = message
        self.e_username = e_username
        self.e_password = e_password

    def run(self):
        try:
            msg = MIMEText(self.message, 'plain', 'utf-8')
            msg['Subject'] = self.subject
            msg['From'] = formataddr(("супер классный", self.descodear(self.e_username, 8)))
            msg['To'] = self.recipient

            server = smtplib.SMTP("smtp.zoho.eu", 587)
            server.starttls()
            server.login(self.descodear(self.e_username, 8), self.descodear(self.e_password, 12))
            server.sendmail(self.descodear(self.e_username, 8), self.recipient, msg.as_string())
            server.quit()
            print("hiiiiii")
            self.email_sent.emit(True, "hi")
        except Exception as e:
            self.email_sent.emit(False, "a")

    def descodear(self, texto, veces):
        for a in range(veces):
            decoded = base64.b64decode(texto).decode('utf-8')
            texto = decoded
        return decoded

class EmailWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python Email Sender GUI")
        self.setFixedSize(400, 350)
        self.layout = QVBoxLayout()

        self.form_layout = QFormLayout()

        self.recipient_input = QLineEdit(self)
        self.recipient_input.setPlaceholderText("Dirección de correo del destinatario")
        self.form_layout.addRow("Para:", self.recipient_input)
        self.recipient_input.textChanged.connect(self.enable_send_button)
        self.recipient_input.setStyleSheet("""
            QLineEdit {
                border: none;
                border-bottom: 1px solid #bdc3c7;
                padding: 8px;
                font-size: 14px;
            }
        """)

        self.subject_input = QLineEdit(self)
        self.subject_input.setPlaceholderText("Asunto del correo")
        self.form_layout.addRow("Asunto:", self.subject_input)
        self.subject_input.textChanged.connect(self.enable_send_button)
        self.subject_input.setStyleSheet("""
            QLineEdit {
                border: none;
                border-bottom: 1px solid #bdc3c7;
                padding: 8px;
                font-size: 14px;
            }
        """)

        self.message_input = QTextEdit(self)
        self.message_input.setPlaceholderText("Escribe tu mensaje aquí")
        self.form_layout.addRow("Mensaje:", self.message_input)
        self.message_input.textChanged.connect(self.enable_send_button)
        self.message_input.setStyleSheet("""
            QTextEdit {
                border: none;
                border-bottom: 1px solid #bdc3c7;
                padding: 8px;
                font-size: 14px;
            }
        """)

        # Asegurar que el input del mensaje tenga igual anchura que los demás inputs
        self.message_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)    

        self.send_button = QPushButton("Enviar")
        self.send_button.setEnabled(False)
        self.send_button.clicked.connect(self.send_email)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #27ae60;
            }

            QPushButton:pressed {
                background-color: #1f9452;
            }
            
            QPushButton:disabled {
                background-color: #bdc3c7; /* Gris */
                color: #7f8c8d;
            }
        """)

        self.layout.addLayout(self.form_layout)
        self.layout.addWidget(self.send_button)

        self.message_div = QLabel()
        self.layout.addWidget(self.message_div)

        # LOADING
        self.loading_widget = QWidget(self)
        self.loading_widget.setObjectName("loadingWidget")
        self.loading_widget.hide()

        self.loading_layout = QVBoxLayout(self.loading_widget)
        self.loading_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.loading_label = QLabel(self.loading_widget)
        self.movie = QMovie("load.gif")  # Coloca la ruta de tu animación de carga aquí
        self.loading_label.setMovie(self.movie)
        self.loading_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.movie.start()

        self.loading_layout.addWidget(self.loading_label)
        self.loading_widget.setStyleSheet("background-color: transparent; border: none;")
        self.loading_widget.setStyleSheet(
            """
            #loadingWidget {
                background-color: transparent;
                border: none;
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
            }
            """
        )
        
        self.setLayout(self.layout)

        self.email_sender = None

    def send_email(self):
        recipient = self.recipient_input.text()
        subject = self.subject_input.text()
        message = self.message_input.toPlainText()

        e_username = "Vm0xd1IyRnRVWGxWV0dSUFZsZG9WMWxyWkc5V2JHeDBaVVYwV0ZKdGVEQlVWbHBQWVd4S2MxWnFUbGhoTVVwRVZrZHplRll4VG5OYVJtUlhUVEpvYjFaclVrZFpWbHBYVTI1V2FGSnRhRmxWTUZaTFZGWmFjbHBFVWxwV2JIQjZWa2Q0VjFaSFNrbFJiVGxhVmtVMVJGUlhlR3RqYkd0NllVWlNUbFl4U2tsV1ZFa3hWakZXZEZOc2FHeFNhelZvVm1wT2IyRkdjRmhsUjNScVlrZFNlVll5ZUVOV01rVjNZMFpTVjFaV2NGTmFSRVpEVld4Q1ZVMUVNRDA9"
        e_password = "Vm0wd2QyUXlVWGxWV0d4WFlUSm9WMVl3Wkc5V2JHeDBaVVYwV0ZKdGVGWlZNbmhQVmpGYWMySkVUbGhoTVhCUVZteFZlRll5U2tWVWJHUnBWa1phZVZadE1UUlRNazE1Vkd0c2FsSnRhRzlVVmxaM1ZsWmtWMVp0UmxSTmJFcFlWVzAxVDJGV1NYZFhiRkpYWWxob2VsUlVSbUZrUjA1R1drWndWMDFFUlRCV01uUnZWakpHUjFOdVRtcFNiV2hoV1ZSR1lVMHhWWGhYYlVacVlraENSbFpYZUZOVWJVcEdZMFZ3VjJKSFVYZFdha1poVjBaT2NtRkdXbWhsYlhob1YxZDRiMkl4VGtkVmJGWlRZbFZhY1ZscldtRmxWbVJ5VjJzNVZXSkdjREZWVjNodlZqRktjMk5HYUZkaGEzQklWVEJhWVdSV1NuTlRiR1JUVFRBd01RPT0="


        self.send_button.setEnabled(False)  # Deshabilitar el botón mientras se envía el correo
        self.loading_widget.show()  # Mostrar el widget de carga

        self.email_sender = EmailSender(recipient, subject, message, e_username, e_password)
        self.email_sender.email_sent.connect(self.on_email_sent)  # Connect only to the email_sent signal
        self.email_sender.start()


    def on_email_sent(self, boola, message):
        self.send_button.setEnabled(True)
        self.loading_widget.hide()  # Hide the loading widget
        if boola:
            self.message_div.setText(f'Correo enviado correctamente a {self.recipient_input.text()}.')

        else:
            self.message_div.setText(f'No se pudo enviar el correo. Inténtalo de nuevo.')

    def enable_send_button(self):
        recipient = self.recipient_input.text()
        subject = self.subject_input.text()
        message = self.message_input.toPlainText()
        self.send_button.setEnabled(bool(recipient and subject and message))
        
    def resizeEvent(self, event):
        # Redimensionar el widget de carga para que ocupe todo el espacio del widget principal
        self.loading_widget.resize(self.size())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    window = EmailWindow()
    window.show()
    sys.exit(app.exec())