from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
import re

root = Tk()
root.title("Simple player")
root.geometry("600x400")
root.iconbitmap('icon/image1.ico')

# Инициализация миксера
pygame.mixer.init()

# Статус паузы
global paused
paused = False


# Получение информации о длине песни
def play_time():

    if stopped:
        return

    current_time = pygame.mixer.music.get_pos() / 1000

    converted_time = time.strftime('%M:%S', time.gmtime(current_time))

    song = song_list.get(ACTIVE)
    song = f'audio/{song}'
    # Далее мы "загрузим" песню в Mutagen
    song_mut = MP3(song)
    # Получение длины песни с помощью Mutagen
    global song_length
    song_length = song_mut.info.length
    converted_length = time.strftime('%M:%S', time.gmtime(song_length))

    if my_slider.get() >= song_length:
        status_bar.config(text=f'{converted_length} of {converted_length}')

    elif paused:
        pass

    elif 0 < current_time - my_slider.get() < 0.08:
        status_bar.config(text=f'{converted_time} of {converted_length}')
        my_slider.config(to=song_length, value=current_time)

    else:
        my_slider.config(to=song_length, value=my_slider.get())
        converted_time = time.strftime('%M:%S', time.gmtime(my_slider.get()))
        status_bar.config(text=f'{converted_time} of {converted_length}')

        my_slider.config(value=my_slider.get()+0.05)

    # Обновление времени на баре
    if current_time <= (song_length - 0.06):
        status_bar.after(50, lambda: play_time())  # Вызов функции через одну секунду после пердыдущей


# Функция добавления песни
def add_song():
    song = filedialog.askopenfilename(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"),
                                                                                             ("flac Files", "*.flac")))

    # Удаление информации о формате файла и его директории
    # song = song.replace("C:/Users/Andrew/Desktop/creations/pyplayer/audio/", "")
    song = re.search(r'audio/.*$', song)
    song = song.group(0)
    song = re.sub(r'audio/', '', song)
    print(song)
    #  song = song.replace(".mp3", "")
    #  song = song.replace(".flac", "")

    # добавление песни в список
    song_list.insert(END, song)


# Функция добавления множества песен
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='audio/', title="Choose Songs",
                                        filetypes=(("mp3 Files", "*.mp3"), ("flac Files", "*.flac")))
    for song in songs:
        # song = song.replace("C:/Users/Andrew/Desktop/creations/pyplayer/audio/", "")
        song = re.search(r'audio/.*$', song)
        song = song.group(0)
        song = re.sub(r'audio/', '', song)
        song_list.insert(END, song)


global played
played = False

# Воспроизвести выбранную песню
def play():
    global stopped
    global paused
    global played

    song = song_list.get(ACTIVE)
    song = f'audio/{song}'  # + '.mp3'
    print(song)

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    paused = False
    stopped = False

    # Удаление активного выделения в сонг листе
    song_list.selection_clear(0, END)
    # Подстрочное выделение новой песни в сонг листе
    song_list.activate(ACTIVE)
    # Выделение ячейки с песней цветом
    song_list.select_set(ACTIVE, last=None)

    # Вызов функции определения времени песни
    if not played:
        play_time()
    else:
        status_bar.config(text='')
        my_slider.config(value=0)

    played = True


global stopped
stopped = False

# Прекратить воспроизведение
def stop():
    # Ресет статуса
    status_bar.config(text='')
    my_slider.config(value=0)

    # Стоп
    pygame.mixer.music.stop()

    # Очистка плейлиста
    song_list.selection_clear(ACTIVE)

    global stopped
    global played
    stopped = True
    played = False



# Приостановка воспроизвдения
def pause(is_paused):
    global paused
    global played
    paused = is_paused
    played = False

    if paused:
        pygame.mixer.music.unpause()
        paused = False

    else:
        pygame.mixer.music.pause()
        paused = True


# Воспроизведение следующей песни
def next_song():
    global paused  # Статус паузы
    # Получение индекса текущей песни в плейлисте
    next_one = song_list.curselection()  # return type is list
    # Увеличение индекса песни
    next_one = next_one[0] + 1
    # Получение названия песни
    song = song_list.get(next_one)
    # Изменение строки с песней для возможности вопроизведения
    song = f'audio/{song}'
    # Load & play
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    # Изменение статуса паузы
    paused = False

    my_slider.config(value=0)

    # Удаление активного выделения в сонг листе
    song_list.selection_clear(0, END)
    # Подстрочное выделение новой песни в сонг листе
    song_list.activate(next_one)
    # Выделение ячейки с песней цветом
    song_list.select_set(next_one, last=None)


# Воспроизведение предыдущей песни
def previous_song():
    global paused  # Статус паузы
    # Получение индекса текущей песни в плейлисте
    next_one = song_list.curselection()  # return type is list
    # Уменьщение индекса песни
    next_one = next_one[0] - 1
    # Получение названия песни
    song = song_list.get(next_one)
    # Изменение строки с песней для возможности вопроизведения
    song = f'audio/{song}'
    print(song)
    # Load & play
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    # Изменение статуса паузы
    paused = False

    my_slider.config(value=0)

    # Удаление активного выделения в сонг листе
    song_list.selection_clear(0, END)
    # Подстрочное выделение новой песни в сонг листе
    song_list.activate(next_one)
    # Выделение ячейки с песней цветом
    song_list.select_set(next_one, last=None)


# Удаление одной песни из плейлиста
def remove_song():
    stop()
    song_list.delete(ANCHOR)
    pygame.mixer.music.stop()


# Удаление всех песен из плейлиста
def remove_all_songs():
    stop()
    song_list.delete(0, END)
    pygame.mixer.music.stop()


# Функция слайдера
def slide(x):
    song = song_list.get(ACTIVE)
    song = f'audio/{song}'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=my_slider.get())


# Функция изменения громкости
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())
    current_volume = pygame.mixer.music.get_volume()
#   volume_slider.config(value=current_volume)


# Создадим плейлист
master_frame = Frame(root)
master_frame.pack(pady=20)

song_list = Listbox(master_frame, bg='white', fg='black', width=60, selectbackground="gray", selectforeground="black")
song_list.grid(row=0, column=0)

# Опишем кнопки play, pause...
back_btn_image = PhotoImage(file='images/back_250.png')
forward_btn_image = PhotoImage(file='images/forward_250.png')
play_btn_image = PhotoImage(file='images/play_250.png')
pause_btn_image = PhotoImage(file='images/pause_250.png')
stop_btn_image = PhotoImage(file='images/stop_250.png')

# Создадим фрейм для кнопок
controls_frame = Frame(master_frame)
controls_frame.grid(row=1, column=0, pady=10)

# Создадим фрейм для слайдера громкости
volume_frame = LabelFrame(master_frame, text='volume')
volume_frame.grid(row=0, column=1)

# Создадим кнопки контроля для плеера
back_button = Button(controls_frame, image=back_btn_image, borderwidth=0, command=previous_song)
forward_button = Button(controls_frame, image=forward_btn_image, borderwidth=0, command=next_song)
play_button = Button(controls_frame, image=play_btn_image, borderwidth=0, command=play)
pause_button = Button(controls_frame, image=pause_btn_image, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(controls_frame, image=stop_btn_image, borderwidth=0, command=stop)

back_button.grid(row=0, column=0, padx=12)
forward_button.grid(row=0, column=1, padx=12)
play_button.grid(row=0, column=2, padx=12)
pause_button.grid(row=0, column=3, padx=12)
stop_button.grid(row=0, column=4, padx=12)

# Создадим меню
my_menu = Menu(root)
root.config(menu=my_menu)

# Добавим меню добавления песен
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add songs", menu=add_song_menu)

# Добавим команду добавления одной песни
add_song_menu.add_command(label="Add One Song To Playlist", command=add_song)

# Добавим команду добавления нескольких песен
add_song_menu.add_command(label="Add Many Songs To Playlist", command=add_many_songs)

# Добваим меню удаления песен
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Remove A Song From Playlist", command=remove_song)
remove_song_menu.add_command(label="Remove All Songs From Playlist", command=remove_all_songs)

# Создадим status bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# Слайдер для времени
my_slider = ttk.Scale(master_frame, from_=0, to=1000, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.grid(pady=20, row=2, column=0)


# Слайдер для громкости
volume_slider = ttk.Scale(volume_frame, from_=1, to=0, orient=VERTICAL, value=0.5, command=volume, length=145)
volume_slider.pack()

root.mainloop()
