import random
import smtplib
import sqlite3
import string
import socket
from ctypes import windll
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import sample
from tkinter import messagebox, Tk
import sys
import pathlib
import yadisk
from PyQt5.QtCore import QSize, Qt, QBasicTimer
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import *
from PyQt5.uic.properties import QtGui

import httplib2
#import apiclient.discovery
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import os
from PyQt5 import QtGui
from PyQt5 import QtWidgets

try:
    # Включите в блок try/except, если вы также нацелены на Mac/Linux
    from PyQt5.QtWinExtras import QtWin                                         #  !!!
    myappid = 'mycompany.myproduct.subproduct.version'                          #  !!!
    QtWin.setCurrentProcessExplicitAppUserModelID(myappid)                      #  !!!
except ImportError as e:
    print(e)

# .. или так ..                                                                 #  !!!
#import ctypes
#myappid = 'mycompany.myproduct.subproduct.version'
#ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
def add_file(file):
    y = yadisk.YaDisk(token="AgAAAABJRyuzAAa6pTvMKnWv4Eeos3P4GVqkqmU")
    if os.path.isfile(file):
        if not y.is_file(os.path.basename(file)):
            y.upload(file, os.path.basename(file))
            return True, 'ok'
        return False, 'file_already_in_disk'
    return False, 'no_such_file'


def download_file(file):
    y = yadisk.YaDisk(token="AgAAAABJRyuzAAa6pTvMKnWv4Eeos3P4GVqkqmU")
    if os.path.isfile(file + '.sqlite3'):
        return False, 'file_already_exists'
    if y.is_file(file + '.sqlite3'):
        try:
            y.download(file + '.sqlite3', file + '.sqlite3')
        except Exception:
            return False, 'no_internet'
        return True, 'ok'
    return False, 'no_such_file'


def delete_file(file):
    y = yadisk.YaDisk(token="AgAAAABJRyuzAAa6pTvMKnWv4Eeos3P4GVqkqmU")
    if y.is_file(file):
        y.remove(file, permanently=True)
        return True, 'ok'
    return False, 'no_such_file'


# создание нового аккаунта (занесение данных в я.диск и гугл таблицы)
def add_new_account(nickname, password, email):
    try:
        # Файл, полученный в Google Developer Console
        with open('creds.json', 'w+', encoding='utf-8') as f:
                f.write(r'''{
  "type": "service_account",
  "project_id": "oauth-295813",
  "private_key_id": "ae9ba005a85bd0c230cdc752213ad1ef321e1ad1",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDT9TSA+4Fe78QQ\nMV+4H7TVNpZtTWZgnqH6gedktJKeyDfis0C1vbts+St/2GJSERj8HXTatrlZZ7Gm\nSCb+VShd15ks9wWvOEjpreL0awDC4+uk+xbqVrb7+jaqHbgPGZllalrjG06osOeQ\nQGYZ7pRxmFPun/yhdmLXQWKF5s79eWjdLKzZlsT5EJ7I0oCVt4ego5A0zkf1tlKw\n14stx8CKirmRzQI0E3WvVRisMFlTDkqLKLb15dSX3IAuAmMsjrP2l83m/ayAyBkV\nebMfqi7/Bc1b4wGjPy/PavBWT73qpA6ubZi/877kmMkTlqlROg0pg9L90ehjY17q\nkw3s5g0NAgMBAAECggEAJTxeRyuH8H70JXkbDPxq9wsCNb0Dd4VexOS12yP63xCi\n+r1NaLAmgVArw2em7C5rQn1FRlgT60AzfhgOW59nukayNutFkSD09DJzXMeAiHxk\nbSUcQzpNJqqwGEYky+hOIbojseKd+LYtVBLwLO2UH/moAxORnObwmcq3jXj9E5vD\nBxAdY91NC+zV8DMm1U3CgGzuFX6VGqulQKa1tanCDJD7KFT9f1MhAP329hBxzHnT\nVLX9cW+zyhg81+J1QiKW6kP7NZkzHLW0ULhZCVEcCGXrdRmq+j1yGyTrZDL1EX2V\nOTWk5/xxXxomreG4XngmoPaD3wGpXR/wjSLOzj6jMQKBgQDp8CKZohrpYZBNa1cA\n9wK2ioW690pc30DeQ+ScqRltSuKk28T99GKBR2hooeOSLMhWKHTZ3e2GWC5H4aZj\nSBhM1+X1Ak1p1u4w3ilWlIh0goiyNhZsHMadTMlP+YxZ1rd/vu4K/kvFeX9G9qNQ\nRs5BnZxnylZzOQUpfSjGlt4zkQKBgQDn8mlcFnGMVEf4n50ViVvAkSmRQfhDFtel\nucRbhhw8IL5LZEZKS0AxREbO5BimgoqN/znfQIjw4cOIpfBBaBIe5yz0CQRzEla2\nhwu/ucibfA/M/vC1hhsWbhXdrz4ieryKyDvW2hoCzPZIB0BPP1cs34tS8/0gG/sJ\nGvV3kZbLvQKBgQDgN9cR5XthwK8sZPtI43doOjCe2LIffaOQ5QXS2YiTZjkAxdtz\nhK59NlHuJ2wVCHMjkTceMkWchBwnrTFq6wjPbgbr5D8KeIRntids4oQ/F3WpSYoI\nKTR8Q8KXsplA6jmKaReC1eUN6ruA6pfxM0wxO71TBW4Cld5Ku7k/Tg6+4QKBgGpM\nk3KrqoBIg+9ynxgmqlEXdfhnRnLgvhXqjA3x6XC5BN0iaIBV+mZZxyW8LXvqKbun\n84rYVaonnWg7vF8NZfiZs+VnWI2wIuNmAsFsUH7JnagyUniurC1caFL/pDdDDrN/\nzsTJkdAkxN3/zL5E5hvfm0d6IFCd4i+rFkIlC/n1AoGAFp8OzAFNMMitGUjihWmo\nCiMq7b61Ax3HJOFnpOjjfm2hubt0Y9bff6+ZGtL7lYApRKLsbsUI2YFeVut/SdLt\nSnHV1ivvqI7WARYWr9ptCySoQd0ItJx/jWGRvkFbniKc7ExtMRjn3wbywUsxDc+A\nNCU2v305mkg7lyj+2mIYYj4=\n-----END PRIVATE KEY-----\n",
  "client_email": "account@oauth-295813.iam.gserviceaccount.com",
  "client_id": "108851297345893727832",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/account%40oauth-295813.iam.gserviceaccount.com"
}
''')
        CREDENTIALS_FILE = 'creds.json'
        # ID Google Sheets документа (можно взять из его URL)
        spreadsheet_id = '1Lpw-IZkFWylk8FL1Q0jEDhurokJtNlepX9sQAUp7bPw'

        # Авторизуемся и получаем service — экземпляр доступа к API
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            CREDENTIALS_FILE,
            ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())
        service = build('sheets', 'v4', http=httpAuth)
        # Пример чтения файла
        values = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range='A1:A1',
            majorDimension='COLUMNS'
        ).execute()
        count = int(values['values'][0][0])
        values = service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": "A1:A1",
                     "majorDimension": 'ROWS',
                     "values": [[f'{count + 1}']]}
                ]
            }
        ).execute()
        values = service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": f"A{count}:C{count}",
                     "majorDimension": 'COLUMNS',
                     "values": [[f'{nickname}'], [f'{password}'],
                                [f'{email}']]}
                ]
            }
        ).execute()
        file = pathlib.Path('creds.json')
        file.unlink()
        # создание БД
        with sqlite3.connect(f'{nickname}.sqlite3') as con:
            cur = con.cursor()
            # добавление таблицы в БД, в которой хранятся данные о достижениях в игре
            cur.execute("""CREATE TABLE IF NOT EXISTS datas(
                                                        total_games TEXT, 
                                                        total_count TEXT,
                                                        max_count TEXT,
                                                        medium_count TEXT);
                                                        """)
            con.commit()
            # добавление таблицы в БД, в которой хранятся настройки аккаунта
            cur.execute("""CREATE TABLE IF NOT EXISTS settings(
                                                                   font TEXT, 
                                                                   backcolor TEXT,
                                                                   textcolor TEXT,
                                                                   buttoncolor TEXT,
                                                                   speed TEXT,
                                                                   prep TEXT,
                                                                   size TEXT);
                                                                   """)
            con.commit()
            cur.execute("""CREATE TABLE IF NOT EXISTS password(
                        password TEXT);""")
            con.commit()
            cur.execute(
                """INSERT INTO password VALUES('{}')""".format(password))
            con.commit()


        ## здесь заносятся настройки по умолчанию. Тип шрифта и данные о цветах
        with sqlite3.connect(f'{nickname}.sqlite3') as con:
            cur = con.cursor()
            font, button_color, background, text, speed, prep, size = ['Arial',
                                                       'rgb(144, 238, 144);',
                                                       'rgb(255, 0, 0);',
                                                       'rgb(154, 154, 170);','1', '0', '1']
            cur.execute("""INSERT INTO  settings VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(font, background, text, button_color, speed, prep, size))
            con.commit()
            datas = [0] * 4
            cur.execute(
                """INSERT INTO  datas VALUES('{}', '{}', '{}', '{}')""".format(*datas))
            con.commit()
        with sqlite3.connect(f'{nickname}.sqlite3') as con:
            cur = con.cursor()
        add_file(f'{nickname}.sqlite3')
        for i in range(10):
            try:
                con.close()
            except:
                pass
        file = pathlib.Path(f'{nickname}.sqlite3')
        file.unlink()
    except Exception as e:
        if not os.path.isdir('Змейка'):
            print(e.args)
            root = Tk()
            root.withdraw()
            messagebox.showerror('Змейка',
                                 'Критическая ошибка: невозможно загрузить данные. Проверьте подключение к интернету.')
            root.destroy()
            try:
                file = pathlib.Path('creds.json')
                file.unlink()
            except Exception:
                pass
        else:
            pass


#  получение данных о аккаунтах в виде словаря
def get_accounts():
    try:
        # Файл, полученный в Google Developer Console
        with open('creds.json', 'w+', encoding='utf-8') as f:
                f.write(r'''{
          "type": "service_account",
          "project_id": "oauth-295813",
          "private_key_id": "ae9ba005a85bd0c230cdc752213ad1ef321e1ad1",
          "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDT9TSA+4Fe78QQ\nMV+4H7TVNpZtTWZgnqH6gedktJKeyDfis0C1vbts+St/2GJSERj8HXTatrlZZ7Gm\nSCb+VShd15ks9wWvOEjpreL0awDC4+uk+xbqVrb7+jaqHbgPGZllalrjG06osOeQ\nQGYZ7pRxmFPun/yhdmLXQWKF5s79eWjdLKzZlsT5EJ7I0oCVt4ego5A0zkf1tlKw\n14stx8CKirmRzQI0E3WvVRisMFlTDkqLKLb15dSX3IAuAmMsjrP2l83m/ayAyBkV\nebMfqi7/Bc1b4wGjPy/PavBWT73qpA6ubZi/877kmMkTlqlROg0pg9L90ehjY17q\nkw3s5g0NAgMBAAECggEAJTxeRyuH8H70JXkbDPxq9wsCNb0Dd4VexOS12yP63xCi\n+r1NaLAmgVArw2em7C5rQn1FRlgT60AzfhgOW59nukayNutFkSD09DJzXMeAiHxk\nbSUcQzpNJqqwGEYky+hOIbojseKd+LYtVBLwLO2UH/moAxORnObwmcq3jXj9E5vD\nBxAdY91NC+zV8DMm1U3CgGzuFX6VGqulQKa1tanCDJD7KFT9f1MhAP329hBxzHnT\nVLX9cW+zyhg81+J1QiKW6kP7NZkzHLW0ULhZCVEcCGXrdRmq+j1yGyTrZDL1EX2V\nOTWk5/xxXxomreG4XngmoPaD3wGpXR/wjSLOzj6jMQKBgQDp8CKZohrpYZBNa1cA\n9wK2ioW690pc30DeQ+ScqRltSuKk28T99GKBR2hooeOSLMhWKHTZ3e2GWC5H4aZj\nSBhM1+X1Ak1p1u4w3ilWlIh0goiyNhZsHMadTMlP+YxZ1rd/vu4K/kvFeX9G9qNQ\nRs5BnZxnylZzOQUpfSjGlt4zkQKBgQDn8mlcFnGMVEf4n50ViVvAkSmRQfhDFtel\nucRbhhw8IL5LZEZKS0AxREbO5BimgoqN/znfQIjw4cOIpfBBaBIe5yz0CQRzEla2\nhwu/ucibfA/M/vC1hhsWbhXdrz4ieryKyDvW2hoCzPZIB0BPP1cs34tS8/0gG/sJ\nGvV3kZbLvQKBgQDgN9cR5XthwK8sZPtI43doOjCe2LIffaOQ5QXS2YiTZjkAxdtz\nhK59NlHuJ2wVCHMjkTceMkWchBwnrTFq6wjPbgbr5D8KeIRntids4oQ/F3WpSYoI\nKTR8Q8KXsplA6jmKaReC1eUN6ruA6pfxM0wxO71TBW4Cld5Ku7k/Tg6+4QKBgGpM\nk3KrqoBIg+9ynxgmqlEXdfhnRnLgvhXqjA3x6XC5BN0iaIBV+mZZxyW8LXvqKbun\n84rYVaonnWg7vF8NZfiZs+VnWI2wIuNmAsFsUH7JnagyUniurC1caFL/pDdDDrN/\nzsTJkdAkxN3/zL5E5hvfm0d6IFCd4i+rFkIlC/n1AoGAFp8OzAFNMMitGUjihWmo\nCiMq7b61Ax3HJOFnpOjjfm2hubt0Y9bff6+ZGtL7lYApRKLsbsUI2YFeVut/SdLt\nSnHV1ivvqI7WARYWr9ptCySoQd0ItJx/jWGRvkFbniKc7ExtMRjn3wbywUsxDc+A\nNCU2v305mkg7lyj+2mIYYj4=\n-----END PRIVATE KEY-----\n",
          "client_email": "account@oauth-295813.iam.gserviceaccount.com",
          "client_id": "108851297345893727832",
          "auth_uri": "https://accounts.google.com/o/oauth2/auth",
          "token_uri": "https://oauth2.googleapis.com/token",
          "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
          "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/account%40oauth-295813.iam.gserviceaccount.com"
        }
        ''')
        CREDENTIALS_FILE = 'creds.json'
        # ID Google Sheets документа (можно взять из его URL)
        spreadsheet_id = '1Lpw-IZkFWylk8FL1Q0jEDhurokJtNlepX9sQAUp7bPw'
        # Авторизуемся и получаем service — экземпляр доступа к API
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            CREDENTIALS_FILE,
            ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())
        service = build('sheets', 'v4', http=httpAuth)
        # Пример чтения файла
        values = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range='A1:A1',
            majorDimension='COLUMNS'
        ).execute()
        count = int(values['values'][0][0])
        values = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=f'A2:C{count}',
            majorDimension='COLUMNS'
        ).execute()
        values = values['values']
        datas = {}
        for i in values:
            datas[i[0]] = i[1:]
        file = pathlib.Path('creds.json')
        file.unlink()
        return datas
    except Exception as e:
        pass



        root = Tk()
        root.withdraw()
        messagebox.showerror('Змейка',
                             'Критическая ошибка: невозможно загрузить данные. Проверьте подключение к интернету.')
        root.destroy()
        try:
            file = pathlib.Path('creds.json')
            file.unlink()
        except Exception:
            pass



accounts: list
emails: list
passwors: list
L: int
h: int


def get_dates():
    global accounts, emails, passwords, L, H
    flag = True
    try:
        socket.gethostbyaddr("www.yandex.ru")
    except Exception:
        if os.path.isdir('Змейка'):
            flag = False
        else:
            return False, False
    if flag:
        help_param = get_accounts()
        accounts = help_param['account']
        accounts.append('None')
        accounts.append('none')
        emails = help_param['email']
        passwords = help_param['password']
        L = 1920
        H = 1080
    else:
        accounts = [i[:-8] for i in (os.listdir('Змейка'))]
        os.chdir('Змейка')
        a = os.listdir()[0]
        with sqlite3.connect(a) as con:
            cur = con.cursor()
            # добавление таблицы в БД, в которой хранятся данные о достижениях в игре
            password = (cur.execute("""SELECT * FROM password""").fetchall()[0][0])
def update():
    global accounts, emails, passwords
    try:
        help_param = get_accounts()
    except Exception as e:
        root = Tk()
        root.withdraw()
        messagebox.showerror('Авторизация', 'Невозможно загрузить данные.')
        root.destroy()
        sys.exit()
    accounts = help_param['account']
    emails = help_param['email']
    passwords = help_param['password']


def is_account_exist(account):
    if account not in accounts:
        return False
    return True


def stuff_mail(theme, text,
               to):  # отправка паролей для входа и проверочных кодов
    message = MIMEMultipart()
    message["Subject"] = theme
    message["From"] = 'shifrovalshchik@list.ru'
    body = text
    message.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
        server.login('shifrovalshchik@list.ru', 'Zxoiet123')
    except Exception as e:
        print(e.args)

    try:
        server.sendmail(message['from'], to, message.as_string())
        server.quit()
        return True, 'ok'
    except Exception as e:
        print(e.args)
        try:
            socket.gethostbyaddr("www.yandex.ru")
        except Exception:
            return False, 'no_internet'
        # print("Пароль не может быть отправлен на указанный адрес." + '\n' + "Введите корректный адрес.")
        return False, 'adress_error'


def expect_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class Autorisation(QMainWindow):
    def __init__(self):
        super().__init__()
        self.way = self.first_step
        self.setWindowIcon(QIcon('icons\icon.png'))
        self.obj()

    def obj(self):
        self.setStyleSheet('background-color: rgb(186, 214, 177);'
                           'border-color: rgb(18, 18, 18);'
                           'color: rgb(255, 255, 255);'
                           'font: bold 10pt "Arial";')
        QMessageBox.information(self, 'Авторизация', 'Пожалуйста, подождите')
        get_dates()
        self.setFixedSize(int(L * 0.2), int(H * 0.15))
        self.setWindowTitle('Авторизация')
        self.lbl = QLabel(self)
        self.lbl.setText('Добро пожаловать!')
        self.lbl.resize(int(0.5 * int(L * 0.2)), int(0.15 * int(H * 0.2)))
        self.lbl.move(int(0.25 * int(L * 0.2)), 0)
        self.lbl.setStyleSheet('background-color: rgb(186, 214, 177);'
                               'border-color: rgb(18, 18, 18);'
                               'color: rgb(255, 255, 255);'
                               'font: bold 14pt "Arial";')
        self.edit_nickname = QLineEdit(self)
        self.edit_nickname.resize(int(0.7 * int(L * 0.2)),
                                  int(0.15 * int(H * 0.2)))
        # self.edit_nickname.setEchoMode(QLineEdit.Password)
        self.edit_nickname.setStyleSheet(
            'background-color: rgb(255, 255, 255);'
            'border-color: rgb(18, 18, 18);'
            'color: rgb(125, 121, 114);'
            'font: bold 12pt "Arial";')
        self.edit_nickname.move(5, int(0.2 * int(H * 0.2)))
        self.lbl2 = QLabel(self)
        self.lbl2.setText('Введите никнейм от Вашего аккаунта')
        self.lbl2.setStyleSheet('background-color: rgb(186, 214, 177);'
                                'border-color: rgb(18, 18, 18);'
                                'color: rgb(255, 255, 255);'
                                'font: bold 8pt "Arial";')
        self.lbl2.resize(int(0.57 * int(L * 0.2)), int(0.15 * int(H * 0.2)))
        self.lbl2.move(5, int(0.35 * int(H * 0.2)))
        self.contin = QPushButton(self)
        self.contin.resize(int(0.25 * int(L * 0.2)), int(0.15 * int(H * 0.2)))
        self.contin.move(int(0.73 * int(L * 0.2)), int(0.2 * int(H * 0.2)))
        self.contin.setText('Продолжить')
        self.contin.setAutoDefault(True)  # click on <Enter>
        self.contin.setStyleSheet('background-color: rgb(125, 121, 114);'
                                  'border-color: rgb(18, 18, 18);'
                                  'color: rgb(228, 230, 246);'
                                  'font: bold 10pt "Arial";')
        self.reg_lbl = QLabel(self)
        self.reg_lbl.setText('Ещё нет аккаунта?')
        self.reg_lbl.setStyleSheet('background-color: rgb(186, 214, 177);'
                                   'border-color: rgb(18, 18, 18);'
                                   'color: rgb(255, 255, 255);'
                                   'font: bold 12pt "Arial";')
        self.reg_lbl.resize(int(0.4 * int(L * 0.2)), int(0.15 * int(H * 0.2)))
        self.reg_lbl.move(5, int(0.55 * int(H * 0.2)))
        self.btn = QLabel(self)
        self.btn.setText('Зарегистрироваться')
        self.btn.setStyleSheet('background-color: rgb(186, 214, 177);'
                               'border-color: rgb(18, 18, 18);'
                               'color: rgb(228, 230, 246);'
                               'font: bold 12pt "Arial";')
        self.btn.resize(int(0.45 * int(L * 0.2)), int(0.15 * int(H * 0.2)))
        self.btn.move(5 + int(0.4 * int(L * 0.2)), int(0.55 * int(H * 0.2)))
        self.contin.clicked.connect(self.action)
        self.btn.installEventFilter(self)
        self.no = QPushButton(self)
        self.no.resize(int(0.25 * int(L * 0.2)), int(0.15 * int(H * 0.2)))
        self.no.move(int(0.73 * int(L * 0.2)), 2 * int(0.2 * int(H * 0.2)))
        self.no.setText('Назад')
        self.no.setStyleSheet('background-color: rgb(125, 121, 114);'
                              'border-color: rgb(18, 18, 18);'
                              'color: rgb(228, 230, 246);'
                              'font: bold 10pt "Arial";')
        self.no.clicked.connect(self.back)
        self.no.hide()

    def action(self):
        if self.contin.text() == 'Войти':
            self.is_password_ok()
        elif self.contin.text() == 'Продолжить':
            self.first_step()

    def eventFilter(self, obj, e):
        if e.type() == 2:
            btn = e.button()
            if btn:
                self.registration()
        return super(QMainWindow, self).eventFilter(obj, e)

    def registration(self, arg=''):
        self.hide()
        self.edit_nickname.setText('')
        self.r = Registration(self, arg)
        self.r.show()

    def first_step(self):
        if self.edit_nickname.text().strip() == '':
            QMessageBox.critical(self, 'Авторизация', 'Введите никнейм.')
            return False
        if not is_account_exist(self.edit_nickname.text().strip()):
            if self.contin.text().lower() == 'продолжить':
                msg = QMessageBox(self)
                msg.setWindowTitle('Авторизация')
                msg.setText(
                    f'Аккаунт с никнеймом {self.edit_nickname.text().strip()} не найден. Создать аккаунт с данным никнеймом?')

                play = msg.addButton(
                    'Да', QMessageBox.AcceptRole)
                change = msg.addButton(
                    'Нет', QMessageBox.AcceptRole)
                msg.setIcon(QMessageBox.Question)
                msg.setDefaultButton(play)
                msg.exec_()
                msg.deleteLater()
                if msg.clickedButton() is play:
                    self.registration(self.edit_nickname.text().strip())
                else:
                    self.edit_nickname.setText('')
            return False
        self.way = self.is_password_ok
        self.acc = self.edit_nickname.text().strip()
        self.second_step()

    def second_step(self):
        self.setFixedSize(int(L * 0.2), int(H * 0.12))
        self.btn.hide()
        self.reg_lbl.hide()
        self.edit_nickname.setText('')
        self.edit_nickname.setEchoMode(QLineEdit.Password)
        self.no.show()
        self.contin.setText('Войти')
        self.contin.setStyleSheet('background-color: rgb(125, 121, 114);'
                                  'border-color: rgb(18, 18, 18);'
                                  'color: rgb(228, 230, 246);'
                                  'font: bold 10pt "Arial";')
        self.lbl2.setText('Введите пароль от Вашего аккаунта')

    def back(self):
        self.way = self.first_step
        self.setFixedSize(int(L * 0.2), int(H * 0.15))
        self.lbl2.setText('Введите никнейм от Вашего аккаунта')
        self.btn.show()
        self.reg_lbl.show()
        self.no.hide()
        self.edit_nickname.setText('')
        self.contin.setText('Продолжить')
        self.edit_nickname.setEchoMode(QLineEdit.Normal)

    def is_password_ok(self):
        # a = accounts.index(self.acc)
        if self.contin.text().lower() == 'войти':
            if self.edit_nickname.text().strip() == passwords[
                accounts.index(self.acc)]:
                self.hide()
                a = download_file(self.acc)
                if not a[0]:
                    if a[1] == 'file_already_exists':
                        if a[1] == 'file_already_exists':
                            try:
                                file = pathlib.Path(f'{self.acc}.sqlite3')
                                file.unlink()
                                a = download_file(self.acc)
                            except Exception:
                                pass
                    if a[1] == 'no_internet':
                        QMessageBox.critical(self,'Авторизация', 'Невозможно получить даные.\n Проветьте подключение к интернету')
                        self.back()
                    self.back()

                self.close()
                return self.edit_nickname.text().strip(), passwords[
                accounts.index(self.acc)]
            else:
                QMessageBox.critical(self, 'Авторизация',
                                     'Введён неверный пароль')
                self.edit_nickname.setText('')
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.way()

    def closeEvent(self, event):
        self.close()


# основное окно регистрации
class Registration(QMainWindow):
    def __init__(self, auth,  *args): # при авторизации, если аккаунт не будет найден, можно спрашивать, нужно ли создать аккаунт с таким именем. Если да - то при регистрации в поле "Никнейм" появися данные из поля ввода никнейма при авторизации
        self.auth = auth
        super().__init__()
        if args:
            self.n_ac = args[0]
        else:
            self.n_ac = ''
        self.obj()

    def obj(self):
        self.flag = True
        self.setFixedSize(int(0.9 * int(L * 0.2)), int(H * 0.28))
        self.setWindowTitle('Регистрация')
        self.setStyleSheet('background-color: rgb(186, 214, 177);'
                           'border-color: rgb(18, 18, 18);'
                           'color: rgb(255, 255, 255);'
                           'font: bold 10pt "Arial";')
        #QMessageBox.information(self, 'Регистрация', 'Пожалуйста, пожождите...')
        self.email_lbl = QLabel(self)
        self.email_lbl.setText('Ваш email:')
        self.email_lbl.setStyleSheet('background-color: rgb(186, 214, 177);'
                                     'border-color: rgb(18, 18, 18);'
                                     'color: rgb(255, 255, 255);'
                                     'font: bold 12pt "Arial";')
        self.email_lbl.resize(int(0.43 * int(L * 0.2)),
                              int(0.15 * int(H * 0.2)))
        self.email_lbl.move(0, 0)
        self.edit_email = QLineEdit(self)
        self.edit_email.textChanged[str].connect(self.ok_email)
        self.edit_email.resize(int(0.7 * int(L * 0.2)),
                               int(0.15 * int(H * 0.2)))
        self.edit_email.setStyleSheet('background-color: rgb(255, 255, 255);'
                                      'border-color: rgb(18, 18, 18);'
                                      'color: rgb(255, 255, 255);'
                                      'font: bold 12pt "Arial";')
        self.edit_email.move(0, int(0.2 * int(H * 0.2)))
        self.nickname_lbl = QLabel(self)
        self.nickname_lbl.setText('Желаемый никнейм:')
        self.nickname_lbl.setStyleSheet('background-color: rgb(186, 214, 177);'
                                        'border-color: rgb(18, 18, 18);'
                                        'color: rgb(255, 255, 255);'
                                        'font: bold 12pt "Arial";')
        self.nickname_lbl.resize(int(0.43 * int(L * 0.2)),
                                 int(0.15 * int(H * 0.2)))
        self.nickname_lbl.move(0, int(0.35 * int(H * 0.2)))
        self.edit_nickname = QLineEdit(self)
        self.edit_nickname.setText(self.n_ac)
        self.edit_nickname.textChanged[str].connect(self.nik_ok)
        self.edit_nickname.resize(int(0.7 * int(L * 0.2)),
                                  int(0.15 * int(H * 0.2)))
        self.edit_nickname.setStyleSheet(
            'background-color: rgb(255, 255, 255);'
            'border-color: rgb(18, 18, 18);'
            'color: rgb(255, 255, 255);'
            'font: bold 12pt "Arial";')
        self.edit_nickname.move(0, int(0.55 * int(H * 0.2)))
        self.nik_ok()
        self.password_lbl = QLabel(self)
        self.password_lbl.setText('Желаемый пароль:')
        self.password_lbl.setStyleSheet('background-color: rgb(186, 214, 177);'
                                        'border-color: rgb(18, 18, 18);'
                                        'color: rgb(255, 255, 255);'
                                        'font: bold 12pt "Arial";')
        self.password_lbl.resize(int(0.43 * int(L * 0.2)),
                                 int(0.15 * int(H * 0.2)))
        self.password_lbl.move(0, int(0.7 * int(H * 0.2)))
        self.edit_password = QLineEdit(self)
        self.edit_password.textChanged[str].connect(self.ok_password)
        self.edit_password.resize(int(0.7 * int(L * 0.2)),
                                  int(0.15 * int(H * 0.2)))
        self.edit_password.setStyleSheet(
            'background-color: rgb(255, 255, 255);'
            'border-color: rgb(18, 18, 18);'
            'color: rgb(255, 255, 255);'
            'font: bold 12pt "Arial";')
        self.edit_password.move(0, int(0.9 * int(H * 0.2)))
        self.g_p = QPushButton(self)
        self.g_p.setText('Сгенерировать' + '\n' + 'пароль')
        self.g_p.setStyleSheet('background-color: rgb(125, 121, 114); color: rgb(228, 230, 246);''font: bold 10pt "Arial";')
        self.g_p.resize(int(0.3 * int(L * 0.2)), int(0.17 * int(H * 0.2)))
        self.g_p.move(0, int(1.14 * int(H * 0.2)))
        self.g_p.clicked.connect(self.generate_password)
        self.cont = QPushButton(self)
        self.cont.setText('Продолжить')
        self.cont.setStyleSheet('background-color: rgb(125, 121, 114); color: rgb(228, 230, 246);''font: bold 10pt "Arial";')
        self.cont.resize(int(0.3 * int(L * 0.2)), int(0.15 * int(H * 0.2)))
        self.cont.move(int(0.4 * int(L * 0.2)), int(1.15 * int(H * 0.2)))
        self.cont.clicked.connect(self.no_clear)
        self.lbl = QLabel(self)
        self.lbl.setText('Помощь')
        self.lbl.setStyleSheet('background-color: rgb(186, 214, 177);'
                               'border-color: rgb(18, 18, 18);'
                               'color: rgb(228, 230, 246);'
                               'font: bold 12pt "Arial";')
        self.lbl.resize(int(0.5 * int(L * 0.2)), int(0.15 * int(H * 0.2)))
        self.lbl.move(int(0.71 * int(L * 0.2)), 0)
        self.lbl.installEventFilter(self)
        ##
        self.bak = QLabel(self)
        self.bak.setText('Назад')
        self.bak.setStyleSheet('background-color: rgb(186, 214, 177);'
                               'border-color: rgb(18, 18, 18);'
                               'color: rgb(228, 230, 246);'
                               'font: bold 12pt "Arial";')
        self.bak.resize(50, int(0.15 * int(H * 0.2)))
        self.bak.move(int(0.71 * int(L * 0.2)) - 70, 0)
        self.bak.installEventFilter(self)
        ##
        self.inputText = QTextBrowser(self)
        self.inputText.move(int(0.92 * int(L * 0.2)), 0)
        self.inputText.setStyleSheet('background-color: rgb(186, 214, 177);'
                                     'border-color: rgb(18, 18, 18);'
                                     'color: rgb(255, 255, 255);'
                                     'font: bold 12pt "Arial";')
        self.inputText.resize(int(L * 0.3), int(H * 0.28))
        self.inputText.setText('''Для регистрации в обновлённой версии "Змейки" Вам нужно
указать свой email, никнейм и пароль.
Введённые данные отбражаются красным цветом, если введённые данные не соответствуют требованиям (см ниже).
Иначе - зелёным цветом.
Требования для email:
    Email должен быть корректен и не использован ранее в системе.
Требования для никнейма:
    Никнейм должен не корече 4х символов и не использован
    ранее в системе.
Требования для пароля:
    Пароль должен быть не короче 8 символов;
    Пароль должен содержать хотя бы одну заглавную букву;
    Пароль должен содержать хотя бы одну цифру.
После того, как все поля будут гореть зелёным цветом,
нажмите на кнопку "Продолжить". Затем введите код, отправленный на указанную почту. Если коды совпадут, то регистрация успешно завершиться. После этого Вы
сможете войти в Ваш аккаунт.
Для того, чтобы скрыть данное окно, нажмите на кнопку "Свернуть".''')
        self.inputText.hide()
        self.inputText.setReadOnly(True)
        self.dol = QLabel(self)
        self.dol.setText('Завершено:')
        self.dol.setStyleSheet('background-color: rgb(186, 214, 177);'
                                     'border-color: rgb(18, 18, 18);'
                                     'color: rgb(255, 255, 255);'
                                     'font: bold 12pt "Arial";')
        self.dol.move(0, 250)
        self.dol.hide()
        self.pbar = QProgressBar(self)
        self.pbar.setStyleSheet('background-color: rgb(186, 214, 177);'
                                'border-color: rgb(18, 18, 18);'
                                'color: rgb(255, 255, 255);'
                                'font: bold 12pt "Arial";')
        self.pbar.resize(155, 20) # int(0.9 * int(L * 0.2)), 20
        self.pbar.move(110, 255)
        self.pbar.hide()


    def ok_email(self):
        if "@" in self.edit_email.text() and self.edit_email.text() not in emails and (
                '.ru' in self.edit_email.text() \
                or '.com' in self.edit_email.text()):
            self.edit_email.setStyleSheet(
                'background-color: rgb(255, 255, 255);'
                'border-color: rgb(18, 18, 18);'
                'color: rgb(0, 255, 0);'
                'font: bold 12pt "Arial";')
            return True
        else:
            self.edit_email.setStyleSheet(
                'background-color: rgb(255, 255, 255);'
                'border-color: rgb(18, 18, 18);'
                'color: rgb(255, 0, 0);'
                'font: bold 12pt "Arial";')
            return False

    def nik_ok(self):
        if len(
                self.edit_nickname.text().strip()) >= 7:
            self.edit_nickname.setText(self.edit_nickname.text().strip()[:7])
        if len(
                self.edit_nickname.text().strip()) >= 4 and self.edit_nickname.text().strip() not in accounts:
            self.edit_nickname.setStyleSheet(
                'background-color: rgb(255, 255, 255);'
                'border-color: rgb(18, 18, 18);'
                'color: rgb(0, 255, 0);'
                'font: bold 12pt "Arial";')
            return True
        else:
            self.edit_nickname.setStyleSheet(
                'background-color: rgb(255, 255, 255);'
                'border-color: rgb(18, 18, 18);'
                'color: rgb(255, 0, 0);'
                'font: bold 12pt "Arial";')
            return False

    def ok_password(self):
        if self.password_level(self.edit_password.text()).lower() == 'ok':
            self.edit_password.setStyleSheet(
                'background-color: rgb(255, 255, 255);'
                'border-color: rgb(18, 18, 18);'
                'color: rgb(0, 255, 0);'
                'font: bold 12pt "Arial";')
            return True

        else:
            self.edit_password.setStyleSheet(
                'background-color: rgb(255, 255, 255);'
                'border-color: rgb(18, 18, 18);'
                'color: rgb(255, 0, 0);'
                'font: bold 12pt "Arial";')
            return False

    def no_clear(self):
        a = (self.edit_email.text().strip() != '')
        b = (self.edit_nickname.text().strip() != '')
        c = (self.edit_password.text().strip() != '')
        if a:
            a = 'a'
        else:
            a = ''
        if b:
            b = 'b'
        else:
            b = ''
        if c:
            c = 'c'
        else:
            c = ''
        vars = {
            '': 'Пожалуйста, введитье свой email, желаемый никнейм и желаемый пароль.',
            'c': 'Пожалуйста, введитье свой email и желаемый никнейм.',
            'a': 'Пожалуйста, введитье желаемый никнейм и желаемый пароль.',
            'b': 'Пожалуйста, введитье свой email и желаемый пароль.',
            'ab': 'Пожалуйста, введитье желаемый пароль.',
            'bc': 'Пожалуйста, введитье свой email.',
            'ca': 'Пожалуйста, введитье желаемый никнейм.'
            }
        if a + b + c != 'abc':
            QMessageBox.critical(self, "Регистрация", vars[a + b + c])
            return False
        res_p = self.password_level(self.edit_password.text())
        res_e = self.ok_email()
        res_n = self.nik_ok()
        res = (res_p.lower() == 'ok') and res_e and res_n
        if res:
            self.send_code()
            return True
        if not res_e:
            QMessageBox.critical(self, 'Регистрация',
                                 'Введённый email некорректен либо уже используется.')
            return False
        if not res_n:
            QMessageBox.critical(self, 'Регистрация',
                                 'Введённый никнейм некорректен либо уже используется.')
            return False
        if not res_p:
            QMessageBox.critical(self, 'Регистрация', f'{res}')
            return False

    def send_code(self):
        first_part = 'На введённый адрес не удалось отправить код подтверждения' + '\n'
        errors = {'no_internet': 'Проверьте подключение к интернету.',
                  'adress_error': 'Проверьте корректность введённых данных.'}
        QMessageBox.information(self, "Регистрация",
                                "На указанный Вами email будет отправлен код потверждения." + '\n' +
                                'Пожалуйста, введите его в появившееся поле ввода.')
        code = str(random.choice(range(1000, 10000)))
        text = f'''Спасибо, что зарегестрировались в обновлённой версии "Змейки" !''' + '\n'
        text += f'Ваш никнейм: {self.edit_nickname.text().strip()}' + '\n'
        text += f'Ваш пароль: {self.edit_password.text()}' + '\n'
        text += f'Код подтверждения регистрации: {code}' + '\n' * 2
        text += 'С уважением, разработчики.'
        res = stuff_mail('Код подтверждения', text, self.edit_email.text())
        if not res[0]:
            QMessageBox.critical(self, "Регистрация",
                                 first_part + errors[res[1]])
            if errors[res[1]] == 'Проверьте корректность введённых данных.':
                self.edit_email.setStyleSheet(
                    'background-color: rgb(255, 255, 255);'
                    'border-color: rgb(18, 18, 18);'
                    'color: rgb(255, 0, 0);'
                    'font: bold 12pt "Arial";')
            return False
        res, ok_pressed = QInputDialog.getText(self, "Регистация",
                                               "Введите проверочный код:")
        while not ok_pressed:
            action, ok_pressed_2 = QInputDialog.getItem(
                self, "Выбор действия",
                "Вы не ввели проверочный код. Что сделать?",
                ("Отправить код повторно", "Прервать регистрацию",
                 "Завершить работу программы"), 1, False)

            while not ok_pressed_2:
                action, ok_pressed_2 = QInputDialog.getItem(
                    self, "Выбор действия",
                    "Вы не ввели проверочный код. Что сделать?",
                    ("Отправить код повторно", "Прервать регистрацию",
                     "Завершить работу программы"), 1, False)
            if action == "Отправить код повторно":
                QMessageBox.information(self, "Регистрация",
                                        "На указанный Вами email будет отправлен код потверждения." + '\n' +
                                        'Пожалуйста, введите его в появившееся поле ввода.')
                code = str(random.choice(range(1000, 10000)))
                text = f'''Спасибо, что зарегестрировались в обновлённой версии "Змейки" !''' + '\n'
                text += f'Ваш никнейм: {self.edit_nickname.text().strip()}' + '\n'
                text += f'Ваш пароль: {self.edit_password.text()}' + '\n'
                text += f'Код подтверждения регистрации: {code}' + '\n' * 2
                text += 'С уважением, разработчики.'
                res = stuff_mail('Код подтверждения', text,
                                 self.edit_email.text())
                if not res[0]:
                    QMessageBox.critical(self, "Регистрация",
                                         first_part + errors[res[1]])
                    return False
                res, ok_pressed = QInputDialog.getText(self, "Регистация",
                                                       "Введите проверочный код:")
            if action == "Прервать регистрацию":
                self.hide()

                return
            if action == "Завершить работу программы":
                sys.exit()
        while res != code:
            action, ok_pressed_2 = QInputDialog.getItem(
                self, "Выбор действия",
                "Введённый код не совпадает с отправленным. Что сделать?",
                ("Отправить код повторно", "Прервать регистрацию",
                 "Завершить работу программы"), 1, False)
            while not ok_pressed_2:
                action, ok_pressed_2 = QInputDialog.getItem(
                    self, "Выбор действия",
                    "Введённый код не совпадает с отправленным. Что сделать?",
                    ("Отправить код повторно", "Прервать регистрацию",
                     "Завершить работу программы"), 1, False)
            if action == "Отправить код повторно":
                QMessageBox.information(self, "Регистрация",
                                        "На указанный Вами email будет отправлен код потверждения." + '\n' +
                                        'Пожалуйста, введите его в появившееся поле ввода.')
                code = str(random.choice(range(1000, 10000)))
                text = f'''Спасибо, что зарегестрировались в обновлённой версии "Змейки" !''' + '\n'
                text += f'Ваш никнейм: {self.edit_nickname.text().strip()}' + '\n'
                text += f'Ваш пароль: {self.edit_password.text()}' + '\n'
                text += f'Код подтверждения регистрации: {code}' + '\n' * 2
                text += 'С уважением, разработчики.'
                res = stuff_mail('Код подтверждения', text,
                                 self.edit_email.text())
                if not res[0]:
                    QMessageBox.critical(self, "Регистрация",
                                         first_part + errors[res[1]])
                    return False
                res, ok_pressed = QInputDialog.getText(self, "Регистация",
                                                       "Введите проверочный код:")
            if action == "Прервать регистрацию":
                self.hide()

                return
            if action == "Завершить работу программы":
                sys.exit()
        try:
            self.setDisabled(True)
            self.g_p.hide()
            self.cont.hide()
            self.pbar.show()
            self.dol.show()
            for i in range(1, 37):
                self.pbar.setValue(i)
                time.sleep(0.15)

            add_new_account(self.edit_nickname.text(),
                                self.edit_password.text(),
                                self.edit_email.text())
            self.pbar.setValue(55)
            for i in range(56, 78):
                self.pbar.setValue(i)
                time.sleep(0.1)
            update()
            self.pbar.setValue(87)
            for i in range(88, 101):
                self.pbar.setValue(i)
                time.sleep(0.1)
            QMessageBox.information(self, "Регистрация",
                                    "Регистрация успешно завершена")
            self.close()
            self.auth.show()
            ## здесь процесс создания аккаунта заканчивается, и можно снова показывать окно авторизации
        except Exception as e:
            pass
            QMessageBox.critical(self, "Регистрация",
                                 "Регистрация не может быть завершена.")
            self.close()
            self.auth.show()
    def closeEvent(self, evnt):
        self.close()

    def help(self):
        self.flag = False
        self.setFixedSize(int(L * 0.483), int(H * 0.28))
        self.inputText.show()
        self.lbl.setText('Свернуть')

    def back(self):
        self.close()
        self.auth.show()


    def back_help(self):
        self.lbl.setText('Помощь')
        self.setFixedSize(int(0.9 * int(L * 0.2)), int(H * 0.28))

        self.flag = True

    def eventFilter(self, obj, e):
        if e.type() == 2:
            btn = e.button()
            if btn:
                if obj is self.bak:
                    self.back()
                    return True
                if self.flag:
                    self.help()
                else:
                    self.back_help()
        return super(QMainWindow, self).eventFilter(obj, e)

    def password_level(self, password):
        if len(password) < 8:
            return "Пароль короче 8 символов."
        letters, numbers, up = False, False, False
        for i in password:
            if i.lower() == i and i.isalpha():
                letters = True
            if ord(i) in range(48, 58):
                numbers = True
            if i.upper() == i and ord(i) not in range(48, 58):
                up = True
        if letters and numbers and up:
            return 'Ok'
        elif letters and numbers and not up:
            return "Добавьте в пароль заглавных букв."
        elif letters and up and not numbers:
            return "Добавьтев пароль цифр."
        elif numbers and up and not letters:
            return "Добавьте в пароль строчных букв."
        elif numbers and not letters and not up:
            return "Добавьтев пароль  букв разных регистров."
        elif letters and not numbers and not up:
            return "Добавьте в пароль цифр и заглавных букв."
        else:
            return "Добавьте в пароль прописных букв и цифр."

    def generate_password(self):
        lenth = sample(range(8, 12), 1)[0]
        numbers = [['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']]
        total_list = [list(string.ascii_lowercase)] + [
            list(string.ascii_uppercase)] + numbers
        count = 0
        final_list = []
        work_min = [0, 1, 2]
        work_max = [0, 1, 2]
        for i in range(lenth):
            count += 1
            if count <= 3:
                group_of_symbols = sample(work_min, 1)[0]
                work_min.remove(group_of_symbols)
                final_list.append(sample(total_list[group_of_symbols], 1)[0])
            else:
                group_of_symbols = sample(work_max, 1)[0]
                final_list.append(sample(total_list[group_of_symbols], 1)[0])
        random.shuffle(final_list)
        final_list.reverse()
        self.passwor = final_list
        self.edit_password.setText(''.join(self.passwor))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.no_clear()

def main_auth():
    try:
        sys.excepthook = expect_hook
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        app.setWindowIcon(QIcon(r'icons\icon.png'))
        work_class = Autorisation()
        work_class.setWindowIcon(QIcon(r'icons\icon.png'))
        work_class.show()
        if app.exec_():
            pass
        return work_class.acc
    except Exception as e:
        return 'None'