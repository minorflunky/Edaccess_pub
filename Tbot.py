import os
import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

API_KEY = os.getenv("API_KEY")
bot = telebot.TeleBot("2068307274:AAGCu-eINzyBvQvjloSQ01W3mz8QGyGPVe8")

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("testing").sheet1
print('init done')

elaps = 0
oldstate = 0


def begin():
    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id, 'hello')

        id = message.chat.id
        IdFile = open('ID.txt', 'r+')
        Flag = 0

        for line in IdFile:
            if str(id) in line:
                Flag = 1
                print('matching ID found')
                break

        if Flag == 0:
            print(id, ('is not registered, registering'))
            IdFile.write(str(id) + "\n")
            IdFile.close()

        while True:
            data = sheet.get_all_records()
            time.sleep(0.5)
            print('fetched')

            if oldstate != data and oldstate != 0:
                print('initial change detected timer start')

            while elaps < 30:
                data = sheet.get_all_records()
                time.sleep(0.985)
                elaps += 1
                print(elaps)

                if oldstate != data:
                    elaps = 0
                    print('change detected timer reset')

                oldstate = data
            elaps = 0
            Idlist = open('ID.txt', 'r')
            for line in Idlist:
                bot.send_message(int(line), 'google doc changed')

            oldstate = data

    bot.polling()


begin()

# Me 936548134
# Alima 919173101
# Mom 1083662268
