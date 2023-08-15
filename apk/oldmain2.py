import smtplib
import base64
import re
import names
import cProfile

from email.mime.text import MIMEText
from email.utils import formataddr

from kivymd.app import MDApp
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.modalview import ModalView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from threading import Thread
from kivy.metrics import dp
from kivy.properties import BooleanProperty, StringProperty
from kivy.clock import Clock, mainthread
from kivy.lang.builder import Builder
from kivy.config import Config

Config.set('graphics', 'fullscreen', 'auto')
dark_theme = False
translations = {
    "Español": {
        "recipient_hint": u"Dirección de correo del destinatario",
        "subject_hint": "Asunto del correo",
        "message_hint": u"Escribe tu mensaje aquí",
        "send_button_text": "Enviar",
        "email_sent_success": "Correo enviado correctamente a {}.",
        "email_sent_error": "No se pudo enviar el correo. Inténtalo de nuevo.",
    },
    "English": {
        "recipient_hint": "Recipient's email address",
        "subject_hint": "Email subject",
        "message_hint": "Type your message here",
        "send_button_text": "Send",
        "email_sent_success": "Email sent successfully to {}.",
        "email_sent_error": "Failed to send the email. Please try again.",
    },
    u"Français": {
        "recipient_hint": "Adresse e-mail du destinataire",
        "subject_hint": u"Sujet de l'e-mail",
        "message_hint": "Tapez votre message ici",
        "send_button_text": "Envoyer",
        "email_sent_success": u"E-mail envoyé avec succès à {}.",
        "email_sent_error": u"Impossible d'envoyer l'e-mail. Veuillez réessayer.",
    },
    "简体中文": {
        "title": "邮件发送器 [size=30]v0.4[/size]",
        "recipient_hint": "收件人邮箱地址",
        "subject_hint": "邮件主题",
        "message_hint": "在这里输入您的消息",
        "send_button_text": "发送",
        "email_sent_success": "邮件成功发送至{}。",
        "email_sent_error": "发送邮件失败，请重试。",
    },
}

class EmailSender(Thread):
    def __init__(self, recipient, subject, message, e_username, e_password):
        super(EmailSender, self).__init__()
        self.recipient = recipient
        self.subject = subject
        self.message = message
        self.e_username = e_username
        self.e_password = e_password
        self.daemon = True

    def run(self):
        try:
            msg = MIMEText(self.message, 'plain', 'utf-8')
            msg['Subject'] = self.subject
            msg['From'] = formataddr((str(names.get_full_name()), self.descodear(self.e_username, 8)))
            msg['To'] = self.recipient

            server = smtplib.SMTP("smtp.zoho.eu", 587)
            server.starttls()
            server.login(self.descodear(self.e_username, 8), self.descodear(self.e_password, 12))
            server.sendmail(self.descodear(self.e_username, 8), self.recipient, msg.as_string())
            server.quit()

            self.email_sent_callback(True, "Correo enviado correctamente a {}.".format(self.recipient))
        except Exception as e:
            self.email_sent_callback(False, "No se pudo enviar el correo. Inténtalo de nuevo.")

    def email_sent_callback(self, boola, message):
        Clock.schedule_once(lambda dt: self.on_email_sent(boola, message), 0)

    @mainthread
    def on_email_sent(self, boola, message):
        app = App.get_running_app()
        if app and app.root:
            translated_message = translations[app.current_language].get("email_sent_success" if boola else "email_sent_error", message)
            app.root.handle_email_sent(boola, translated_message)

    @mainthread
    def update_ui(self, boola, message):
        app = App.get_running_app()
        if app and app.root:
            app.root.email_sent(boola, message)

    def descodear(self, texto, veces):
        for a in range(veces):
            decoded = base64.b64decode(texto).decode('utf-8')
            texto = decoded
        return decoded
    
    
class EmailWindow(FloatLayout):

    email_sent = BooleanProperty(False)
    countdown = StringProperty("")

    def send_email(self, *args):
        self.ids.spinner.active = True
        self.ids.send_button.disabled = True
        recipient = self.ids.recipient_input.text
        subject = self.ids.subject_input.text
        message = self.ids.message_input.text

        e_username = "Vm0xd1IyRnRVWGxWV0dSUFZsZG9WMWxyWkc5V2JHeDBaVVYwV0ZKdGVEQlVWbHBQWVd4S2MxWnFUbGhoTVVwRVZrZHplRll4VG5OYVJtUlhUVEpvYjFaclVrZFpWbHBYVTI1V2FGSnRhRmxWTUZaTFZGWmFjbHBFVWxwV2JIQjZWa2Q0VjFaSFNrbFJiVGxhVmtVMVJGUlhlR3RqYkd0NllVWlNUbFl4U2tsV1ZFa3hWakZXZEZOc2FHeFNhelZvVm1wT2IyRkdjRmhsUjNScVlrZFNlVll5ZUVOV01rVjNZMFpTVjFaV2NGTmFSRVpEVld4Q1ZVMUVNRDA9"
        e_password = "Vm0wd2QyUXlVWGxWV0d4WFlUSm9WMVl3Wkc5V2JHeDBaVVYwV0ZKdGVGWlZNbmhQVmpGYWMySkVUbGhoTVhCUVZteFZlRll5U2tWVWJHUnBWa1phZVZadE1UUlRNazE1Vkd0c2FsSnRhRzlVVmxaM1ZsWmtWMVp0UmxSTmJFcFlWVzAxVDJGV1NYZFhiRkpYWWxob2VsUlVSbUZrUjA1R1drWndWMDFFUlRCV01uUnZWakpHUjFOdVRtcFNiV2hoV1ZSR1lVMHhWWGhYYlVacVlraENSbFpYZUZOVWJVcEdZMFZ3VjJKSFVYZFdha1poVjBaT2NtRkdXbWhsYlhob1YxZDRiMkl4VGtkVmJGWlRZbFZhY1ZscldtRmxWbVJ5VjJzNVZXSkdjREZWVjNodlZqRktjMk5HYUZkaGEzQklWVEJhWVdSV1NuTlRiR1JUVFRBd01RPT0="

        email_sender_thread = EmailSender(recipient, subject, message, e_username, e_password)
        email_sender_thread.start()
    
    def enable_send_button(self):
        self.ids.send_button.disabled = False
        self.countdown = ""
        self.email_sent = False

    def start_countdown(self):
        self.ids.send_button.disabled = True
        self.countdown = "15"
        self.email_sent = True
        Clock.schedule_interval(self.update_countdown, 1)
    
    @mainthread
    def handle_email_sent(self, boola, message):
        self.ids.spinner.active = False
        self.ids.send_button.disabled = False
        self.ids.message_div.text = message
        if boola:
            self.start_countdown()

        # Hide the message label after 5 seconds
        Clock.schedule_once(lambda dt: self.hide_message_label(), 3)

    @mainthread
    def hide_message_label(self):
        self.ids.message_div.text = ""

    def update_countdown(self, dt):
        remaining_time = int(self.countdown) - 1
        if remaining_time > 0:
            self.countdown = str(remaining_time)
        else:
            Clock.unschedule(self.update_countdown)
            self.enable_send_button()


    @mainthread
    def email_sent(self, boola, message):
        self.ids.message_div.text = message
        if boola:
            self.start_countdown()

    def email_error(self, *args):
        txt = self.ids.recipient_input.text
        if re.match(r"^[\w\-\.]+@([\w\-]+\.)+[\w\-]{1,4}$", txt) or txt == "":
            self.ids.recipient_input.error = False
        else:
            self.ids.recipient_input.error = True
    
    def reload_translation(self):
        Builder.unload_file('main.kv')
        Builder.load_file('main.kv')

class EmailApp(MDApp):
    supported_languages = ["Español", "English", "Français", "简体中文"]
    current_language = StringProperty("English")

    def build(self):
        Builder.load_file('main.kv')
        self.profile = cProfile.Profile()
        self.profile.enable()
        self.theme_cls.primary_palette = ("Orange")
        self.theme_cls.theme_style = ("Dark")
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.material_style = "M3"
        self.email_window = EmailWindow()
        self.email_window.ids.spinner.active = False

        menu_items = [
            {
                "text": f"English",
                "viewclass": "OneLineListItem",
                "divider_color":  (0, 0, 0, 0),
                "on_release": lambda *args: self.set_language("English")
            },
            {
                "text": f"Español",
                "viewclass": "OneLineListItem",
                "divider_color":  (0, 0, 0, 0),
                "on_release": lambda *args: self.set_language("Español")
            },
            {
                "text": f"Français",
                "viewclass": "OneLineListItem",
                "divider_color":  (0, 0, 0, 0),
                "on_release": lambda *args: self.set_language("Français")
            }

        ]
        self.menu = MDDropdownMenu(
            caller=self.email_window.ids.lang_button,
            items=menu_items,
            width_mult=2,
            max_height=dp(125),
        )
        return self.email_window
    
    
    def open_language_dropdown(self):
       self.menu.open()

    def change_lang(self, lang):
        if lang in self.supported_languages:
            self.current_language = lang


    def switch_theme_style(self):
        global dark_theme
        if dark_theme: 
            self.theme_cls.primary_palette = ("Orange")
            self.theme_cls.theme_style = ("Dark")

        else:
            self.theme_cls.primary_palette = ("Blue")
            self.theme_cls.theme_style = ("Light")
        dark_theme = not dark_theme
        
    def toggle_theme(self, *args):
        # Use Clock to schedule the theme switch with a brief delay
        Clock.schedule_once(lambda dt: self.switch_theme_style())
        
    def set_language(self, language):
    # Implementa la lógica para cambiar el idioma
        self.current_language = language
        tr_lang = translations.get(language)


        self.email_window.ids.recipient_input.hint_text = tr_lang["recipient_hint"]
        self.email_window.ids.subject_input.hint_text = tr_lang["subject_hint"]
        self.email_window.ids.message_input.hint_text = tr_lang["message_hint"]
        self.email_window.ids.send_button.text = tr_lang["send_button_text"]


if __name__ == "__main__":
    email_app = EmailApp()
    email_app.run()
    email_app.profile.disable()
    email_app.profile.print_stats(sort='cumtime')