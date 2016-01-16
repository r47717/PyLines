#!/usr/bin/env python3

from params import *
from ballset import BallSet
import threading as th
from tkinter import *
from time import sleep
from tkinter.messagebox import showinfo


# --- Events ---#

def on_mouse_down(event, arg):
    global mouseEnabled, doIncrementEvent
    if not mouseEnabled:
        return
    mouseEnabled = False
    (canvas, balls) = arg
    i = event.x // DD
    j = event.y // DD
    selected_ball = balls.get_selected_ball()
    if not selected_ball:
        balls.select_ball(i, j, canvas)
        mouseEnabled = True
        return
    if balls.move_ball(i, j, canvas):
        balls.collapse_lines(canvas)
        doIncrementEvent.set()
    mouseEnabled = True

# --- Balls thread ---#

def balls_thread_func(canvas, balls):
    global mouseEnabled, gameStopped, doIncrementEvent
    delay = 0.7
    initial_num = 3
    increment_num = 3
    for i in range(1, initial_num + 1):
        balls.new_random_ball(canvas)
        sleep(delay)
    mouseEnabled = True
    while not gameStopped:
        doIncrementEvent.wait()
        if gameStopped:
            return
        mouseEnabled = False
        for i in range(1, increment_num + 1):
            sleep(delay)
            balls.new_random_ball(canvas)
        balls.collapse_lines(canvas)
        doIncrementEvent.clear()
        mouseEnabled = True


# --- Canvas drawings ---#

def draw_grid(canvas):
    for i in range(0, CELLS):
        for j in range(0, CELLS):
            canvas.create_rectangle(i * DD, j * DD, i * DD + DD, j * DD + DD, fill="#EEEEEE", width=1)


# --- run GUI ---#

root = Tk()
root.title("PyLines")
root.wm_resizable(False, False)
canvas = Canvas(root, width=FIELD_SIZE, height=FIELD_SIZE)
draw_grid(canvas)
balls = BallSet()
canvas.bind("<Button-1>", lambda event, arg=(canvas, balls): on_mouse_down(event, arg))
canvas.pack()

mouseEnabled = False # TODO: replace with a mutex
doIncrementEvent = th.Event()
doIncrementEvent.clear()
gameStopped = False
ballsThread = th.Thread(target=balls_thread_func, args=(canvas, balls))
ballsThread.start()

root.mainloop()

gameStopped = True
doIncrementEvent.set()
ballsThread.join()