#!/usr/bin/env python3
import os
import os.path
import threading
from random import shuffle,seed
from time import sleep
from subprocess import call
from os import urandom

import vlc
import tkinter
import tkinter.messagebox

#get songs that in dir
def GetSongs(directory):
    songs=[]
    #get list of songs
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in [f for f in filenames if f.endswith(".mp3")]:
            songs.append((os.path.join(dirpath, filename)))
    #randomize list and return
    num=0
    for x in range(ord(urandom(1))):
        num+=ord(urandom(1))
    seed(num)
    shuffle(songs)
    return songs


#get a playlist of songs that match given directory
def GetPlaylist(directory=False):
    playlist=[]

    #if directory not set
    if directory==False:
        with open("directory","r") as x:
            directory=x.read()
    #get songs in dir
    playlist=GetSongs(directory)

    #save directory
    with open("directory","w") as x:
        x.write(directory)
    return playlist




#play playlist
def Play(playlist):
    global listPlayer
    #create vlc instance
    Player = vlc.Instance('--loop')

    #create playlist object
    mediaList = Player.media_list_new()
    #add playlist to playlist object
    for music in playlist:
        mediaList.add_media(Player.media_new(music))
    #create player
    listPlayer = Player.media_list_player_new()
    #set playlist
    listPlayer.set_media_list(mediaList)
    #set to loop
    listPlayer.set_playback_mode(vlc.PlaybackMode.loop)
    #play
    listPlayer.play()



#displays screen to interact with player
def Interact():
    global screen

    #creates screen
    screen = tkinter.Tk()
    screen.attributes("-fullscreen", True)

    #declares buttons
    playButton = tkinter.Button(screen, text ="Play", command = PlaySong, font = ("Helvetica", 40, "bold"), background="Cyan", activebackground="Cyan")
    seekButton = tkinter.Button(screen, text ="Seek", command = DoSeek, font = ("Helvetica", 40, "bold"), background="Cyan", activebackground="Cyan")
    prevButton = tkinter.Button(screen, text ="Prev", command = PrevSong, font = ("Helvetica", 40, "bold"), background="Cyan", activebackground="Cyan")
    nextButton = tkinter.Button(screen, text ="Next", command = NextSong, font = ("Helvetica", 40, "bold"), background="Cyan", activebackground="Cyan")

    #creates grid
    screen.rowconfigure(0, weight=2, uniform="equal")
    screen.rowconfigure(1, weight=2, uniform="equal")
    screen.columnconfigure((0,1), weight=1)

    #maps buttons to grid
    playButton.grid(row=0, column=0, columnspan=1, sticky='EWNS')
    seekButton.grid(row=0, column=1, columnspan=1, sticky='EWNS')    
    prevButton.grid(row=1, column=0, columnspan=1, sticky='EWNS')
    nextButton.grid(row=1, column=1, columnspan=1, sticky='EWNS')


    #starts interact screen
    screen.mainloop()


#check if player playing, get playlist, and play
def StartPlayer(directory=False):
    if directory!=False:
        #get playlist
        playlist=GetPlaylist(directory)
        #stop player
        listPlayer.stop()
        listPlayer.release()
    #if not started then get playlist
    else:playlist=GetPlaylist()

    #launch player in seperate thread
    t = threading.Thread(target=Play, args=(playlist,))
    t.setDaemon(True)
    t.start()
    sleep(2)


#toggles player
def PlaySong():
    listPlayer.pause()

#goes back one song
def PrevSong():
    listPlayer.previous()

#goes to next song
def NextSong():
    listPlayer.next()

#opens window that lets you choose folder
def DoSeek():
    global folderPath,folder,screen2

    #destroys controller screen
    screen.destroy()

    #creates new screen
    screen2 = tkinter.Tk()
    screen2.attributes("-fullscreen", True)
    screen2.configure(background='Cyan')

    #declares buttons
    nextButton = tkinter.Button(screen2, text ="Next", command = Cycle, font = ("Helvetica", 40, "bold"), background="Cyan", activebackground="Cyan")
    slctButton = tkinter.Button(screen2, text ="Play", command = Select, font = ("Helvetica", 40, "bold"), background="Cyan", activebackground="Cyan")
    intoButton = tkinter.Button(screen2, text ="Into", command = Into, font = ("Helvetica", 40, "bold"), background="Cyan", activebackground="Cyan")
    backButton = tkinter.Button(screen2, text ="Back", command = Back, font = ("Helvetica", 40, "bold"), background="Cyan", activebackground="Cyan")

    #creates grid
    screen2.rowconfigure(0, weight=1)
    screen2.rowconfigure(1, weight=2, uniform="equal")
    screen2.rowconfigure(2, weight=2, uniform="equal")
    screen2.columnconfigure((0,1), weight=1)

    #creates label
    folder =tkinter.StringVar()
    folderDisplay=tkinter.Label(screen2, textvariable=folder, anchor=tkinter.N, bg="Cyan", fg="Black", font=("Helvetica", 20 ,"bold"), wraplength=500)
    #gets base folders to display on label
    folderPath=["Music"]
    GetDirs()

    #maps widgets to grid
    folderDisplay.grid(row=0, column=0, columnspan=2)
    nextButton.grid(row=1, column=0, columnspan=1, sticky='EWNS')
    slctButton.grid(row=1, column=1, columnspan=1, sticky='EWNS')    
    intoButton.grid(row=2, column=0, columnspan=1, sticky='EWNS')
    backButton.grid(row=2, column=1, columnspan=1, sticky='EWNS')

    #starts search screen
    screen2.mainloop()

#scans directories to get new dirs
def GetDirs():
    global dirList,place,maxPlace
    #turns folderPath list into path string
    path="/".join(folderPath)
    #gets every dir in immediate path dir
    dirList = [ item for item in os.listdir(path) if os.path.isdir(os.path.join(path, item)) ]
    #if no dirs in dir goes back one then scans again and returns
    if len(dirList)==0:
        folderPath.pop()
        GetDirs()
        return
    #resets place in dir and updates amount of dirs
    place=0
    maxPlace=-1
    for x in dirList:
        maxPlace+=1
    #updates label to dir
    folder.set(dirList[place])

#displays next dir in dir or wraps around if at last dir
def Cycle():
    global place
    place+=1
    if place>maxPlace:
        place=0
    folder.set(dirList[place])

#selects dir, calls player to start playing dir, then destroys search screen and creates interact screen
def Select():
    folderPath.append(dirList[place])
    directory="/".join(folderPath)
    StartPlayer(directory)
    screen2.destroy()
    Interact()

#goes into dir then scans
def Into():
    folderPath.append(dirList[place])
    GetDirs()

#goes back one dir then scans
def Back():
    if len(folderPath)>1:
        folderPath.pop()
        GetDirs()
    else:
        screen2.destroy()
        Interact()



#starts player then lets you interact
def Main():
    os.chdir("/home/pi/Blueberry")
    StartPlayer()
    Interact()


if __name__=="__main__":
    try:
        Main()
    except Exception as e:
        print(e)