import os
import random

import requests
import telebot
from bs4 import BeautifulSoup as b
from dotenv import load_dotenv
from telebot import types

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
# выделяем токен в отдельный файл
load_dotenv()
# Создаем бот
bot = telebot.TeleBot(os.getenv("TOKEN"))
# создаем словарь, куда будем добавлять пользователей
users = {}


# создаем клавиатуру (кнопки) и преветственное сообщение
@bot.message_handler(commands=["start"])
def start(message):
    # получаем идентификатор для каждого нового пользователя и сохраняем его в словарь
    user_id = message.from_user.id
    users[user_id] = []
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(text="Анекдот")
    markup.add(item1)
    item2 = types.KeyboardButton(text="Мем")
    markup.add(item2)
    bot.send_message(message.from_user.id,
                     "Привет! Я бот хорошего настроения :)\nНажми: \nАнекдот - "
                     "для получения анекдота\nМем - для получения мема",
                     reply_markup=markup)


# обрабатываем ответ от пользователя
@bot.message_handler(content_types=["text"])
def handle_text(message):
    user_id = message.from_user.id

    # обрабатываем запрос на анекдот
    if message.text.strip() == "Анекдот":

        # проверяем не пуст ли наш список анекдотов, усли пуст - опять получаем его
        # со страницы с анекдотами
        global list_of_jokes
        if len(list_of_jokes) == 0:
            list_of_jokes = parser(url)
        # получаем случайный анекдот из списка
        answer = random.choice(list_of_jokes)
        # отправляем его пользователю
        bot.send_message(message.from_user.id, answer)
        # для того, чтобы анекдоты не повторялись, отправленный анекдот удаляем из списка анекдотов
        list_of_jokes.remove(answer)
    # обрабатываем запрос на мем
    elif message.text.strip() == "Мем":

        try:
            # получаем случайныую картинку из списка
            random_image = random.choice(image_files)
            # проверяем есть ли случайный анекдот в списке уже показанных
            if random_image in users[user_id]:
                # если есть, то опять выбираем случайную картнку
                random_image = random.choice(image_files)
            # добавляем случйное изображение в список показанных
            users[user_id].append(random_image)
            # находим путь именно до этой картинки
            full_path = os.path.join(path_dir, random_image)
            # открываем картнку
            with open(full_path, "rb") as f:
                # отправляем её пользователю
                bot.send_photo(message.from_user.id, f)
        except KeyError:
            print('Key not found')
            bot.send_message(message.from_user.id, "нажми /start")

    elif message.text.strip() != "Анекдот" or message.text.strip() != "Mem":
        bot.send_message(message.from_user.id, "Я тебя не понимаю :(  нажми /start")


bot.polling(none_stop=True, interval=0)
