import os
import random

import requests
from bs4 import BeautifulSoup as b

# cтраница сайта, которую будет парсить
URL = "https://anekdoty.ru/pro-programmistov/"
# прописывам путь к папкк с мемами
PATH_DIR = "C:\\Users\\Fujitsu\\OneDrive\\Desktop\\Мемы"


# адрес страницы и путь к папке - константы
class TanyaBot:
    # создаеи словари, куда будем добавлять пользователей
    users_mem = {}
    users_joke = {}

    @staticmethod
    def get_anekdots():
        r = requests.get(URL)
        soup = b(r.text, "html.parser")
        anekdots = soup.find_all("div", class_="holder-body")
        return [c.text for c in anekdots]

    @staticmethod
    def get_joke():
        list_of_jokes = TanyaBot.get_anekdots()
        answer = random.choice(list_of_jokes)
        return answer

    @staticmethod
    def get_mem():
        image_files = os.listdir(PATH_DIR)
        random_image = random.choice(image_files)
        return random_image
