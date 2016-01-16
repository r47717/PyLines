#!/usr/bin/env python3

from params import *
from ballset import BallSet
import threading as th
from tkinter import *
from time import sleep
from tkinter.messagebox import showinfo


# --- Events ---#

def on_mouse_down(event, arg):
    global mouseEnabled, doIncrementEvent, score
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
        lines = balls.collapse_lines(canvas)
        if lines:
            score += lines
            update_score(score)
        doIncrementEvent.set()
    mouseEnabled = True

# --- Balls thread ---#

def balls_thread_func(canvas, balls):
    global mouseEnabled, gameStopped, doIncrementEvent, score
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
            if balls.get_size() == CELLS*CELLS:
                game_over(score)
                return
            balls.new_random_ball(canvas)
        lines = balls.collapse_lines(canvas)
        if lines:
            score += lines
            update_score(score)
        doIncrementEvent.clear()
        mouseEnabled = True


# --- Canvas drawings ---#

def draw_grid(canvas):
    for n in range(1, CELLS):
        x0 = BORDER + DD * n
        y0 = BORDER
        x1 = x0
        y1 = y0 + DD * CELLS
        canvas.create_line(x0, y0, x1, y1, width=1, fill="#CCCCCC")
        canvas.create_line(y0, x0, y1, x1, width=1, fill="#CCCCCC")
        pass
        #canvas.create_rectangle(i * DD, j * DD, i * DD + DD, j * DD + DD, fill="#EEEEEE", width=1)


def update_score(num):
    global score_label
    s = "Score: %d" % (num)
    score_label.config(text=s)

def game_over(num):
    global score_label
    s = "Game Over, Final Score: %d" % (num)
    score_label.config(text=s)


# --- run GUI ---#

root = Tk()
root.title("PyLines")
root.wm_resizable(False, False)
canvas = Canvas(root, width=FIELD_SIZE, height=FIELD_SIZE, bd=4, relief=RIDGE)
draw_grid(canvas)
balls = BallSet()
canvas.bind("<Button-1>", lambda event, arg=(canvas, balls): on_mouse_down(event, arg))
canvas.pack()

score = 0
score_label = Label(root, text="Score: 0")
score_label.pack()

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