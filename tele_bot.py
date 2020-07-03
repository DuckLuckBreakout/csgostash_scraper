import telebot
from constants import TELE_TOKEN, MY_ID


class TeleBot:
    def __init__(self):
        self.bot = telebot.TeleBot(TELE_TOKEN)

    def send_new_file_info(self, file):
        self.bot.send_message(MY_ID, file)
