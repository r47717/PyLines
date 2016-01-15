FIELD_SIZE = 500
CELLS = 10
DD = FIELD_SIZE / CELLS


class Ball:
    def __init__(self, i, j, color='green'):
        self.i = i
        self.j = j
        self.color = color
        self.selected = False

    def __str__(self):
        return "Ball: (%d, %d)" % self.coords()

    def select(self, status=True):
        self.selected = status

    def is_selected(self):
        return self.selected

    def draw(self, canvas):
        border = 'black' if self.selected else self.color
        x = self.i * DD
        y = self.j * DD
        pad = 2
        canvas.create_oval(x + pad, y + pad, x + DD - pad, y + DD - pad, fill=self.color, outline=border)

    def move(self, i, j):
        self.i = i
        self.j = j

    def coords(self):
        return self.i, self.j

    def get_color(self):
        return self.color
