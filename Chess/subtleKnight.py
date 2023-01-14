import random
import pygame

# The classic chess puzzle many people have encountered is following:
# On an otherwise empty board there is a knight. The knight has a quest:
# It has to move in a fashion, such that it visists every square once,
# and only once.
# My friend claimed, that a winning strategy in this game is to always
# move the knight in a square, such that you minimize the moving options
# on your next turn.
# This program allows user to test this hypothesis on an n*n board
# spoiler alert: it does work, how ever if the board has odd number
# of squares, you have about 50 50 chance to not be able to win, as the
# knight always has to jump on a square of different color


def find_smallest(lista):
    temp = 8
    index = 0
    for i in range(len(lista)):
        if lista[i] <= temp:
            index = i
            temp = lista[i]
    return index


def get_squares(start, board, size):
    a = [-2, -1, 1, 2, 2, 1, -1, -2]
    b = [1, 2, 2, 1, -1, -2, -2, -1]
    squares = []
    vals = []
    for i in range(8):
        if 0 <= start[0] + a[i] <= size-1 and 0 <= start[1] + b[i] <= size-1:
            if board[start[0] + a[i]][start[1] + b[i]] == "O":
                squares.append([start[0] + a[i], start[1] + b[i]])

    for i in range(len(squares)):
        vals.append(square_value(squares[i], board, size))

    index = find_smallest(vals)
    if len(vals) == 0:
        return -1
    else:
        return squares[index]


def square_value(start, board, size):
    a = [-2, -1, 1, 2, 2, 1, -1, -2]
    b = [1, 2, 2, 1, -1, -2, -2, -1]
    tot = 0
    for i in range(8):
        if 0 <= start[0] + a[i] <= size-1 and 0 <= start[1] + b[i] <= size-1:
            if board[start[0] + a[i]][start[1] + b[i]] == "O":
                tot += 1
    return tot

def CreateBoard(size):
    for i in range(size):
        for j in range(size):
            if (i + j) % 2 == 0:
                pygame.draw.rect(dis, vanilla, [i * int(512/size), j * int(512/size), int(512/size), int(512/size)])
                print(int(512/size))
            else:
                pygame.draw.rect(dis, brown, [i * int(512/size), j * int(512/size), int(512/size), int(512/size)])


pygame.init()


size = 512
square_size = 64
dis = pygame.display.set_mode((size, size))
brown = (220, 130, 50)
vanilla = (210, 205, 185)


def CreateBoard(size):
    for i in range(size):
        for j in range(size):
            if (i+j) % 2 == 0:
                pygame.draw.rect(dis, vanilla, [i * square_size, j * square_size, square_size, square_size])
            else:
                pygame.draw.rect(dis, brown, [i * square_size, j * square_size, square_size, square_size])


def BoardGraphics(board, size, knight):
    for i in range(size):
        for j in range(size):
            if board[i][j] == "X":
                dis.blit(knight, (j*512/size, i*512/size))

def Animation(size, all_boadrs):
    knight = pygame.image.load('knight.png')
    knight = pygame.transform.scale(knight, (int(512 / size), int(512 / size)))

    CreateBoard(size)
    BoardGraphics(all_boadrs[0], size, knight)
    pygame.display.update()

    gameOver = False
    while not gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True
    pygame.quit()
    quit()

def main():

    size = int(input("laudan koko (n*n)"))
    board = []
    all_boards = []
    for i in range(size):
        temp = []
        for j in range(size):
            temp.append("O")
        board.append(temp)

    start = [random.randint(0, size-1),random.randint(0, size-1)]
    board[start[0]][start[1]] = "X"

    success = 1
    for k in range(size*size-1):
        start = get_squares(start, board, size)
        if start == -1:
            success = 0
            break
        board[start[0]][start[1]] = "X"
        all_boards.append(board)
        for i in range(size):
            print(board[i])
        print("----------------------------------------", k)

        Animation(size, all_boards)



main()
