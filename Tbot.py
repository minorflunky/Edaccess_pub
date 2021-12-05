import os
from gspread.exceptions import GSpreadException
import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import multiprocessing as mp
import timeit
from requests.exceptions import ConnectionError
import socket

try:
    API_KEY = os.getenv("API_KEY")
    bot = telebot.TeleBot("<INSERT YOUR BOT API KEY HERE>")

    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "creds.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("2021-2022 Schedule").sheet1
    print('init done')
except:
    print('API connection failure! check internet connection')
    exit()


def begin():
    @bot.message_handler(commands=['start'])
    def start(message):
        id = message.chat.id
        IdFile = open('ID.txt', 'r+')
        Flag = 0

        for line in IdFile:
            if str(id) in line:
                Flag = 1
                print('matching ID found')
                bot.send_message(message.chat.id, 'Мы с вами уже знакомы.')
                break

        if Flag == 0:
            bot.send_message(
                message.chat.id, 'Здравствуйте, я бот EdAccess, я отправляю нотификации когда расписание меняется. ')
            print(id, ('is not registered, registering'))
            IdFile.write(str(id) + "\n")
            IdFile.close()
    bot.polling()


def alert():
    Idlist = open('/home/pi/EdAccess/ID.txt', 'r')
    for line in Idlist:
        bot.send_message(chat_id=int(line),
                         text="<a href=https://docs.google.com/spreadsheets/d/1zxkwNvSVPfKUZLqcvznRlqNFm6FNUzOCOqvXGjnGDvk/edit?usp=sharing'>Расписание</a> было изменено.",
                         parse_mode='HTML')


def check():
    while True:

        data = sheet.acell('A1').value
        print(data)
        print('fetched')
        time.sleep(1)
        if data == 'send':
            print('send command received')
            alert()
            sheet.update('A1', '')


google = mp.Process(target=check, args=[])
telegram = mp.Process(target=begin, args=[])


try:
    google.start()
    begin()
except:
    print('oops! something went wrong killing script :(')
    google.kill()
    bot.stop_polling()
    exit
# Me 936548134
