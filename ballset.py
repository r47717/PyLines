from random import randint, choice
from ball import Ball
# from tkinter.messagebox import showinfo

FIELD_SIZE = 500
CELLS = 10
DD = FIELD_SIZE / CELLS
colors = ['red', 'green', 'blue', 'yellow']


class BallSet:
    def __init__(self):
        self.data = []
        self.selected_ball = None

    def __str__(self):
        str = ""
        for ball in self.data:
            str += "(%d, %d)\n" % ball.coords()
        return str

    def find(self, i, j):
        for ball in self.data:
            if ball.coords() == (i, j):
                return ball
        return None

    # Adds new ball to the BallSet unless a ball with such coords already exists
    #
    def add_ball(self, ball):
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

    def clean(self):
        self.data = []

    def select_ball(self, i, j, canvas):
        ball = self.find(i, j)
        if not ball: # empty space click - do nothing
            return
        if ball == self.selected_ball: # clicked on selected ball - unselect
            self.selected_ball.select(False)
            self.selected_ball.draw(canvas)
            self.selected_ball = None
            return
        # clicked on new ball - select new
        if self.selected_ball:
            self.selected_ball.select(False)
            self.selected_ball.draw(canvas)
        self.selected_ball = ball
        ball.select()
        ball.draw(canvas)

    def get_selected_ball(self):
        return self.selected_ball

    # returns set of balls with specified color
    #
    def find_balls_by_color(self, color):
        balls = []
        for ball in self.data:
            if ball.get_color() == color:
                balls.append(ball)
        return balls

    # returns list of balls sets by color
    #
    def ball_sets_by_color(self):
        color_list = []
        for color in colors:
            color_list.append(self.find_balls_by_color(color))
        return color_list

    # Checks relational position of two balls, possible return values:
    # 0 - not in seq
    # 1 - ball1 is to upper-left from 0
    # 2 - ball1 is above 0
    # 3 - ball1 is to upper-right from 0
    # 4 - ball1 is to the right from 0
    # 5 - ball1 is to lower-right from 0
    # 6 - ball1 is below 0
    # 7 - ball1 is to lower-left from 0
    # 8 - ball1 is to the left from 0
    @staticmethod
    def rel(ball0, ball1):
        i0, j0 = ball0.coords()
        i1, j1 = ball1.coords()
        di = i0 - i1
        dj = j0 - j1
        if di > 0 and di == dj:
            return 1
        elif di > 0 and dj == 0:
            return 2
        elif di > 0 and dj == -di:
            return 3
        elif di == 0 and dj < 0:
            return 4
        elif dj == di < 0:
            return 5
        elif di < 0 and dj == 0:
            return 6
        elif di < 0 and dj == -di:
            return 7
        elif di == 0 and dj > 0:
            return 8
        else:
            return 0

    # Checks relational position of two balls, possible return values:
    # 0 - not in seq
    # 1 - upper-left to lower-right diagonal
    # 2 - vertical
    # 3 - upper-right to lower-left diagonal
    # 4 - horizontal
    @staticmethod
    def rel2(ball0, ball1):
        rel = BallSet.rel(ball0, ball1)
        if rel == 1 or rel == 5:
            return 1
        elif rel == 2 or rel == 6:
            return 2
        elif rel == 3 or rel == 7:
            return 3
        elif rel == 4 or rel == 8:
            return 4
        else:
            return 0

    # Checks that all balls in 'balls' are aligned, possible return values:
    # 0 - not in seq
    # 1 - upper-left to lower-right diagonal
    # 2 - vertical
    # 3 - upper-right to lower-left diagonal
    # 4 - horizontal
    @staticmethod
    def is_aligned(balls):
        if len(balls) <= 1:
            return 0
        ball0 = balls[0]
        ball1 = balls[1]
        rel = BallSet.rel2(ball0, ball1)
        if rel == 0:
            return 0
        for i in range(2, len(balls)):  # check the boundary!
            if BallSet.rel2(ball1, balls[i]) != rel:
                return 0
        return rel

    # Checks if 'balls' is a sequence - this means all balls are aligned and no gaps
    #
    @staticmethod
    def is_seq(balls):
        rel = BallSet.is_aligned(balls)
        if rel == 0:
            return False
        if rel < 4:
            sorted_balls = sorted(balls, key = lambda ball: ball.coords()[0])
        else:
            sorted_balls = sorted(balls, key = lambda ball: ball.coords()[1])
        length = len(sorted_balls)
        min_i = sorted_balls[0].coords()[0]
        min_j = sorted_balls[0].coords()[1]
        max_i = sorted_balls[length - 1].coords()[0]
        max_j = sorted_balls[length - 1].coords()[1]
        di = abs(max_i - min_i) + 1
        dj = abs(max_j - min_j) + 1
        return (di == 1 and dj == length or
                dj == 1 and di == length or
                di == dj == length)

    # Finds the longest sequence (vertical, diagonal, horizontal) in 'balls'
    # (recursive, works slowly ~n!)
    @staticmethod
    def find_longest_recursive(balls):
        if len(balls) < 3:
            return []
        if BallSet.is_seq(balls):
            return balls
        if len(balls) == 3:
            return []

        original = balls[:]
        max_len = 0
        result = []
        for ball in original:
            shorter = original[:]
            shorter.remove(ball)
            shorter_len = len(shorter)
            shorter_longest = BallSet.find_longest(shorter)
            if len(shorter_longest) == shorter_len:
                return shorter_longest
            if len(shorter_longest) > max_len:
                result = shorter_longest[:]
                max_len = len(shorter_longest)
        return result

    # Returns list of balls on vertical or horizontal 'n'
    @staticmethod
    def vh_filter(n, balls, is_vertical = True):
        res = []
        for ball in balls:
            i, j = ball.coords()
            if is_vertical:
                if i + 1 == n:
                    res.append(ball)
            else:
                if j + 1 == n:
                    res.append(ball)
        return res

    # Returns longest vertical or horizontal sequence
    @staticmethod
    def vh_longest(n, balls, is_vertical = True):
        filtered = BallSet.vh_filter(n, balls, is_vertical)
        if len(filtered) < 3:
            return []
        index = 1 if is_vertical else 0
        filtered = sorted(filtered, key = lambda ball: ball.coords()[index])
        latest = filtered[0]
        seq = [latest]
        longest_seq = []
        longest_len = 0
        for item in filtered[1:]:
            if seq == [] or item.coords()[index] == latest.coords()[index] + 1:
                seq.append(item)
                latest = item
            elif len(seq) > longest_len:
                longest_seq = seq[:]
                longest_len = len(seq)
                latest = item
                seq = [latest]
        if len(seq) > longest_len:
            longest_seq = seq[:]
            longest_len = len(seq)
        return longest_seq if len(longest_seq) >= 3 else []

    # Lists diag coords as tuples for n from 1 to 4*CELLS-2 diag numbers
    #
    @staticmethod
    def diag_coords(n):
        if n <= 2 * CELLS - 1: # up to down diags
            i1 = 0 if n <= CELLS else n - CELLS
            j1 = CELLS - n if n <= CELLS else 0
            i2 = n - 1 if n <= CELLS else CELLS - 1
            j2 = CELLS - 1 if n <= CELLS else (2*CELLS - 1) - n
            result = [(i, j1 + (i - i1)) for i in range(i1, i2 + 1)]
        else:  # down to up diags
            n -= (2 * CELLS - 1)
            i1 = 0 if n <= CELLS else n - CELLS
            j1 = n - 1 if n <= CELLS else CELLS - 1
            i2 = n - 1 if n <= CELLS else CELLS - 1
            j2 = i1 = 0 if n <= CELLS else n - CELLS
            result = [(i, j1 - (i - i1)) for i in range(i1, i2 + 1)]
        return result

    # returns list of balls on diag 'n'
    #
    @staticmethod
    def d_filter(n, balls):
        dc = BallSet.diag_coords(n)
        result = []
        for ball in balls:
            for c in dc:
                if ball.coords() == c:
                    result.append(ball)
        return result

    # Returns the longest seq for diag 'n'
    #
    @staticmethod
    def d_longest(n, balls):
        filtered = BallSet.d_filter(n, balls)
        if len(filtered) < 3:
            return []
        filtered = sorted(filtered, key = lambda ball: ball.coords()[0])
        longest_seq = []
        longest_len = 0
        latest = filtered[0]
        seq = [latest]
        di = 1
        dj = 1 if n <= 2 * CELLS - 1 else -1
        for item in filtered[1:]:
            if (seq == [] or item.coords()[0] == latest.coords()[0] + di and
            item.coords()[1] == latest.coords()[1] + dj):
                seq.append(item)
                latest = item
            elif len(seq) > longest_len:
                longest_seq = seq[:]
                longest_len = len(seq)
                latest = item
                seq = [latest]
        if len(seq) > longest_len:
            longest_seq = seq[:]
            longest_len = len(seq)
        return longest_seq if len(longest_seq) >= 3 else []


    # Finds the longest sequence (vertical, diagonal, horizontal) in 'balls'
    #
    @staticmethod
    def find_longest(balls):
        sequences = []
        for n in range(1, CELLS + 1):
            sequences.append(BallSet.vh_longest(n, balls, True))
        for n in range(1, CELLS + 1):
            sequences.append(BallSet.vh_longest(n, balls, False))
        for n in range(1, 4*CELLS - 1):
            sequences.append(BallSet.d_longest(n, balls))
        longest = []
        longest_len = 0
        for seq in sequences:
            if len(seq) > longest_len:
                longest = seq[:]
                longest_len = len(seq)
        return longest


    # remove balls from seq from 'balls' - todo: can we do it in one function?
    #
    @staticmethod
    def reduce_seq(balls, seq):
        for ball in seq:
            balls.remove(ball)


    # checks for 3+ long lines and collapses (removes balls) if any
    #
    def collapse_lines(self):
        dirty = False
        while True:
            color_sets = self.ball_sets_by_color()
            longest = []
            longest_len = 0
            for set in color_sets:
                longest_seq = self.find_longest(set)
                if len(longest_seq) > longest_len:
                    longest = longest_seq[:]
                    longest_len = len(longest_seq)
            if longest_len >= 3:
                BallSet.reduce_seq(self.data, longest)
                dirty = True
            else:
                break
        return dirty


    def move_ball(self, new_i, new_j, canvas):
        ball = self.find(new_i, new_j)
        if ball:
            self.select_ball(new_i, new_j, canvas)
            return False
        if self.move_route_exists(*self.selected_ball.coords(), i2=new_i, j2=new_j):
            self.selected_ball.move(new_i, new_j)
            self.selected_ball.select(False)
            self.selected_ball.draw(canvas)
            self.selected_ball = None
            return True
        else:
            return False


    # returns list of all valid and free neighbor cells
    #
    def get_neighbors(self, cell):
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

    # Returns true if there is a way for a ball from i1,j1 to i2,j2 (no diag moves)
    #
    def move_route_exists(self, i1, j1, i2, j2):
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