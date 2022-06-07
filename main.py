import requests
import json
import os
from tqdm import tqdm
import time
URL = "https://cloud-api.yandex.net/v1/disk/resources"
user_id = input("Введите ID пользователя вк:")
yandex_token = input("Введите Yandex Disk Token:")
token = input("Введите VK Token:")
url = "https://api.vk.com/method/photos.get"
headers = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": f'OAuth {yandex_token}'}

#Первая функция для внесения параметров запроса
def get_params(vk_token):
    params = {
        "owner_id" : user_id,
        "access_token" : vk_token,
        "album_id" : "profile",
        "extended" : "1",
        "photo_sizes" : "1",
        "v" : "5.131"
    }
    res = requests.get(url, params=params)
    return res

#Тут просто извлекаем из json количество лайков
def get_likes(vk_token):
    for photos in get_params(token).json()["response"]["items"]:
        file_likes = photos["likes"]["count"]   #кол-во лайков для названия файла

#А тут извлекаем из json дату публикации(на случай повторения количества лайков у двух фотографий)
    return file_likes
def get_date(token):
    for likes in get_params(token).json()["response"]["items"]:
        date_for_file = likes["date"]
    return date_for_file

# Получаем размер аватарки
def get_size(token):
    for sizes in get_params(token).json()["response"]["items"]:
        for size in sizes["sizes"]:
            for type_of_size in size["type"]:
                pass
    return type_of_size

#Получаем URL фотографии
def get_url(token):
    for sizes in get_params(token).json()["response"]["items"]:
        for size in sizes["sizes"]:
            for type_of_size in size["type"]:
                if type_of_size == "z":
                    url2 = size["url"]
                    break
                else:
                    pass
    return url2

#Создаем словарь для преобразования его в json
def create_dict():
    name_of_file = str(get_likes(token)) + "_" + str(get_date(token)) + ".jpg"
    new_dict = [{"file_name" : name_of_file, "size" : get_size(token)}]
    return new_dict

#Создаем json файл
def create_json():
    with open("new_json.txt", "w") as f:
        json.dumps(create_dict())

create_json()

#JSON файл данного типо требуется на вывод по заданию
def write_and_read(dict, filename):
    dict = json.dumps(dict)
    dict = json.loads(str(dict))
    with open(filename, "w", encoding= "utf-8") as file:
        json.dump(create_dict(), file, indent=3)
    with open(filename, "r", encoding= "utf-8") as file2:
        print(f'\n{file2.read()}')

#Производим сохранение фотографии
def save_photo():
    p = requests.get(get_url(token))
    with open(f'{create_dict()[0]["file_name"]}', "wb") as f:
        f.write(p.content)

#Cоздаем Папку
def create_folder(path):
    """Создание папки. \n path: Путь к создаваемой папке."""
    requests.put(f'{URL}?path={path}', headers=headers)

create_folder("Doc")

def upload_file(loadfile, savefile, replace=True):
    """Загрузка файла.
    savefile - Путь к файлу на Диске
    loadfile - Путь к загружаемому файлу
    replace - true or false Замена файла на Диске"""
    res = requests.get(f'{URL}/upload?path={savefile}&overwrite={replace}&', headers=headers).json()
    with open(loadfile, 'rb') as f:
        try:
            requests.put(res['href'], files={'file':f})
        except KeyError:
            print(res)

def check():
    for type_of_error in get_params(token).json():
        if type_of_error == "error":
            print("ОШИБКА\nСкорее всего профиль данного пользователя не доступен")
            break
        else:
            file = create_dict()[0]["file_name"]
            direct = "/Doc" + "/" + create_dict()[0]["file_name"]
            def the_most_miserable_progress_bar():
                pbar = tqdm(total=100)
                for i in range(1):
                    save_photo()
                    write_and_read(create_dict(), "new_json.txt")
                    time.sleep(0.3)
                    pbar.update(50)
                    upload_file(file, direct)
                    time.sleep(0.3)
                    pbar.update(50)
                pbar.close()
            the_most_miserable_progress_bar()
check()