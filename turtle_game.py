from time import time

from numpy import left_shift, right_shift
import server_module.unit_client as unitClient
import pyautogui
import turtle
import time
import random
from turtle import Screen
import win32api

unit_client = unitClient.UnitClient(1, "192.168.1.38")
unit_client.connectToServer()

# Creating the screen object
screen = Screen()

# Setting the screen color-mode
screen.colormode(255)

screenTk = screen.getcanvas().winfo_toplevel()
screenTk.attributes("-fullscreen", True)

prev_pos = None
prev_main_new_pos = None
who = None
color_of_tk = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
dict_of_pens = {}

screen_width, screen_height = 1920, 1080

state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
state_right = win32api.GetKeyState(0x02)  # Right button down = 0 or 1. Button up = -127 or -128

send_data_flag = True
pos = []

t_my = turtle.Turtle()
t_my.pencolor(color_of_tk)
t_my.width(4)
t_my.speed('fastest')
t_my.pencolor(color_of_tk)

data_stream = []

dict_of_data_stream = {}

def draw(x, y):
    if state_left < 0:
        t_my.goto(x, y)
    else:
        t_my.penup()
        t_my.goto(x , y)
        t_my.pendown()

start_time = int(time.time() * 1000)

while True:
    a = win32api.GetKeyState(0x01)
    b = win32api.GetKeyState(0x02)

    if a != state_left:  # Button state changed
        state_left = a
        print(a)
        if a < 0:
            print('Left Button Pressed')
        else:
            print('Left Button Released')

    if b != state_right:  # Button state changed
        state_right = b
        if b < 0:
            t_my.clear()
            print('Right Button Pressed')
        else:
            print('Right Button Released')


    who_data = unit_client.getStateOfData().get('cnt')
    if not who:
        if who_data:
            who = who_data + 1
        else:
            who = 1
        unit_client.sendDataToServer({'cnt': who})

    new_pos = list(pyautogui.position())
    if prev_pos:
        pos = [pos[0] + new_pos[0] - prev_pos[0], pos[1] - new_pos[1] + prev_pos[1]]
    else:
        pos = [new_pos[0] - screen_width//2, screen_height//2 - new_pos[1]]
    prev_pos = new_pos

    if prev_main_new_pos != pos:
        data_stream.append(pos + [state_left, state_right])
        draw(pos[0], pos[1])
    prev_main_new_pos = pos

    data_dict = unit_client.getStateOfData()
    for key, val in data_dict.items():
        if key != 'cnt' and int(key) != who:
            if key not in dict_of_pens:
                t = turtle.Turtle()
                t.pencolor(val['color'])
                t.width(4)
                t.speed('fastest')
                t.pencolor(val['color'])
                dict_of_pens[key] = t
            else:
                pass
            
            if key not in dict_of_data_stream:
                dict_of_data_stream[key] = []
            
            if val['pos'] != dict_of_data_stream[key]:
                print("Draw")
                pen = dict_of_pens[key]
                for i in val['pos']:
                    if i[2] < 0:
                        pen.goto(i[0] , i[1])
                    else:
                        pen.penup()
                        pen.goto(i[0] , i[1])
                        pen.pendown()
                    
                    if i[3] < 0:
                        pen.clear()

            dict_of_data_stream[key] = val['pos']


    if int(time.time() * 1000) - start_time >= 1000:
        if data_stream != []:
            new_data_stream = []
            for i in data_stream:
                new_data_stream.append(i.copy())
            data_stream = []
            start_time = int(time.time() * 1000)
            unit_client.sendDataToServer({who: {'pos': new_data_stream, 'color': color_of_tk}})
    

    time.sleep(0.001)
                
            