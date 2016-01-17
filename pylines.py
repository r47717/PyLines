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


# ---------------------------------------------- Canvas ---------------------------------------------------------------#

class LinesCanvas(Canvas):
    def __init__(self, parent, balls):
        Canvas.__init__(self, parent, width=FIELD_SIZE, height=FIELD_SIZE, bd=4, relief=RIDGE)
        parent.set_canvas(self)
        self.draw_grid()
        self.pack()
        self.balls = balls
        self.bind("<Button-1>", self.on_mouse_down)
        self.delay = 0.7
        self.increment = 3
        self.initial_balls()

    def draw_grid(self):
        for n in range(1, CELLS):
            x0 = BORDER + DD * n
            y0 = BORDER
            x1 = x0
            y1 = y0 + DD * CELLS
            self.create_line(x0, y0, x1, y1, width=1, fill="#CCCCCC")
            self.create_line(y0, x0, y1, x1, width=1, fill="#CCCCCC")

    def on_mouse_down(self, event):
        if self.master.status != Status.on:
            return
        i = event.x // DD
        j = event.y // DD
        selected_ball = self.balls.get_selected_ball()
        if not selected_ball:
            self.balls.select_ball(i, j, self)
            return
        if self.balls.move_ball(i, j, self):
            self.update()
            sleep(0.05)
            lines = self.balls.collapse_lines(self)
            sleep(0.05)
            if lines:
                self.master.add_to_score(lines)
            self.new_balls()

    def initial_balls(self):
        for i in range(self.increment):
            self.balls.new_random_ball(self)
            self.update()
            sleep(self.delay)

    def new_balls(self):
        for i in range(self.increment):
            sleep(self.delay)
            if self.balls.get_size() == CELLS*CELLS:
                self.master.game_over()
                return
            self.balls.new_random_ball(canvas)
            self.update()
        lines = self.balls.collapse_lines(canvas)
        if lines:
            self.master.add_to_score(lines)

    def restart(self):
        self.balls.clean(self)
        self.initial_balls()


# ----------------------------------------------- Frame ---------------------------------------------------------------#


class LinesFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.score = 0
        self.status = Status.on
        self.score_label = Label(self, text="Score: 0")
        self.score_label.pack()
        self.make_menu()

    def set_canvas(self, canvas):
        self.canvas = canvas

    def make_menu(self):
        menubar = Menu(self.master)
        file_menu = Menu(menubar, tearoff=False)
        file_menu.add_command(label="Restart", command=self.on_menu_restart)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_menu_exit)
        menubar.add_cascade(label="File", menu=file_menu)
        help_menu = Menu(menubar, tearoff=False)
        help_menu.add_command(label="About...", command=self.on_menu_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.master.config(menu=menubar)

    def update_score(self, num):
        s = "Score: %d" % (num)
        self.score_label.config(text=s)

    def add_to_score(self, num):
        self.score += num
        self.update_score(self.score)

    def game_over(self):
        status = Status.over
        s = "Game Over, Final Score: %d" % (self.score)
        self.score_label.config(text=s)

    def on_menu_restart(self):
        self.status = Status.on
        self.score = 0
        self.update_score(0)
        canvas.restart()

    def on_menu_exit(self):
        self.master.quit()

    def on_menu_about(self):
        showinfo(title="About", message="PyLines (c) by r47717")

# ------------------------------------------------ Create GUI ---------------------------------------------------------#

root = Tk()
root.title("PyLines")
root.wm_resizable(False, False)

frame = LinesFrame(root)
frame.pack()

canvas = LinesCanvas(frame, BallSet())
root.mainloop()
