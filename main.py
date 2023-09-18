import os
import random

import requests
import telebot
from bs4 import BeautifulSoup as b
from telebot import types
from dotenv import load_dotenv

# cтраница сайта, которую будет парсить
url = "https://anekdoty.ru/pro-programmistov/"


# parser() делает парсинг страницы и возвращает список анекдотов
def parser(url):
    r = requests.get(url)
    soup = b(r.text, "html.parser")
    anekdots = soup.find_all("div", class_="holder-body")
    return [c.text for c in anekdots]


# сохраняем списоок анекдотов в переменной list_of_jokes
list_of_jokes = parser(url)
# прописывам путь к папкк с мемами
path_dir = "C:\\Users\\Fujitsu\\OneDrive\\Desktop\\Мемы"
# получаем список мемов в папке
image_files = os.listdir(path_dir)
# получаем токен в BotFather

load_dotenv()
# Создаем бот
bot = telebot.TeleBot(os.getenv("TOKEN"))


# создаем клавиатуру (кнопки) и преветственное сообщение
@bot.message_handler(commands=["start"])
def start(m):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(text="Анекдот")
    markup.add(item1)
    item2 = types.KeyboardButton(text="Мем")
    markup.add(item2)
    bot.send_message(m.from_user.id,
                     "Привет! Я бот хорошего настроения :)\nНажми: \nАнекдот - для получения анекдота\nМем - для получения мема",
                     reply_markup=markup)


# обрабатываем ответ от пользователя
@bot.message_handler(content_types=["text"])
def handle_text(message):
    # обрабатываем запрос на анекдот
    if message.text.strip() == "Анекдот":
        answer = random.choice(list_of_jokes)
        bot.send_message(message.from_user.id, answer)
        list_of_jokes.remove(answer)
    elif message.text.strip() == "Мем":
        global image_files
        if len(image_files) == 0:
            image_files = os.listdir(path_dir)
        random_image = random.choice(image_files)
        full_path = os.path.join(path_dir, random_image)
        with open(full_path, "rb") as f:
            bot.send_photo(message.from_user.id, f)
            image_files.remove(random_image)
    elif message.text.strip() != "Анекдот" or message.text.strip() != "Mem":
        start(message)


bot.polling(none_stop=True, interval=0)
