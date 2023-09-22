import random
import requests
from bs4 import BeautifulSoup as b
import os

URL = "https://anekdoty.ru/pro-programmistov/"
PATH_DIR = "C:\\Users\\Fujitsu\\OneDrive\\Desktop\\Мемы"
class TanyaBot:
    users = {}

    def get_anekdots():
        r = requests.get(URL)
        soup = b(r.text, "html.parser")
        anekdots = soup.find_all("div", class_="holder-body")
        return [c.text for c in anekdots]

    # сохраняем списоок анекдотов в переменной list_of_jokes

    # прописывам путь к папкк с мемами
    def get_joke(user_id):
        list_of_jokes = TanyaBot.get_anekdots()
        answer = random.choice(list_of_jokes)
        return answer

    def get_mem(user_id):
        image_files = os.listdir(PATH_DIR)
        random_image = random.choice(image_files)
        return random_image
