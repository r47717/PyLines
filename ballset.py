from algo import *
from params import *
from random import randint, choice
from ball import Ball
from tkinter import Canvas
from tkinter.messagebox import showinfo

colors = ['red', 'green', 'blue', 'yellow']


class BallSet:
    def __init__(self):
        self.data = []
        self.selected_ball = None

    def __str__(self):
        s = ""
        for ball in self.data:
            s += "(%d, %d)\n" % ball.coords()
        return s

    def find(self, i, j):
        for ball in self.data:
            if ball.coords() == (i, j):
                return ball
        return None

    def add_ball(self, ball):
        """
        Adds new ball to the BallSet unless a ball with such coords already exists
        Also checks the coords are correct
        :param ball: ball to be added
        :return: None
        """
        assert CELLS > ball.coords()[0] >= 0
        assert CELLS > ball.coords()[1] >= 0
        for item in self.data:
            if item.coords() == ball.coords():
                return
        self.data.append(ball)

    def new_random_ball(self, canvas=None):
        while True:
            i1 = randint(0, CELLS - 1)
            j1 = randint(0, CELLS - 1)
            if not self.find(i1, j1):
                break
        new_ball = Ball(i1, j1, choice(colors))
        self.data.append(new_ball)
        if canvas:
            new_ball.draw(canvas)

    def draw_all_balls(self, canvas):
        for ball in self.data:
            ball.draw(canvas)

    def clean(self, canvas):
        for item in self.data:
            item.delete(canvas)
        self.data = []

    def select_ball(self, i, j, canvas):
        ball = self.find(i, j)
        if not ball: # empty space click - do nothing
            return
        if ball == self.selected_ball: # clicked on selected ball - unselect
            self.selected_ball.select(canvas, False)
            self.selected_ball = None
            return
        # clicked on new ball - select new
        if self.selected_ball:
            self.selected_ball.select(canvas, False)
        self.selected_ball = ball
        ball.select(canvas)

    def get_selected_ball(self):
        return self.selected_ball

    def find_balls_by_color(self, color):
        """
        Returns list of balls with specified color
        :param color:
        :return:
        """
        balls = []
        for ball in self.data:
            if ball.get_color() == color:
                balls.append(ball)
        return balls

    def ball_sets_by_color(self):
        """
        Returns list of balls sets by color
        :return: list of lists of balls by color
        """
        color_list = []
        for color in colors:
            color_list.append(self.find_balls_by_color(color))
        return color_list

    def collapse_lines(self, canvas: Canvas):
        """
        Checks for 3+ long lines and collapses it (removes corresponding balls)
        :return: True if any lines were collapsed, False otherwise
        """
        dirty = False
        while True:
            color_sets = self.ball_sets_by_color()
            longest = []
            longest_len = 0
            for set in color_sets:
                longest_seq = find_longest(set)
                if len(longest_seq) > longest_len:
                    longest = longest_seq[:]
                    longest_len = len(longest_seq)
            if longest_len >= 3:
                reduce_seq(self.data, longest, canvas)
                dirty = True
            else:
                break
        return dirty

    def move_ball(self, new_i, new_j, canvas):
        """
        Tries to move the selected ball to the new cell
        :param new_i: new cell coords
        :param new_j: new cell coords
        :param canvas: canvas to draw the ball
        :return: True if the move happened, False otherwise
        """
        ball = self.find(new_i, new_j)
        if ball:
            self.select_ball(new_i, new_j, canvas) # TODO: check this out
            return False
        if self.move_route_exists(*self.selected_ball.coords(), i2=new_i, j2=new_j):
            self.selected_ball.move(new_i, new_j, canvas)
            self.selected_ball.select(canvas, False)
            self.selected_ball = None
            return True
        else:
            return False

    def get_neighbors(self, cell):
        """
        Returns list of all valid and free neighbor cells
        :param cell: cell to find neighbors for
        :return: list of cells (tuple i, j) that are neighbords for 'cell' and not occupied
        """
        i, j = cell
        n = []
        if i > 0:         n.append((i-1, j))
        if j > 0:         n.append((i,   j-1))
        if j < CELLS - 1: n.append((i,   j+1))
        if i < CELLS - 1: n.append((i+1, j))
        for item in self.data:
            if item.coords() in n:
                n.remove(item.coords())
        return n

    def move_route_exists(self, i1, j1, i2, j2):
        """
        Returns true if there is a way for a ball from i1,j1 to i2,j2 (no diag moves)
        :param i1: coords of point 1
        :param j1: coords of point 1
        :param i2: coords of point 2
        :param j2: coords of point 2
        :return: True if the route exists, otherwise False
        """
        reachable = [(i1, j1)]
        front =  [(i1, j1)]
        while True:
            if (i2, j2) in reachable:
                return True
            new_front = []
            new_exist = False
            for item in front:
                neighbors = self.get_neighbors(item)
                for n in neighbors:
                    if n not in reachable:
                        new_front.append(n)
                        new_exist = True
            if not new_exist:
                break
            front = new_front[:]
            reachable.extend(front)
        return False

# ------ Testing -------

if __name__ == "__main__":
    pass

# balls = BallSet()
# balls.new_random_ball()
# balls.new_random_ball()
# balls.new_random_ball()
# balls.new_random_ball()
# balls.new_random_ball()
# balls.new_random_ball()
# balls.new_random_ball()
# balls.new_random_ball()
# balls.new_random_ball()
# balls.new_random_ball()
# balls.new_random_ball()
# balls.new_random_ball()
# balls.new_random_ball()
# balls.new_random_ball()
# balls.new_random_ball()
# balls.new_random_ball()
# balls.new_random_ball()
# balls.new_random_ball()
# balls.new_random_ball()
# balls.new_random_ball()
# balls.new_random_ball()
# balls.new_random_ball()
# balls.new_random_ball()
# balls.new_random_ball()
# balls.new_random_ball()
# balls.new_random_ball()
# balls.new_random_ball()
# balls.new_random_ball()
# balls.new_random_ball()
# balls.new_random_ball()

#balls.add_ball(Ball(6,0))
#balls.add_ball(Ball(3,3))
#balls.add_ball(Ball(4,2))
#balls.add_ball(Ball(2,4))
#balls.add_ball(Ball(5,1))
#balls.add_ball(Ball(1,5))
#balls.add_ball(Ball(0,6))

#balls.add_ball(Ball(6,5))
#balls.add_ball(Ball(6,6))
#balls.add_ball(Ball(6,7))
#balls.add_ball(Ball(6,8))
#balls.add_ball(Ball(6,9))

#balls.add_ball(Ball(8,8))
#balls.add_ball(Ball(7,8))
#balls.add_ball(Ball(6,8))
#balls.add_ball(Ball(5,8))
#balls.add_ball(Ball(4,8))
#balls.add_ball(Ball(3,8))
#balls.add_ball(Ball(2,8))


# print("balls: \n", balls)
#
# longest = BallSet.find_longest(balls.data)
# print("longest:")
# for i in longest:
#     print(i)
#
# balls.collapse_lines()
#
# longest = BallSet.find_longest(balls.data)
# print("longest 2:")
# for i in longest:
#     print(i)


#for n in range(1, 4*CELLS - 1):
#    seq = BallSet.d_longest(n, balls.data)
#    if seq:
#        print("diag #", n)
#        for i in seq:
#            print(i)
#        break

#lst = balls.d_longest(1, balls.data)
#print("longest diag sequence: ")
#for item in lst:
#    print(item)

#diag = 6
#print("diag:")
#print(BallSet.diag_coords(diag))

#print("filter: \n")
#filter = BallSet.d_filter(diag, balls.data)

#for item in filter:
#    print(item)