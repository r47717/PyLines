#!/usr/bin/env python3

from params import *
from ballset import BallSet
import threading as th
from tkinter import *
from time import sleep
from tkinter.messagebox import showinfo
from enum import Enum


class Status(Enum):
    on = 1       # game in progress
    over = 3     # game over, can restart
    quit = 4     # game is being quit, restart impossible


# ---------------------------------------------- Events ---------------------------------------------------------------#

def on_mouse_down(event, arg):
    global mouseEnabled, doIncrementEvent, score, status
    if not mouseEnabled:
        return
    if status != Status.on:
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
        lines = balls.collapse_lines(canvas)
        if lines:
            score += lines
            update_score(score)
        doIncrementEvent.set()
    mouseEnabled = True


def on_menu_restart():
    global status, balls, canvas, score, mouseEnabled, doIncrementEvent
    balls.clean(canvas)
    status = Status.on
    score = 0
    update_score(0)
    mouseEnabled = False
    doIncrementEvent.set()


def on_menu_exit():
    global root, status, doIncrementEvent
    status = Status.quit
    doIncrementEvent.set()
    root.quit()


def on_menu_about():
    showinfo(title="About", message="PyLines (c) by r47717")


# ----------------------------------------------- Balls thread --------------------------------------------------------#

def balls_thread_func(canvas, balls):
    global mouseEnabled, status, doIncrementEvent, score
    delay = 0.7
    initial_num = 3
    increment_num = 3
    for i in range(1, initial_num + 1):
        balls.new_random_ball(canvas)
        sleep(delay)
    mouseEnabled = True
    while status != Status.quit:
        doIncrementEvent.wait()
        if status == Status.quit:
            return
        mouseEnabled = False
        for i in range(1, increment_num + 1):
            sleep(delay)
            if balls.get_size() == CELLS*CELLS:
                game_over(score)
                continue
            balls.new_random_ball(canvas)
        lines = balls.collapse_lines(canvas)
        if lines:
            score += lines
            update_score(score)
        doIncrementEvent.clear()
        mouseEnabled = True


# ---------------------------------------------- Canvas drawings ------------------------------------------------------#

def draw_grid(canvas):
    for n in range(1, CELLS):
        x0 = BORDER + DD * n
        y0 = BORDER
        x1 = x0
        y1 = y0 + DD * CELLS
        canvas.create_line(x0, y0, x1, y1, width=1, fill="#CCCCCC")
        canvas.create_line(y0, x0, y1, x1, width=1, fill="#CCCCCC")
        pass

# ---------------------------------------------- Game control ---------------------------------------------------------#


def update_score(num):
    global score_label
    s = "Score: %d" % (num)
    score_label.config(text=s)


def game_over(num):
    global score_label, status, doIncrementEvent
    doIncrementEvent.clear()
    status = Status.over
    s = "Game Over, Final Score: %d" % (num)
    score_label.config(text=s)


balls = BallSet()

status = Status.on

score = 0

mouseEnabled = False # TODO: replace with a mutex
doIncrementEvent = th.Event()
doIncrementEvent.clear()

# ------------------------------------------------ Create GUI ---------------------------------------------------------#

root = Tk()
root.title("PyLines")
root.wm_resizable(False, False)

menubar = Menu(root)
file_menu = Menu(menubar, tearoff=False)
file_menu.add_command(label="Restart", command=on_menu_restart)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=on_menu_exit)
menubar.add_cascade(label="File", menu=file_menu)
help_menu = Menu(menubar, tearoff=False)
help_menu.add_command(label="About...", command=on_menu_about)
menubar.add_cascade(label="Help", menu=help_menu)
root.config(menu=menubar)

canvas = Canvas(root, width=FIELD_SIZE, height=FIELD_SIZE, bd=4, relief=RIDGE)
draw_grid(canvas)
canvas.bind("<Button-1>", lambda event, arg=(canvas, balls): on_mouse_down(event, arg))
canvas.pack()

score_label = Label(root, text="Score: 0")
score_label.pack()

ballsThread = th.Thread(target=balls_thread_func, args=(canvas, balls))
ballsThread.start()

root.mainloop()

status = Status.quit
doIncrementEvent.set()
ballsThread.join()