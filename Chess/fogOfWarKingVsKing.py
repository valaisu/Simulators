import random

# Fog of war is a chess variant, where the player can only see opponents peaces,
# if they are on squares this player can move some of his own pieces to.
# In this variant, lets imagine a situation, where both players have only the king
# left. If they were to move randomly around, eventually the other player would,
# unfortunately, move into a square, where he can be eaten. The question is, what
# is the optimal strategy in a king vs king situation.
# Obviously it depends on the opponents strategy. And that cannot be known. But if
# we assume that the opponent strategy is to move aimlessly around, we can have an
# optimal strategy.

# This program calculates the winning chances, when one player moves between two
# squares, and the other wanders around aimlessly. Both players eat the enemy king
# once given the chance

def Passive(board, piece):
    pos = (-1, -1)
    for i in range(8):
        for j in range(8):
            if board[i][j] == piece:
                pos = i, j
    '''if pos[0] < 2:
        board[pos[0] + 1][pos[1]] = piece
        board[pos[0]][pos[1]] = 0'''
    board[pos[0]-1+((1+pos[0])%2)*2][pos[1]] = piece #works always
    #board[pos[0] - 1 + (pos[0] % 2) * 2][pos[1]] = piece #works while not on edge
    board[pos[0]][pos[1]] = 0

    return board, NextTo(board, piece)


def Active(board, piece):
    pos = (-1, -1)
    for i in range(8):
        for j in range(8):
            if board[i][j] == piece:
                pos = i, j
    squares = []
    for i in range(3):
        for j in range(3):
            if 0 <= i + pos[0] - 1 < 8 and 0 <= j + pos[1] - 1 < 8:
                if i != 1 or j != 1:
                    squares.append([i + pos[0] - 1, j + pos[1] - 1])

    board[pos[0]][pos[1]] = 0
    a = random.randint(0, len(squares)-1)
    choice = squares[a]
    board[choice[0]][choice[1]] = piece
    return board, NextTo(board, piece)


def NextTo(board, piece):
    pos = (-1, -1)
    for i in range(8):
        for j in range(8):
            if board[i][j] == piece:
                pos = i, j
    for i in range(3):
        for j in range(3):
            if 0 <= i+pos[0]-1 < 8 and 0 <= j+pos[1]-1 < 8:
                if i != 1 or j != 1:
                    if board[i+pos[0]-1][j+pos[1]-1] != 0:
                        return True
    return False

'''for e in range(1, 7):
    for r in range(8):'''
activeWin = 0
passiveWin = 0

for k in range(100000):
    board = []

    for i in range(8):
        temp = []
        for j in range(8):
            temp.append(0)
        board.append(temp)

    a = [1, 7]
    b = [random.randint(0, 7), random.randint(0, 7)]

    board[a[0]][a[1]] = 1
    board[b[0]][b[1]] = 2

    #print(NextTo(board, 1), a, b)

    if a != b and not NextTo(board, 1):

        go = 0
        while (go < 100):

            board, c = Active(board, 2)
            if c:
                passiveWin += 1
                go += 100
            board, d = Passive(board, 1)
            if d and go < 100:
                activeWin += 1
                go += 100


print("Passive strategy wins " + str(100*passiveWin/(activeWin+passiveWin)) + "% of the time with starting square: " + str(1) + str(7))
