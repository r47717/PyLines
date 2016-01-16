from params import *
from ballset import BallSet


def relation(ball0, ball1):
    """
    Checks relational position of two balls, possible return values:
    0 - not in seq
    1 - ball1 is to upper-left from 0
    2 - ball1 is above 0
    3 - ball1 is to upper-right from 0
    4 - ball1 is to the right from 0
    5 - ball1 is to lower-right from 0
    6 - ball1 is below 0
    7 - ball1 is to lower-left from 0
    8 - ball1 is to the left from 0
    """
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


def relation2(ball0, ball1):
    """
    Checks relational position of two balls, possible return values:
    0 - not in seq
    1 - upper-left to lower-right diagonal
    2 - vertical
    3 - upper-right to lower-left diagonal
    4 - horizontal
    """
    rel = relation(ball0, ball1)
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


def is_aligned(balls):
    """
    Checks that all balls in 'balls' are aligned, possible return values:
    0 - not in seq
    1 - upper-left to lower-right diagonal
    2 - vertical
    3 - upper-right to lower-left diagonal
    4 - horizontal
    :param balls: list of balls to be ckeched for alignment
    :return: value from 0 to 4 - see above
    """
    if len(balls) <= 1:
        return 0
    ball0 = balls[0]
    ball1 = balls[1]
    rel = relation2(ball0, ball1)
    if rel == 0:
        return 0
    for i in range(2, len(balls)):  # check the boundary!
        if relation2(ball1, balls[i]) != rel:
            return 0
    return rel


def is_seq(balls):
    """
    Checks if 'balls' is a sequence - this means all balls are aligned and no gaps
    :param balls: list of balls to be checked for a sequence
    :return: True if it is a sequence, False otherwise
    """
    rel = is_aligned(balls)
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


def find_longest_recursive(balls):
    """
    Reviews 'balls' list and finds the longest sequence in the list
    Recursive and works pretty slowly (~n!), so not in use now
    :param balls: balls list
    :return: list with the sequence
    """
    if len(balls) < 3:
        return []
    if is_seq(balls):
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
        shorter_longest = find_longest(shorter)
        if len(shorter_longest) == shorter_len:
            return shorter_longest
        if len(shorter_longest) > max_len:
            result = shorter_longest[:]
            max_len = len(shorter_longest)
    return result


def vh_filter(n, balls, is_vertical = True):
    """
    Selects all balls from 'balls' that are on the vertical or horizontal 'n'
    :param n: number of vertical or horizontal (1 < n < CELLS)
    :param balls: list of balls to be examined
    :param is_vertical: if True then verticals else horizontals
    :return: list of balls
    """
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


def vh_longest(n, balls, is_vertical = True):
    """
    Returns longest vertical or horizontal sequence
    :param n: Uses vh_filter to select balls in 'balls' and then finds the longest seq in the set
    :param balls: initial balls list
    :param is_vertical: if True then verticals are used else horizontals
    :return: returns list of balls as the longest sequence or [] if no sequence (a sequence is at least 3 balls)
    """
    filtered = vh_filter(n, balls, is_vertical)
    if len(filtered) < 3:
        return []
    index = 1 if is_vertical else 0   # will filter by i or j coord
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


def diag_coords(n):
    """
    Lists diag coords as tuples for n from 1 to 4*CELLS-2 diag numbers
    :param n: For a diagonal #n it returns list of tuples of coordinates (i, j)
    :return:
    """
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


def d_filter(n, balls):
    """
    returns list of balls on diag 'n'
    :param n:
    :param balls:
    :return:
    """
    dc = diag_coords(n)
    result = []
    for ball in balls:
        for c in dc:
            if ball.coords() == c:
                result.append(ball)
    return result


def d_longest(n, balls):
    """
    Returns the longest seq for diag 'n'
    :param n:
    :param balls:
    :return:
    """
    filtered = d_filter(n, balls)
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


def find_longest(balls):
    """
    Finds the longest sequence (vertical, diagonal, horizontal) in 'balls'
    :param balls:
    :return:
    """
    sequences = []
    for n in range(1, CELLS + 1):
        tmp = vh_longest(n, balls, True)
        if tmp:
            sequences.append(tmp)
    for n in range(1, CELLS + 1):
        tmp = vh_longest(n, balls, False)
        if tmp:
            sequences.append(tmp)
    for n in range(1, 4*CELLS - 1):
        tmp = d_longest(n, balls)
        if tmp:
            sequences.append(tmp)
    longest = []
    longest_len = 0
    for seq in sequences:
        if len(seq) > longest_len:
            longest = seq[:]
            longest_len = len(seq)
    return longest


def reduce_seq(balls, seq):
    """
    Removes balls from seq from 'balls'
    :param balls:
    :param seq:
    :return:
    """
    for ball in seq:
        balls.remove(ball)

