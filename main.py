

from tkinter import *
import pygame.mixer
import time
from tkinter import ttk,filedialog
from mutagen.mp3 import MP3
import os

app = Tk()
app.title('ratatatata player')
app.geometry('450x650')
app.resizable(False,False)
pygame.mixer.init()


#функция добавления песни
def add_song():
    song = filedialog.askopenfilename(initialdir="music/",title="Choose",filetypes=(("mp3 Files","*.mp3"),))
    song = song.replace("C:/Users/gonch/MP3player/music/","")
    song = song.replace(".mp3","")
    play_list.insert(END,song)

#добавление нескольких песен
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir="music/", title="Choose", filetypes=(("mp3 Files", "*.mp3"),))
    for song in songs:
        song = song.replace("C:/Users/gonch/MP3player/music/", "")
        song = song.replace(".mp3", "")
        play_list.insert(END, song)

#функция воспроизведения
def play_btn():
    global stopped
    stopped = False
    song = play_list.get(ACTIVE)
    song = f"C:/Users/gonch/MP3player/music/{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    play_time()
    track_label.config(text=song.replace("C:/Users/gonch/MP3player/music/", ""))
    #slider_pos = int(song_length)
    #my_slider.config(to=slider_pos,value=0)

#информация о длительности песни
def play_time():
    if stopped:
        return
    current_time = pygame.mixer.music.get_pos()/1000
    # временная метка для получения данных
    #slider_label.config(text=f"Slider:{int(my_slider.get())} and Song:{int(current_time)}")
    convert_time = time.strftime("%M:%S",time.gmtime(current_time))

    #получение текущей позиции песни
    play_list.curselection()
    song = play_list.get(ACTIVE)
    song = f"C:/Users/gonch/MP3player/music/{song}.mp3"
    song_random = MP3(song)
    global song_length
    song_length = song_random.info.length
    convert_song_lendth = time.strftime("%M:%S", time.gmtime(song_length))
    current_time += 1
    if int(my_slider.get()) == int(song_length):
        pass
    elif paused:
        pass
    elif int(my_slider.get()) == int(current_time):
        #слайдер не двигали
        slider_pos = song_length
        my_slider.config(to=slider_pos, value=int(current_time))
    else:
        #слайдер был перемещён
        slider_pos = song_length
        my_slider.config(to=slider_pos, value=int(my_slider.get()))
        convert_time = time.strftime("%M:%S", time.gmtime(my_slider.get()))
        progress.config(text=f"пройдено  {convert_time} из {convert_song_lendth}")
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)
    progress.config(text=f"time : {convert_time} from {convert_song_lendth}")
    #my_slider.config(value=current_time)
    progress.after(1000, play_time)
#функция остановки
global stopped
stopped = False
def stop_btn():
    pygame.mixer.music.stop()
    play_list.select_clear(ACTIVE)
    progress.config(text="")
    my_slider.config(value=0)
    global stopped
    stopped = True
#функция паузы
global paused
paused = False
def pause_btn(is_paused):
    global paused
    paused = is_paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True

#функция следующая песня
def forward():
    frw = play_list.curselection()
    frw = frw[0]+1
    song = play_list.get(frw)
    song = f"C:/Users/gonch/MP3player/music/{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    track_label.config(text=song.replace("C:/Users/gonch/MP3player/music/", ""))
    my_slider.config(value=0)
    #перемещение полоски состояния
    play_list.selection_clear(0,END)
    play_list.activate(frw)
    play_list.select_set(frw,last=None)

#функция предидущая песня
def previous_btn():
    frw = play_list.curselection()
    frw = frw[0] - 1
    song = play_list.get(frw)
    song = f"C:/Users/gonch/MP3player/music/{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    track_label.config(text=song.replace("C:/Users/gonch/MP3player/music/", ""))
    my_slider.config(value=0)
    # перемещение полоски состояния
    play_list.selection_clear(0, END)
    play_list.activate(frw)
    play_list.select_set(frw, last=None)

#удаление одной песни
def delete_one():
    stop_btn()
    play_list.delete(ANCHOR)
    pygame.mixer.music.stop()

#очистка плейлиста
def clear_all():
    stop_btn()
    play_list.delete(0,END)
    pygame.mixer.music.stop()

#функция слайдера
def slide(x):
    #slider_label.config(text=f"{int(my_slider.get())} of {int(song_length)}")
    song = play_list.get(ACTIVE)
    song = f"C:/Users/gonch/MP3player/music/{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0,start=int(my_slider.get()))

#функция громкости
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())


#фон окна
app.image = PhotoImage(file="fon.png")
bg_logo = Label(app,image=app.image)
bg_logo.grid(row=0,column=0)

#кнопки
play = PhotoImage(file="play.png")
Button(app,image=play,bg="#3887fd",bd=0,command=play_btn).place(x=186,y=473)

stop = PhotoImage(file="stop.png")
Button(app,image=stop,bg="#3887fd",bd=0,command=stop_btn).place(x=196,y=395)

pause = PhotoImage(file="pause.png")
Button(app,image=pause,bg="#3887fd",bd=0,command=lambda: pause_btn(paused)).place(x=196,y=570)

next_btn = PhotoImage(file="next.png")
Button(app,image=next_btn,bg="#3887fd",bd=0,command=forward).place(x=287,y=483)

previous = PhotoImage(file="previous.png")
Button(app,image=previous,bg="#3887fd",bd=0,command=previous_btn).place(x=105,y=483)

#список песен
play_list = Listbox(app,bg="black",fg="red",width=54,height=15,selectbackground="yellow",selectforeground="black")
play_list.place(x=62,y=57)

#меню
my_menu = Menu(app)
app.config(menu=my_menu)
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs",menu=add_song_menu)

#добавление одной песни
add_song_menu.add_command(label="add one song",command=add_song)

#добавление нескольких песен
add_song_menu.add_command(label="add many songs",command=add_many_songs)

#удаление песен
del_song = Menu(my_menu)
my_menu.add_cascade(label="Delete Songs",menu=del_song)
del_song.add_command(label="delete song",command=delete_one)
del_song.add_command(label="clear playlist",command=clear_all)

#создание состояния песни
progress = Label(app,text="",bd=5,relief=GROOVE,anchor=W,bg="#3887fd")
progress.place(x=303,y=5)

#создание слайдера
my_slider = ttk.Scale(app,from_=0,to=100,orient=HORIZONTAL,value=0,length=310,command=slide)
my_slider.place(x=70,y=350)

#слайдер громкости
volume_slider = ttk.Scale(app,from_=0,to=1,orient=VERTICAL,value=1,length=230,command=volume)
volume_slider.place(x=400,y=400)


#временная переменная слайдера
#slider_label = Label(app,text="0",bg="#515352",fg="yellow")
#slider_label.place(x=90,y=10)

#отображение названия песни
track_label = Label(app,text="",font=("arial",12),bg="#515352",fg="yellow")
track_label.place(x=225,y=337,anchor="center")

app.mainloop()