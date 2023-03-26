# Importing tkinter and tkinter.ttk
from optparse import Option
import tkinter as tk
from tracemalloc import start
import pandas as pd
import pygame
import datetime
import time
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

# IOT
try:
    print("Execute on Raspi")
    from gpiozero import LED
    switchRelay = LED(18)
except:
    print("not execute on Raspi")

pygame.init()

settingTable = pd.read_csv('setting.csv', delimiter=',')


def insertSound(playList, music_path):

    # Adding Songs path in our playlist.
    playList.append(music_path)

SONG_END = pygame.USEREVENT + 1

def start_playList(playList):
    print(f"All List {playList}")
    # Loading first audio file into our player
    pygame.mixer.music.load(playList[0])
      
    # Removing the loaded song from our playlist list
    playList.pop(0)
    print(f"All List {playList}")
  
    # Playing our music
    pygame.mixer.music.play()
  
    # setting up an end event which host an event
    # after the end of every song
    pygame.mixer.music.set_endevent(SONG_END)
  
    # Playing the songs in the background
    running = True
    while running:
        
        #print(SONG_END)
        
        # checking if any event has been
        # hosted at time of playing
        for event in pygame.event.get():
            #print(event.type)
            
            # A event will be hosted
            # after the end of every song
            if event.type == SONG_END:
                print('Song Finished')
                  
                # Checking our playList
                # that if any song exist or
                # it is empty
                if len(playList) > 0:
                    print(len(playList))
                    # if song available then load it in player
                    # and remove from the player
                    pygame.mixer.music.load(playList[0])
                    playList.pop(0)
                    
                    # Playing our music
                    pygame.mixer.music.play()
  
            # Checking whether the 
            # player is still playing any song
            # if yes it will return true and false otherwise
            if not pygame.mixer.music.get_busy():
                print("Playlist completed")
                try:
                    print("Execute on Raspi")
                    switchRelay.off()
                except:
                    print("not Execute on Raspi")
                
                  
                # When the playlist has
                # completed playing successfully
                # we'll go out of the
                # while-loop by using break
                running = False
                break


def clock():
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    second = time.strftime("%S")

    clock_label.config(text = hour + ":" + minute + ":" + second)
    clock_label.after(1000, clock)
    for j in range(12):
        if (settingTable.enbTime[j] == 1):
            # formatHour
            if (len(str(settingTable.hourAlarm[j])) == 1):
                settingHour = "0" + str(settingTable.hourAlarm[j])
            else:
                settingHour = str(settingTable.hourAlarm[j])

            # formatMinute
            if (len(str(settingTable.minAlarm[j])) == 1):
                settingMinute = "0" + str(settingTable.minAlarm[j])
            else:
                settingMinute = str(settingTable.minAlarm[j])

            if (settingHour == hour) and (settingMinute == minute) and ("00" == second):
                playList = []

                firstAlarm = "Sounds/ติ๊งหน่องหน้า.mp3"
                startSound = "Sounds/ขณะนี้เวลา.mp3"
                hourSound = "Sounds/HOUR.mp3"
                hourUnit = "Sounds/นาฬิกา.mp3"
                minuteSound = "Sounds/MINUTE.mp3"
                minuteUnit = "Sounds/นาที.mp3"
                lastAlarm = "Sounds/ติ๊งหน่องหลัง.mp3"

                hourSound = hourSound.replace("HOUR", str(settingTable.hourAlarm[j]))
                minuteSound = minuteSound.replace("MINUTE", str(settingTable.minAlarm[j]))
                
                try:
                    insertSound(playList, firstAlarm)
                    print("Insert firstAlarm Complate")
                except:
                    print("no path firstAlarm")
                
                try:
                    insertSound(playList, startSound)
                    print("Insert startSound Complate")
                except:
                    print("no path startSound")
                
                try:
                    insertSound(playList, hourSound)
                    print("Insert hourSound Complate")
                except:
                    print("no path hourSound")
                    
                try:
                    insertSound(playList, hourUnit)
                    print("Insert hourUnit Complate")
                except:
                    print("no path hourUnit")
                    
                try:
                    insertSound(playList, minuteSound)
                    print("Insert minuteSound Complate")
                except:
                    print("no path minuteSound")
                    
                if (str(settingTable.minAlarm[j] != "0")):
                    try:
                        insertSound(playList, minuteUnit)
                        print("Insert minuteUnit Complate")
                    except:
                        print("no path minuteUnit")

                insertSound(playList, settingTable.pathSound[j])
                insertSound(playList, lastAlarm)
                
                try:
                    print("Execute on Raspi")
                    switchRelay.on()
                    time.sleep(5)
                except:
                    print("not Execute on Raspi")
                    
                start_playList(playList)
            

def updatetTime():
    clock_label.config(text = "New Text")

def updateSetting():
    filepath = 'setting.csv'
    settingTable.to_csv(filepath, index=False)

# Button callback
def buttonSoundChg(iSound):
    soundNameCSV.set(
        filedialog.askopenfilename(
            initialdir = "/Users/",
            filetypes = (("Mp3 Files", "*.mp3"),)
        )
    )
    settingTable.loc[iSound,'pathSound'] = soundNameCSV.get()
    updateSetting()

def optionHourChg(iHour, cHour):

    settingTable.loc[iHour,'hourAlarm'] = cHour
    updateSetting()

def optionMinChg(iMin, cMin):

    settingTable.loc[iMin,'minAlarm'] = cMin
    updateSetting()
    

# Create the window
root = tk.Tk()
root.title('School Alarm by nix93')

# Place the window in the center of the screen
windowWidth = 800
windowHeight = 530
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
xCordinate = int((screenWidth/2) - (windowWidth/2))
yCordinate = int((screenHeight/2) - (windowHeight/2))
root.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, xCordinate, yCordinate))

### Here are the three lines by which we set the theme ###
# Create a style
style = ttk.Style(root)

# Import the tcl file
root.tk.call('source', settingTable.theme[0]+'.tcl')

# Set the theme with the theme_use method
style.theme_use(settingTable.theme[0])

# Creating lists for the Comboboxes
hourList = ['', '00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
minList = ['', '00', '05', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55']

# Create control variables
soundNameCSV = tk.StringVar()
setTime = []
enbList = settingTable.enbTime
for i in range(len(enbList)):
    #print(i) 
    if enbList[i] == 1:
        setTime.append(tk.BooleanVar(value = True))
    else:
        setTime.append(tk.BooleanVar(value = False))

b = tk.BooleanVar(value = True)
c = tk.BooleanVar()
d = tk.IntVar(value=2)

dHour = []
hList = settingTable.hourAlarm
for i in range(len(hList)):
    #print(i) 
    if len(str(hList[i])) == 1:
        # print('0' + str(hList[i]))
        dHour.append(tk.StringVar(value = ('0' + str(hList[i]))))
    else:
        # print(str(hList[i]))
        dHour.append(tk.StringVar(value = str(hList[i])))

dMin = []
mList = settingTable.minAlarm
for i in range(len(mList)):
    #print(i) 
    if len(str(mList[i])) == 1:
        # print('0' + str(mList[i]))
        dMin.append(tk.StringVar(value = ('0' + str(mList[i]))))
    else:
        # print(str(mList[i]))
        dMin.append(tk.StringVar(value = str(mList[i])))

f = tk.BooleanVar()
g = tk.DoubleVar(value=75.0)
h = tk.BooleanVar()


# Create a Frame for the Checkbuttons
alarmframe = ttk.LabelFrame(root, text='กำหนดเวลาออด (Alarm Schedule)', width = 380, height = 510)
alarmframe.place(x = 20, y = 12)

# Create a Frame for the Clock
clockframe = ttk.LabelFrame(root, text='เวลาปัจจุบัน (Now)', width = 360, height = 140)
clockframe.place(x = 420, y = 12)

clock_label = ttk.Label(clockframe, text="", font=('', 50))
clock_label.place(x = 20, y  = 12)

clock()

# set Alarm Schedule
ttk.Label(alarmframe, text = 'ช่วงที่ใช้งาน', font=('', 10)).place(x = 20, y = 10)
ttk.Label(alarmframe, text = 'ชั่วโมง', font=('', 10)).place(x = 120, y = 10)
ttk.Label(alarmframe, text = 'นาที', font=('', 10)).place(x = 180, y = 10)
ttk.Label(alarmframe, text = 'เลือกเสียง', font=('', 10)).place(x = 250, y = 10)

optionHour = []
optionMin = []

buttonSound = []

#01
optionHour.append(ttk.OptionMenu(alarmframe, dHour[0], *hourList, command=lambda h: optionHourChg(0, h)))
optionMin.append(ttk.OptionMenu(alarmframe, dMin[0], *minList, command=lambda m: optionMinChg(0, m)))
if setTime[0].get():
    buttonSound.append(ttk.Button(alarmframe, text = 'เลือกเสียง', style='AccentButton', command = lambda : buttonSoundChg(0)))
else:
    buttonSound.append(ttk.Button(alarmframe, text = 'เลือกเสียง', state='disabled'))

#02
optionHour.append(ttk.OptionMenu(alarmframe, dHour[1], *hourList, command=lambda h: optionHourChg(1, h)))
optionMin.append(ttk.OptionMenu(alarmframe, dMin[1], *minList, command=lambda m: optionMinChg(1, m)))
if setTime[1].get():
    buttonSound.append(ttk.Button(alarmframe, text = 'เลือกเสียง', style='AccentButton', command = lambda :  buttonSoundChg(1)))
else:
    buttonSound.append(ttk.Button(alarmframe, text = 'เลือกเสียง', state='disabled'))

#03
optionHour.append(ttk.OptionMenu(alarmframe, dHour[2], *hourList, command=lambda h: optionHourChg(2, h)))
optionMin.append(ttk.OptionMenu(alarmframe, dMin[2], *minList, command=lambda m: optionMinChg(2, m)))
if setTime[2].get():
    buttonSound.append(ttk.Button(alarmframe, text = 'เลือกเสียง', style='AccentButton', command = lambda :  buttonSoundChg(2)))
else:
    buttonSound.append(ttk.Button(alarmframe, text = 'เลือกเสียง', state='disabled'))

#04
optionHour.append(ttk.OptionMenu(alarmframe, dHour[3], *hourList, command=lambda h: optionHourChg(3, h)))
optionMin.append(ttk.OptionMenu(alarmframe, dMin[3], *minList, command=lambda m: optionMinChg(3, m)))
if setTime[3].get():
    buttonSound.append(ttk.Button(alarmframe, text = 'เลือกเสียง', style='AccentButton', command = lambda :  buttonSoundChg(3)))
else:
    buttonSound.append(ttk.Button(alarmframe, text = 'เลือกเสียง', state='disabled'))

#05
optionHour.append(ttk.OptionMenu(alarmframe, dHour[4], *hourList, command=lambda h: optionHourChg(4, h)))
optionMin.append(ttk.OptionMenu(alarmframe, dMin[4], *minList, command=lambda m: optionMinChg(4, m)))
if setTime[4].get():
    buttonSound.append(ttk.Button(alarmframe, text = 'เลือกเสียง', style='AccentButton', command = lambda :  buttonSoundChg(4)))
else:
    buttonSound.append(ttk.Button(alarmframe, text = 'เลือกเสียง', state='disabled'))

#06
optionHour.append(ttk.OptionMenu(alarmframe, dHour[5], *hourList, command=lambda h: optionHourChg(5, h)))
optionMin.append(ttk.OptionMenu(alarmframe, dMin[5], *minList, command=lambda m: optionMinChg(5, m)))
if setTime[5].get():
    buttonSound.append(ttk.Button(alarmframe, text = 'เลือกเสียง', style='AccentButton', command = lambda :  buttonSoundChg(5)))
else:
    buttonSound.append(ttk.Button(alarmframe, text = 'เลือกเสียง', state='disabled'))

#07
optionHour.append(ttk.OptionMenu(alarmframe, dHour[6], *hourList, command=lambda h: optionHourChg(6, h)))
optionMin.append(ttk.OptionMenu(alarmframe, dMin[6], *minList, command=lambda m: optionMinChg(6, m)))
if setTime[6].get():
    buttonSound.append(ttk.Button(alarmframe, text = 'เลือกเสียง', style='AccentButton', command = lambda :  buttonSoundChg(6)))
else:
    buttonSound.append(ttk.Button(alarmframe, text = 'เลือกเสียง', state='disabled'))

#08
optionHour.append(ttk.OptionMenu(alarmframe, dHour[7], *hourList, command=lambda h: optionHourChg(7, h)))
optionMin.append(ttk.OptionMenu(alarmframe, dMin[7], *minList, command=lambda m: optionMinChg(7, m)))
if setTime[7].get():
    buttonSound.append(ttk.Button(alarmframe, text = 'เลือกเสียง', style='AccentButton', command = lambda :  buttonSoundChg(7)))
else:
    buttonSound.append(ttk.Button(alarmframe, text = 'เลือกเสียง', state='disabled'))

#09
optionHour.append(ttk.OptionMenu(alarmframe, dHour[8], *hourList, command=lambda h: optionHourChg(8, h)))
optionMin.append(ttk.OptionMenu(alarmframe, dMin[8], *minList, command=lambda m: optionMinChg(8, m)))
if setTime[8].get():
    buttonSound.append(ttk.Button(alarmframe, text = 'เลือกเสียง', style='AccentButton', command = lambda :  buttonSoundChg(8)))
else:
    buttonSound.append(ttk.Button(alarmframe, text = 'เลือกเสียง', state='disabled'))

#10
optionHour.append(ttk.OptionMenu(alarmframe, dHour[9], *hourList, command=lambda h: optionHourChg(9, h)))
optionMin.append(ttk.OptionMenu(alarmframe, dMin[9], *minList, command=lambda m: optionMinChg(9, m)))
if setTime[9].get():
    buttonSound.append(ttk.Button(alarmframe, text = 'เลือกเสียง', style='AccentButton', command = lambda :  buttonSoundChg(9)))
else:
    buttonSound.append(ttk.Button(alarmframe, text = 'เลือกเสียง', state='disabled'))
'''
#011
optionHour.append(ttk.OptionMenu(alarmframe, dHour[10], *hourList, command=lambda h: optionHourChg(10, h)))
optionMin.append(ttk.OptionMenu(alarmframe, dMin[10], *minList, command=lambda m: optionMinChg(10, m)))
if setTime[10].get():
    buttonSound.append(ttk.Button(alarmframe, text = 'เลือกเสียง', style='AccentButton', command = lambda :  buttonSoundChg(10)))
else:
    buttonSound.append(ttk.Button(alarmframe, text = 'เลือกเสียง', state='disabled'))

#012
optionHour.append(ttk.OptionMenu(alarmframe, dHour[11], *hourList, command=lambda h: optionHourChg(11, h)))
optionMin.append(ttk.OptionMenu(alarmframe, dMin[11], *minList, command=lambda m: optionMinChg(11, m)))
if setTime[11].get():
    buttonSound.append(ttk.Button(alarmframe, text = 'เลือกเสียง', style='AccentButton', command = lambda :  buttonSoundChg(11)))
else:
    buttonSound.append(ttk.Button(alarmframe, text = 'เลือกเสียง', state='disabled'))
'''

for t in range(10):
    if t+1 < 10:
        schedule = '0' + str(t+1)
    else:
        schedule = str(t+1)

    ttk.Checkbutton(alarmframe, text = f'ช่วงที่ {schedule}', variable = setTime[t]).place(x = 20, y = 50 + 45*t)

    # SetTime
    optionHour[t].place(x = 120, y = 45*(t+1))

    ttk.Label(alarmframe, text = ':').place(x = 174, y = 50 + 45*t)

    optionMin[t].place(x = 180, y = 45*(t+1))

    # Button
    buttonSound[t].place(x = 250, y = 45*(t+1))

# And of course the mainloop
root.mainloop()