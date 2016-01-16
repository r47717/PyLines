from params import *
from tkinter import Canvas


class Ball:
    def __init__(self, i, j, color='green'):
        self.i = i
        self.j = j
        self.color = color
        self.selected = False
        self.id = None

    def __str__(self):
        return "Ball: (%d, %d)" % self.coords()

    def select(self, canvas: Canvas, status=True):
        self.selected = status
        border = 'black' if self.selected else self.color
        canvas.itemconfig(self.id, outline=border)

    def is_selected(self):
        return self.selected

    def delete(self, canvas: Canvas):
        canvas.delete(self.id)

    def draw(self, canvas: Canvas):
        border = 'black' if self.selected else self.color
        x = self.i * DD
        y = self.j * DD
        pad = 2
        if not self.id:
            self.id = canvas.create_oval(x + pad, y + pad, x + DD - pad, y + DD - pad, fill=self.color, outline=border)

    def move(self, i, j, canvas: Canvas):
        diff_x = (i - self.i) * DD
        diff_y = (j - self.j) * DD
        self.i = i
        self.j = j
        canvas.move(self.id, diff_x, diff_y)

    def coords(self):
        return self.i, self.j

    def get_color(self):
        return self.color
