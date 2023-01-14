import pygame
import copy

#doesn't recognise castling or en passant

def FenToBoard(fen):
    i = 0
    square = 0
    board = []
    temp = []
    while fen[i] != ' ':
        if fen[i] == '/':
            board.append(temp)
            temp = []
            square = 0
        else:
            if fen[i].isalpha():
                temp.append(fen[i])
                square += 1
            elif fen[i].isdigit():
                square += int(fen[i])
                for j in range(int(fen[i])):
                    temp.append("*")
            else:
                pass
        i += 1
    return board


def BoardToFen(Board):
    fen = ""
    for i in range(8):
        empty = 0
        for j in range(8):
            if Board[i][j] == "*":
                empty += 1
            else:
                if empty != 0:
                    fen += str(empty)
                    empty = 0
                fen += Board[i][j]
        if empty != 0:
            fen += str(empty)
        fen += "/"
    return fen

def Move(start, dest, board, turn, castlings):
    starty = round(start[0]/64-0.51)
    startx = round(start[1]/64-0.51)
    desty = round(dest[0]/64-0.51)
    destx = round(dest[1]/64-0.51)
    if starty == desty and startx == destx:
        return board, turn, castlings
    squares = LegalMove([starty, startx], board)
    for i in range(len(squares)):
        if squares[i] == [destx, desty]:

            if board[startx][starty].islower() == turn:
                return board, turn, castlings
            else:
                turn = not turn
            temp = copy.deepcopy(board)
            board[destx][desty] = board[startx][starty]
            board[startx][starty] = "*"
            for j in range(8):
                for k in range(8):
                    if (board[j][k].lower() == "k") and (board[j][k].islower() == turn):
                        if Check([j, k], not turn, board):
                            print("Virhessiirto")
                            return temp, not turn, castlings
            for j in range(2):
                for k in range(2):
                    if temp[j*7][k*7] != board[j*7][k*7]:
                        castlings[j][k] = 0
                if temp[j*7][4] != board[j*7][4]:
                    castlings[j] = [0, 0]
    return board, turn, castlings


def BoardGraphics(board):
    CreateBoard()
    for i in range(8):
        for j in range(8):
            if board[i][j] == 'k':
                dis.blit(bking, (j * 64, i * 64))
            elif board[i][j] == 'q':
                dis.blit(bqueen, (j * 64, i * 64))
            elif board[i][j] == 'r':
                dis.blit(brook, (j * 64, i * 64))
            elif board[i][j] == 'b':
                dis.blit(bbishop, (j * 64, i * 64))
            elif board[i][j] == 'n':
                dis.blit(bknight, (j * 64, i * 64))
            elif board[i][j] == 'p':
                dis.blit(bpawn, (j * 64, i * 64))
            elif board[i][j] == 'K':
                dis.blit(wking, (j * 64, i * 64))
            elif board[i][j] == 'Q':
                dis.blit(wqueen, (j * 64, i * 64))
            elif board[i][j] == 'R':
                dis.blit(wrook, (j * 64, i * 64))
            elif board[i][j] == 'B':
                dis.blit(wbishop, (j * 64, i * 64))
            elif board[i][j] == 'N':
                dis.blit(wknight, (j * 64, i * 64))
            elif board[i][j] == 'P':
                dis.blit(wpawn, (j * 64, i * 64))
    pygame.display.update()


def CreateBoard():
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                pygame.draw.rect(dis, vanilla, [i * square_size, j * square_size, square_size, square_size])
            else:
                pygame.draw.rect(dis, brown, [i * square_size, j * square_size, square_size, square_size])


def LegalMove(start, board):  # start[0] = y

    squares = []
    if board[start[1]][start[0]].lower() == "k":
        for i in range(3):
            for j in range(3):
                if j != 1 or i != 1:
                    if 7 >= start[1] - 1 + i >= 0 and 7 >= start[0] - 1 + j >= 0:
                        if board[start[1] - 1 + i][start[0] - 1 + j] == "*":
                            squares.append([(start[1] - 1 + i), (start[0] - 1 + j)])
                        else:
                            if board[start[1] - 1 + i][start[0] - 1 + j].islower() != board[start[0]][start[1]].islower():
                                squares.append([(start[1] - 1 + i), (start[0] - 1 + j)])
    elif board[start[1]][start[0]].lower() == "q":
        for q in range(3):
            for w in range(3):
                a = True
                if q != 1 or w != 1:
                    i = 1 * (q - 1)
                    j = 1 * (w - 1)
                    while a:
                        if 7 >= start[1] + i >= 0 and 7 >= start[0] + j >= 0:
                            if board[start[1] + i][start[0] + j] != "*":
                                if board[start[1] + i][start[0] + j].islower() != board[start[1]][start[0]].islower():
                                    squares.append([(start[1] + i), (start[0] + j)])
                                a = False
                            else:
                                squares.append([(start[1] + i), (start[0] + j)])
                        else:
                            a = False
                        i += 1 * (q - 1)
                        j += 1 * (w - 1)

    elif board[start[1]][start[0]].lower() == "r":
        for q in range(3):
            for w in range(3):
                a = True
                if (q-1)*(w-1) == 0 and q != w:
                    i = 1 * (q - 1)
                    j = 1 * (w - 1)
                    while a:
                        if 7 >= start[1] + i >= 0 and 7 >= start[0] + j >= 0:
                            if board[start[1] + i][start[0] + j] != "*":
                                if board[start[1] + i][start[0] + j].islower() != board[start[1]][start[0]].islower():
                                    squares.append([(start[1] + i), (start[0] + j)])
                                a = False
                            else:
                                squares.append([(start[1] + i), (start[0] + j)])
                        else:
                            a = False
                        i += 1 * (q - 1)
                        j += 1 * (w - 1)

    elif board[start[1]][start[0]].lower() == "b":
        for q in range(3):
            for w in range(3):
                a = True
                if abs(q-1) == abs(w-1) and (q-1)*(w-1) != 0:
                    i = 1 * (q - 1)
                    j = 1 * (w - 1)
                    while a:
                        if 7 >= start[1] + i >= 0 and 7 >= start[0] + j >= 0:
                            if board[start[1] + i][start[0] + j] != "*":
                                if board[start[1] + i][start[0] + j].islower() != board[start[1]][start[0]].islower():
                                    squares.append([(start[1] + i), (start[0] + j)])
                                a = False
                            else:
                                squares.append([(start[1] + i), (start[0] + j)])
                        else:
                            a = False
                        i += 1 * (q - 1)
                        j += 1 * (w - 1)

    elif board[start[1]][start[0]].lower() == "n":
        for i in range(5):
            for j in range(5):
                if (not 0 < j < 4) or (not 0 < i < 4):
                    if (i + j) % 2 == 1:
                        if 0 <= start[1] + i - 2 <= 7 and 0 <= start[0] + j - 2 <= 7:
                            if board[start[1] + i - 2][start[0] + j - 2] == "*":
                                squares.append([(start[1] + i - 2), (start[0] + j - 2)])
                            elif board[start[1] + i - 2][start[0] + j - 2].islower() != board[start[1]][start[0]].islower():
                                squares.append([(start[1] + i - 2), (start[0] + j - 2)])
    elif board[start[1]][start[0]] == "p":
        if board[start[1] + 1][start[0]] == "*":
            squares.append([(start[1] + 1), (start[0])])
            if board[3][start[0]] == "*" and start[1] == 1:
                squares.append([(start[1] + 2), (start[0])])
        for i in range(2):
            if 0 <= start[0]+(i*2-1) <= 7:
                if board[start[1]+1][start[0]+(i*2-1)].upper() and board[start[1]+1][start[0]+(i*2-1)] != "*":
                    squares.append([(start[1]+1), (start[0]+(i*2-1))])
    elif board[start[1]][start[0]] == "P":
        if board[start[1] - 1][start[0]] == "*":
            squares.append([(start[1] - 1), (start[0])])
            if board[4][start[0]] == "*" and start[1] == 6:
                squares.append([(start[1] - 2), (start[0])])
        for i in range(2):
            if 0 <= start[0]-(i*2-1) <= 7:
                if board[start[1]-1][start[0]-(i*2-1)].upper() and board[start[1]-1][start[0]-(i*2-1)] != "*":
                    squares.append([(start[1]-1), (start[0]-(i*2-1))])
    return squares


def Check(start, color, board): #True = whiteKing
    #king
    for i in range(3):
        for j in range(3):
            if j != 1 or i != 1:
                if 7 >= start[1] - 1 + i >= 0 and 7 >= start[0] - 1 + j >= 0:
                    if board[start[0] - 1 + j][start[1] - 1 + i].lower() == "k":
                        if board[start[0] - 1 + j][start[1] - 1 + i].islower() == color:
                            return True
    #bishop, rook, queen
    for q in range(3):
        for w in range(3):
            a = True
            if q != 1 or w != 1:
                i = 1 * (q - 1)
                j = 1 * (w - 1)
                while a:
                    if 7 >= start[1] + j >= 0 and 7 >= start[0] + i >= 0:
                        if board[start[0] + i][start[1] + j] != "*":
                            if (q-1)*(w-1) == 0 and (board[start[0]+i][start[1]+j].lower() == "r" or board[start[0]+i][start[1]+j].lower() == "q"):
                                if board[start[0] + i][start[1] + j].islower() == color:
                                    return True
                            if abs(q-1)-abs(w-1) == 0 and (board[start[0]+i][start[1]+j].lower() == "b" or board[start[0]+i][start[1]+j].lower() == "q"):
                                if board[start[0] + i][start[1] + j].islower() == color:
                                    return True
                            a = False
                    else:
                        a = False
                    i += 1 * (q - 1)
                    j += 1 * (w - 1)
    #knight
    for i in range(5):
        for j in range(5):
            if (not 0 < j < 4) or (not 0 < i < 4):
                if (i + j) % 2 == 1:
                    if 0 <= start[1] + i - 2 <= 7 and 0 <= start[0] + j - 2 <= 7:
                        if board[start[0] + j - 2][start[1] + i - 2].lower() == "n":
                            if color == board[start[0] + j - 2][start[1] + i - 2].islower():
                                return True
    #pawn
    a = - 1
    if not color:
        a = + 1
    for i in range(2):
        if 0 <= start[0]+i*2-1 <= 7 and 0 <= start[1]+a <= 7:
            if board[start[0]+a][start[1]+i*2-1].lower() == "p":
                if color != board[start[0]+a][start[1]+i*2-1].isupper():
                    return True

    return False

boardFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR/ w KQkq - 0 1"
board = FenToBoard(boardFen)

bking = pygame.image.load('BlackKing2^8.png')
bking = pygame.transform.scale(bking, (64,64))
bqueen = pygame.image.load('BQueen.png')
bqueen = pygame.transform.scale(bqueen, (64,64))
brook = pygame.image.load('BRook.png')
brook = pygame.transform.scale(brook, (64,64))
bbishop = pygame.image.load('BBishop.png')
bbishop = pygame.transform.scale(bbishop, (64,64))
bknight = pygame.image.load('BHorse.png')
bknight = pygame.transform.scale(bknight, (64,64))
bpawn = pygame.image.load('BPawn.png')
bpawn = pygame.transform.scale(bpawn, (64,64))

wking = pygame.image.load('WKing.png')
wking = pygame.transform.scale(wking, (64,64))
wqueen = pygame.image.load('WQueen.png')
wqueen = pygame.transform.scale(wqueen, (64,64))
wrook = pygame.image.load('WRook.png')
wrook = pygame.transform.scale(wrook, (64,64))
wbishop = pygame.image.load('WBishop.png')
wbishop = pygame.transform.scale(wbishop, (64,64))
wknight = pygame.image.load('WKnight.png')
wknight = pygame.transform.scale(wknight, (64,64))
wpawn = pygame.image.load('WPawn.png')
wpawn = pygame.transform.scale(wpawn, (64,64))

pygame.init()

gameOver = False
size = 512
square_size = 64
dis = pygame.display.set_mode((size, size))
brown = (220, 130, 50)
vanilla = (210, 205, 185)
CreateBoard()
BoardGraphics(board)
pygame.display.update()
whiteToMove = True
castlings = [[1,1],[1,1]]
startCoordinates = []
gameFens = []


while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            startCoordinates = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:
            temp = Move(startCoordinates, pygame.mouse.get_pos(), board, whiteToMove, castlings)
            board = temp[0]
            whiteToMove = temp[1]
            castlings = temp[2]
            BoardGraphics(board)
            gameFens.append(BoardToFen(board))
pygame.quit()
quit()
