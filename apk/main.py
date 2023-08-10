import smtplib
import base64
import re
import platform
import names
import cProfile
import os
import math

from threading import Thread
from os.path import basename
from pathlib import Path

from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart

from plyer import accelerometer

from kivymd.tools.hotreload.app import MDApp
from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import BooleanProperty, StringProperty
from kivy.clock import Clock, mainthread
from kivy.lang.builder import Builder
from kivy.config import Config
from kivymd.toast import toast

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.modalview import ModalView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.filemanager import MDFileManager

Config.set('graphics', 'fullscreen', 'auto')
if platform.system() is not "":
    import android
    from android.storage import primary_external_storage_path
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

translations = {
    "Español": {
        "recipient_hint": u"Dirección de correo del destinatario",
        "subject_hint": "Asunto del correo",
        "message_hint": u"Escribe tu mensaje aquí",
        "send_button_text": "Enviar",
        "file_button_text": "Añadir archivos",
        "email_sent_success": "Correo enviado correctamente a {}",
        "email_sent_error": "No se pudo enviar el correo. Inténtalo de nuevo.",
    },
    "English": {
        "recipient_hint": "Recipient's email address",
        "subject_hint": "Email subject",
        "message_hint": "Type your message here",
        "send_button_text": "Send",
        "file_button_text": "Add files",
        "email_sent_success": "Email sent successfully to {}",
        "email_sent_error": "Failed to send the email. Please try again.",
    },
    u"Français": {
        "recipient_hint": "Adresse e-mail du destinataire",
        "subject_hint": u"Sujet de l'e-mail",
        "message_hint": "Tapez votre message ici",
        "send_button_text": "Envoyer",
        "file_button_text": "Ajouter des fichiers",
        "email_sent_success": u"E-mail envoyé avec succès à {}",
        "email_sent_error": u"Impossible d'envoyer l'e-mail. Veuillez réessayer.",
    },
    "简体中文": {
        "title": "邮件发送器 [size=30]v0.4[/size]",
        "recipient_hint": "收件人邮箱地址",
        "subject_hint": "邮件主题",
        "message_hint": "在这里输入您的消息",
        "send_button_text": "发送",
        "file_button_text": "添加文件",
        "email_sent_success": "邮件成功发送至{}",
        "email_sent_error": "发送邮件失败，请重试。",
    },
}

class EmailSender(Thread):
    def __init__(self, recipient, subject, message, e_username, e_password, selected_files=None):
        super(EmailSender, self).__init__()
        self.recipient = recipient
        self.subject = subject
        self.message = message
        self.e_username = e_username
        self.e_password = e_password
        self.daemon = True
        self.selected_files = selected_files

    def run(self):
        try:
            msg = MIMEMultipart()

            msg['Subject'] = self.subject
            msg['From'] = formataddr((str(names.get_full_name()), self.descodear(self.e_username, 8)))
            msg['To'] = self.recipient
            msg.attach(MIMEText(self.message))
            for f in self.selected_files or []:
                with open(f, "rb") as fil:
                    part = MIMEApplication(fil.read(), Name=basename(f))
                part.add_header('Content-Disposition',
                        'attachment; filename={}'.format(Path(f).name))
                msg.attach(part)
            
            server = smtplib.SMTP("smtp.zoho.eu", 587)
            server.starttls()
            server.login(self.descodear(self.e_username, 8), self.descodear(self.e_password, 12))
            server.sendmail(self.descodear(self.e_username, 8), self.recipient, msg.as_string())
            server.quit()

            self.email_sent_callback(True, self.recipient)
        except Exception as e:
            print(e)
            self.email_sent_callback(False, "No se pudo enviar el correo. Inténtalo de nuevo.")

    def email_sent_callback(self, boola, message):
        Clock.schedule_once(lambda dt: self.on_email_sent(boola, message), 0)

    @mainthread
    def on_email_sent(self, boola, rec):
        app = App.get_running_app()
        if app and app.root:
            if boola:
                translated_message = translations[app.current_language]["email_sent_success"].format(rec)
            else: 
                translated_message = translations[app.current_language]["email_sent_error"]
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
    selected_files = []

    def send_email(self, *args):
        self.ids.spinner.active = True
        self.ids.send_button.disabled = True
        recipient = self.ids.recipient_input.text
        subject = self.ids.subject_input.text
        message = self.ids.message_input.text
        selected_files = getattr(self, 'selected_files', [])

        e_username = "Vm0xd1IyRnRVWGxWV0dSUFZsZG9WMWxyWkc5V2JHeDBaVVYwV0ZKdGVEQlVWbHBQWVd4S2MxWnFUbGhoTVVwRVZrZHplRll4VG5OYVJtUlhUVEpvYjFaclVrZFpWbHBYVTI1V2FGSnRhRmxWTUZaTFZGWmFjbHBFVWxwV2JIQjZWa2Q0VjFaSFNrbFJiVGxhVmtVMVJGUlhlR3RqYkd0NllVWlNUbFl4U2tsV1ZFa3hWakZXZEZOc2FHeFNhelZvVm1wT2IyRkdjRmhsUjNScVlrZFNlVll5ZUVOV01rVjNZMFpTVjFaV2NGTmFSRVpEVld4Q1ZVMUVNRDA9"
        e_password = "Vm0wd2QyUXlVWGxWV0d4WFlUSm9WMVl3Wkc5V2JHeDBaVVYwV0ZKdGVGWlZNbmhQVmpGYWMySkVUbGhoTVhCUVZteFZlRll5U2tWVWJHUnBWa1phZVZadE1UUlRNazE1Vkd0c2FsSnRhRzlVVmxaM1ZsWmtWMVp0UmxSTmJFcFlWVzAxVDJGV1NYZFhiRkpYWWxob2VsUlVSbUZrUjA1R1drWndWMDFFUlRCV01uUnZWakpHUjFOdVRtcFNiV2hoV1ZSR1lVMHhWWGhYYlVacVlraENSbFpYZUZOVWJVcEdZMFZ3VjJKSFVYZFdha1poVjBaT2NtRkdXbWhsYlhob1YxZDRiMkl4VGtkVmJGWlRZbFZhY1ZscldtRmxWbVJ5VjJzNVZXSkdjREZWVjNodlZqRktjMk5HYUZkaGEzQklWVEJhWVdSV1NuTlRiR1JUVFRBd01RPT0="

        email_sender_thread = EmailSender(recipient, subject, message, e_username, e_password, selected_files)
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
    
    def handle_email_sent(self, boola, message):
        # Hide the spinner and enable the "Send" button after the email is sent or an error occurs
        app = App.get_running_app()
        self.ids.spinner.active = False
        self.ids.send_button.disabled = False
        self.ids.message_div.text = message
        app.filesyesno = False
        if boola:
            self.ids.file_button.text =  translations[app.current_language]["file_button_text"]
            self.ids.file_button.icon = "file-plus"
            self.selected_files = []
            self.start_countdown()

        Clock.schedule_once(lambda dt: self.hide_message_label(), 3)

    def hide_message_label(self):
        self.ids.message_div.text = ""

    def update_countdown(self, dt):
        remaining_time = int(self.countdown) - 1
        if remaining_time > 0:
            self.countdown = str(remaining_time)
        else:
            Clock.unschedule(self.update_countdown)
            self.enable_send_button()

    def email_sent(self, boola, message):
        self.ids.message_div.text = message
        if boola:
            self.ids.send_button.disabled = True
            self.start_countdown()

    def email_error(self, *args):
        txt = self.ids.recipient_input.text
        if re.match(r"^[\w\-\.]+@([\w\-]+\.)+[\w\-]{1,4}$", txt) or txt == "":
            self.ids.recipient_input.error = False
        else:
            self.ids.recipient_input.error = True
            
    def update_line_col(self):
        blue = (0.1294, 0.5882, 0.9529, 1.0)
        orange = (1.0, 0.5961, 0.0, 1.0)
        if not self.dark_theme: 
            self.ids.recipient_input.line_color_focus = orange
            self.ids.subject_input.line_color_focus = orange
            self.ids.message_input.line_color_focus = orange
        else:
            self.ids.recipient_input.line_color_focus = blue
            self.ids.subject_input.line_color_focus = blue
            self.ids.message_input.line_color_focus = blue

    def reload_translation(self):
        Builder.unload_file('main.kv')
        Builder.load_file('main.kv')
        
    def select_path(self, path):
        self.selected_files = [path]  # Update the selected_files attribute
        self.ids.file_button.text = self.truncate_filename(str(os.path.basename(self.selected_files[0])), 30)
        self.ids.file_button.icon = "paperclip"
        app = App.get_running_app()
        app.filesyesno = True
        blue = (0.1294, 0.5882, 0.9529, 1.0)
        orange = (1.0, 0.5961, 0.0, 1.0)
        if app.filesyesno:
            if app.firsttimechange:
                app.root.ids.file_button.line_color = orange
                app.root.ids.file_button.icon_color = orange
                app.root.ids.file_button.text_color = (1, 1, 1, 1)
            else:
                if app.dark_theme: 
                    app.root.ids.file_button.line_color = orange
                    app.root.ids.file_button.icon_color = orange
                    app.root.ids.file_button.text_color = (1, 1, 1, 1)
                else:
                    app.root.ids.file_button.line_color = blue
                    app.root.ids.file_button.icon_color = blue
                    app.root.ids.file_button.text_color = (0, 0, 0, 1)
        else:
            app.root.ids.file_button.line_color = (0.3765, 0.4902, 0.5451, 1.0000)
        
        app.file_manager.close()
        
    def truncate_filename(self, filename, max_length):
        if len(filename) <= max_length:
            return filename
        
        first_part_length = (max_length - 3) // 2  # Leave space for "..."
        last_part_length = max_length - 3 - first_part_length
        truncated_filename = f"{filename[:first_part_length]}...{filename[-last_part_length:]}"
        return truncated_filename

class EmailApp(MDApp):
    current_language = StringProperty("English")
    theme_changing = False
    palette = ("Orange")
    style = ("Dark")
    dark_theme = True
    firsttimechange = True
    filesyesno = False
    selected_files = []
    
    def reloadkv():
        try:
            # Load the KV file again using Builder
            Builder.unload_file('main.kv')
            Builder.load_file('main.kv')
            print("KV file reloaded successfully.")
        except Exception as e:
            print("Error while reloading the KV file:", e)

    def build(self):
        Builder.load_file('main.kv')
        self.profile = cProfile.Profile()
        self.profile.enable()
        try:
            accelerometer.enable()
            print("acce enabled")
            Window.bind(on_accelerometer=accelerometer.acceleration)
            self.last_acceleration = (0, 0, 0)
        except NotImplementedError:
            print("acce disabled")
       
        self.shake_threshold = 10  # Adjust this threshold as needed
        self.theme_cls.primary_palette = ("BlueGray")
        self.theme_cls.theme_style = ("Dark")
        self.primary_text_color_rgba = [1, 1, 1, 1]

        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.material_style = "M3"
        self.theme_changing = False
        self.manager_open = False
    
        self.email_window = EmailWindow()
        self.email_window.ids.spinner.active = False

        menu_items = [
            {
                "text": f"English",
                "theme_text_color": "Custom",
                "text_color": (1,1,1,1),
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
            elevation=2
        )
        self.file_manager = MDFileManager(
            exit_manager=self.exit_file_manager,
            select_path=self.select_path,
            preview=False,
            sort_by="date",
        )
        return self.email_window
    
    def file_manager_open(self):
        self.file_manager.show(os.path.join(os.getenv('EXTERNAL_STORAGE'), 'Download'))
        self.manager_open = True

    def exit_file_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()
        
    def select_path(self, path):
        app = App.get_running_app()
        app.root.select_path(path)
        
    def update_selected_files(self, selected_files):
        self.selected_files = selected_files
    
    def events(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True
    
    def open_language_dropdown(self):
       self.menu.open()

    def change_lang(self, lang):
        self.current_language = lang
            
    def toggle_theme(self, *args):
        if not self.theme_changing:
            self.theme_changing = True
            self.theme_change_button_disabled = True

            # Schedule the theme switch with a brief delay
            Clock.schedule_once(self.switch_theme_style, 0.1)
            # Schedule the message update after a longer delay
            Clock.schedule_once(self.update_message, 0.5)

    def switch_theme_style(self, dt=None):
        blue = (0.1294, 0.5882, 0.9529, 1.0)
        orange = (1.0, 0.5961, 0.0, 1.0)
        app = App.get_running_app()
        self.firsttimechange = False
        if not self.dark_theme: 
            self.theme_cls.primary_palette = ("Orange")
            self.theme_cls.theme_style = "Dark"
            app.root.ids.title_label.text_color = (1, 1, 1, 1)
            app.root.ids.message_div.text_color = (1, 1, 1, 1)
            app.root.ids.file_button.text_color = (1, 1, 1, 1)
            
            app.root.ids.lang_button.icon_color = (1, 1, 1, 1)
            
            app.root.ids.theme_button.md_bg_color = orange
            app.root.ids.theme_button.text_color = (0, 0, 0, 1)
            
            app.root.ids.send_button.line_color = orange
            app.root.ids.send_button.text_color = orange
            if self.filesyesno:
                app.root.ids.file_button.line_color = orange
                app.root.ids.file_button.icon_color = orange
            else:
                app.root.ids.file_button.line_color = (0.3765, 0.4902, 0.5451, 1.0000)
                app.root.ids.file_button.icon_color = (0.3765, 0.4902, 0.5451, 1.0000)
            
            self.menu.items[0]["text_color"] = (1, 1, 1, 1)
            self.menu.items[1]["text_color"] = (1, 1, 1, 1)
            self.menu.items[2]["text_color"] = (1, 1, 1, 1)
            
            app.root.ids.spinner.color = orange

        else:
            self.theme_cls.primary_palette = ("Blue")
            self.theme_cls.theme_style = "Light"
            app.root.ids.title_label.text_color = (0, 0, 0, 1)
            app.root.ids.message_div.text_color = (0, 0, 0, 1)
            app.root.ids.file_button.text_color = (0, 0, 0, 1)
            
            app.root.ids.lang_button.icon_color = (0, 0, 0, 1)
            
            app.root.ids.theme_button.md_bg_color = blue
            app.root.ids.theme_button.text_color = (1, 1, 1, 1)
            
            app.root.ids.send_button.line_color = blue
            app.root.ids.send_button.text_color = blue
            if self.filesyesno:
                app.root.ids.file_button.line_color = blue
                app.root.ids.file_button.icon_color = blue
            else:
                app.root.ids.file_button.line_color = (0.3765, 0.4902, 0.5451, 1.0000)
                app.root.ids.file_button.icon_color = (0.3765, 0.4902, 0.5451, 1.0000)
            
            self.menu.items[0]["text_color"] = (0, 0, 0, 1)
            self.menu.items[1]["text_color"] = (0, 0, 0, 1)
            self.menu.items[2]["text_color"] = (0, 0, 0, 1)
            
            app.root.ids.spinner.color = blue
        
        self.dark_theme = not self.dark_theme
        
    def update_message(self, dt):

        # Enable the theme change button after the theme is changed and message is updated
        Clock.schedule_once(lambda dt: setattr(self, 'theme_change_button_disabled', False), 0.1)
        # Reset theme_changing after the theme change is complete
        Clock.schedule_once(lambda dt: setattr(self, 'theme_changing', False), 0.1)

        
    def set_language(self, language):
    # Implementa la lógica para cambiar el idioma
        self.current_language = language
        tr_lang = translations.get(language)
        if language == "简体中文":
            font = "chinese.ttf"
        else:
            font = "Roboto"

        self.email_window.ids.recipient_input.hint_text = tr_lang["recipient_hint"]
        self.email_window.ids.subject_input.hint_text = tr_lang["subject_hint"]
        self.email_window.ids.message_input.hint_text = tr_lang["message_hint"]
        self.email_window.ids.send_button.text = tr_lang["send_button_text"]
        if not self.filesyesno:
            self.email_window.ids.file_button.text = tr_lang["file_button_text"]
        
        self.email_window.ids.recipient_input.font_name = font
        self.email_window.ids.subject_input.font_name = font
        self.email_window.ids.message_input.font_name = font
        self.email_window.ids.send_button.font_name = font
        self.email_window.ids.file_button.font_name = font
        
    def on_accelerometer(self, instance, acceleration):
        x, y, z = acceleration
        delta_x = abs(x - self.last_acceleration[0])
        delta_y = abs(y - self.last_acceleration[1])
        delta_z = abs(z - self.last_acceleration[2])
        total_delta = math.sqrt(delta_x**2 + delta_y**2 + delta_z**2)

        if total_delta > self.shake_threshold:
            self.handle_shake_event()
        
        self.last_acceleration = (x, y, z)
        print(acceleration)

    def handle_shake_event(self):
        print("Phone was shaken!")

if __name__ == "__main__":
    email_app = EmailApp()
    email_app.run()