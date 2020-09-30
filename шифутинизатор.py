from struct import calcsize
import ctypes
from time import sleep 
from urllib.request import urlopen
from os import getcwd, remove, getlogin, listdir, close
from requests import get
from pygame import mixer 
from tkinter import Tk, Frame, Button
from shutil import copyfile


def search_copy(working_dir):
    """ ищет и копирует файл прошлого рабочего стола """
    USER = getlogin()
    PATH = "C:\\Users\\{}\\AppData\\Roaming\\Microsoft\\Windows\\Themes\\CachedFiles".format(USER)

    files = listdir(path=PATH)
    for file in files:
        if file.startswith('CachedImage') and file.endswith('.jpg'):
            path = file

    new_file_dir = working_dir + "\\old_pic.jpg"
    path_to_pic =  PATH + '\\' + path
    copyfile(path_to_pic,new_file_dir)
    return new_file_dir
    

def remover(song_name,pic_path, old_pic_path):
    """ удаляет оставшиеся файлы """ 
    remove(song_name)
    remove(pic_path)

def play_music(song_name):
    """ Нужно для включения музыки, не вызывать в ручную! ( вызыкается функцией window_2_septemb() )"""
    mixer.init()
    mixer.music.load(song_name)
    mixer.music.set_volume(0.3)
    mixer.music.play()
    sleep(0) # задержка перед выводом на экран


def window_2_septemb(song_name,pic_path):
    """ выводит окно со вторым сентября """
    def dest():
        nonlocal root, song_name, pic_path
        root.destroy()
        #remover(song_name,pic_path)

    root = Tk()
    root.geometry("400x400")
    root.config(bg = 'orange')
    root.title('3 Сентября')
    app = Frame(root)
    bt1 = Button(root,text = 'Вернуться во 2 сентября?', command = dest, font = 'Broadway')
    bt1.grid(padx = 90, pady = 160)
    play_music(song_name)
    root.mainloop()


def taking_music_from_internet(work_dir):
    req = get('https://muzter.net/music/0-0-1-6252-20', stream = True) # получаем запрос 
    #sream = True нужен для того, чтобы скачивать неограниченный объем файла
    filename = work_dir + 'shufutin.mp3'

    if req.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(req.content) # Для того, чтобы получить содержимое запроса в байтах,
    return filename

# фон

def taking_pic_from_internet(work_dir):
    url = "https://img.gazeta.ru/files3/875/11942875/00-pic905-895x505-58123.jpg"
    filename = work_dir + 'shufutin.jpg'
    image = urlopen(url).read()
    
    with open(filename, 'wb') as file_pic:
        file_pic.write(image)
    return filename

def is_64bit_windows():
    """Check if 64 bit Windows OS"""
    return calcsize('P') * 8 == 64

def changeBG(path):
    """Change background depending on bit size"""
    if is_64bit_windows():
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 3)
    else:
        ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, path, 3)

SPI_SETDESKWALLPAPER = 20

# главная часть 
working_dir = getcwd() # получаем имя директории

# загружаем музыку 
song_name = taking_music_from_internet(working_dir)

# загружаем картинку 
pic_path = taking_pic_from_internet(working_dir)

# ищем и копируем файл с изначальным фоном, возращает путь к скопированному файлу
new_file_dir_pic = search_copy(working_dir)

# меняем фон
changeBG(pic_path)

# выводим окно и включаем музыку
window_2_septemb(song_name,pic_path)

# меняем фон на изначальный
changeBG(new_file_dir_pic) 

# подчищаем оснтавшиеся файлы
# remover(song_name,pic_path, new_file_dir_pic)