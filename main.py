import telebot
from dotenv import load_dotenv
from telebot import types

from Clases import *

# получаем токен в BotFather
# выделяем токен в отдельный файл
load_dotenv()
# Создаем бот
bot = telebot.TeleBot(os.getenv("TOKEN"))


# создаем клавиатуру (кнопки) и преветственное сообщение
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    TanyaBot.users_mem[user_id] = []
    TanyaBot.users_joke[user_id] = []
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
        try:
            answer = TanyaBot.get_joke()
            if answer in TanyaBot.users_joke[user_id]:
                # если есть, то опять выбираем случайную картнку
                answer = TanyaBot.get_joke()
            # добавляем случйное изображение в список показанных
            TanyaBot.users_joke[user_id].append(answer)
            print(TanyaBot.users_joke[user_id])
            bot.send_message(message.from_user.id, answer)
            print(TanyaBot.users_joke)
        except KeyError:
            print('Key not found')
            bot.send_message(message.from_user.id, "нажми /start")
        # для того, чтобы анекдоты не повторялись, отправленный анекдот удаляем из списка анекдотов

    # обрабатываем запрос на мем
    elif message.text.strip() == "Мем":

        try:
            # получаем случайныую картинку из списка
            random_image = TanyaBot.get_mem()
            # проверяем есть ли случайный анекдот в списке уже показанных
            if random_image in TanyaBot.users_mem[user_id]:
                # если есть, то опять выбираем случайную картнку
                random_image = TanyaBot.get_mem()
            # добавляем случйное изображение в список показанных
            TanyaBot.users_mem[user_id].append(random_image)
            print(TanyaBot.users_mem[user_id])
            # находим путь именно до этой картинки
            full_path = os.path.join(PATH_DIR, random_image)
            # открываем картнку
            with open(full_path, "rb") as f:
                # отправляем её пользователю
                bot.send_photo(message.from_user.id, f)
            print(TanyaBot.users_mem)
        except KeyError:
            print('Key not found')
            bot.send_message(message.from_user.id, "нажми /start")

    elif message.text.strip() != "Анекдот" or message.text.strip() != "Mem":
        bot.send_message(message.from_user.id, "Я тебя не понимаю :(  нажми /start")


bot.polling(none_stop=True, interval=0)
