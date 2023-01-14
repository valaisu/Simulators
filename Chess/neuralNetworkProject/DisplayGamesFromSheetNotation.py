import pygame
import time
import copy

#Testing converting traditional sheet notation to FEN format.
#user can go through games with arrow keys.
#the FEN codes of each move are printed in console.
#castling and en passant fixed

#the sheet notation must be in a text file named "chessgames.txt", located
#in the same directory, as this file.


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




def BoardToFen(board):
    fen = ""
    for i in range(8):
        empty = 0
        for j in range(8):
            if board[i][j] == "*":
                empty += 1
            else:
                if empty != 0:
                    fen += str(empty)
                    empty = 0
                fen += board[i][j]
        if empty != 0:
            fen += str(empty)
        fen += "/"
    return fen


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


def StringToMoves(moves):
    a = len(moves)
    copy = 0
    game = []
    move = ""
    i = 0
    while True:
        if i == a-1:
            break
        if moves[i] == " ":
            copy -= 1
            game.append(move)
            move = ""
            i += 1
        if copy != 0:
            move += moves[i]
        if moves[i] == ".":
            copy = 2
        i += 1
    return game


def PlayMoves(board, moves):
    transfer = ["a", "b", "c", "d", "e", "f", "g", "h"]
    boards = []
    boards.append(board)
    for i in range(len(moves)):
        if moves[i][1] == "-":  # castling
            a = 0
            if i % 2 == 0:
                a = 1
            if len(moves[i]) == 3:
                board[a * 7][6] = board[a * 7][4]
                board[a * 7][4] = "*"
                board[a * 7][5] = board[a * 7][7]
                board[a * 7][7] = "*"
            else:
                board[a * 7][2] = board[a * 7][4]
                board[a * 7][4] = "*"
                board[a * 7][3] = board[a * 7][0]
                board[a * 7][0] = "*"
        elif moves[i][0].islower():  # pawn move
            a = -1
            if i % 2 == 0:
                a = 1  # white to move
            if len(moves[i]) <= 3:#plain move (e4)
                letter = int(transfer.index(moves[i][0]))
                if board[8 - int(moves[i][1]) + a][letter].lower() == "p":
                    board[8 - int(moves[i][1])][letter] = board[8 - int(moves[i][1]) + a][letter]
                    board[8 - int(moves[i][1]) + a][letter] = "*"
                else:
                    board[8 - int(moves[i][1])][letter] = board[8 - int(moves[i][1]) + 2 * a][letter]
                    board[8 - int(moves[i][1]) + 2 * a][letter] = "*"
            else:
                if moves[i][2] == "=":#promotion(e8=D)
                    letter = int(transfer.index(moves[i][0]))
                    if i%2==0:
                        board[8 - int(moves[i][1])][letter] = moves[i][3].upper()
                    else:
                        board[8 - int(moves[i][1])][letter] = moves[i][3].lower()
                    board[8 - int(moves[i][1]) + a][letter] = "*"
                else:#takes(exf4)
                    letterS = transfer.index(moves[i][0])
                    letterD = transfer.index(moves[i][2])
                    board[8 - int(moves[i][3])][letterD] = board[8 - int(moves[i][3]) + a][letterS]
                    board[8 - int(moves[i][3]) + a][letterS] = "*"
                    if len(moves[i]) >= 6:#takes with promotion(exf8=D)
                        if i % 2 == 0:
                            board[8 - int(moves[i][3])][letterD] = moves[i][5].upper()
                        else:
                            board[8 - int(moves[i][3])][letterD] = moves[i][5].lower()

        elif moves[i][1] == "x" or moves[i][2] == "x": #Nxd4, Bxf6+
            if len(moves[i]) == 4:
                letter = transfer.index(moves[i][2])
                SingleMove([letter, 8 - int(moves[i][3])], moves[i][0], ["*", "*"], board, i % 2 == 0)
            else:
                if moves[i][4] == "+":
                    letter = transfer.index(moves[i][2])
                    SingleMove([letter, 8 - int(moves[i][3])], moves[i][0], ["*", "*"], board, i % 2 == 0)
                else:
                    if moves[i][1].isdigit():
                        info = [str(8-int(moves[i][1])), "*"]
                    else:
                        info = ["*", str(transfer.index(moves[i][1]))]
                    letter = transfer.index(moves[i][3])
                    SingleMove([letter, 8 - int(moves[i][4])], moves[i][0], info, board, i % 2 == 0)
        else:
            if len(moves[i]) == 3:
                letter = transfer.index(moves[i][1])
                SingleMove([letter, 8 - int(moves[i][2])], moves[i][0], ["*", "*"], board, i % 2 == 0)
            elif len(moves[i]) == 4:
                if moves[i][3] != "+":
                    if moves[i][1].isdigit():
                        info = [str(8-int(moves[i][1])), "*"]
                    else:
                        info = ["*", str(transfer.index(moves[i][1]))]
                    letter = transfer.index(moves[i][2])
                    SingleMove([letter, 8 - int(moves[i][3])], moves[i][0], info, board, i % 2 == 0)
                else:
                    letter = transfer.index(moves[i][1])
                    SingleMove([letter, 8 - int(moves[i][2])], moves[i][0], ["*", "*"], board, i % 2 == 0)
        PrintBoard(board)
        print(i+1)
        cop = copy.deepcopy(board)
        boards.append(cop)
    return boards


def SingleMove(dest, piece, extra, board, turn):
    if piece.lower() == "q":
        queen(dest, turn, extra, board)
    elif piece.lower() == "r":
        rook(dest, turn, extra, board)
    elif piece.lower() == "b":
        bishop(dest, turn, extra, board)
    elif piece.lower() == "n":
        knight(dest, turn, extra, board)
    elif piece.lower() == "k":
        king(dest, turn, board)


def queen(start, color, extra, board):#start = letter, number; white = True; extra = letter, number
    for q in range(3):
        for w in range(3):
            a = True
            if q != 1 or w != 1:
                i = 1 * (q - 1)
                j = 1 * (w - 1)
                while a:
                    if 7 >= start[1] + i >= 0 and 7 >= start[0] + j >= 0:
                        if board[start[1] + i][start[0] + j].lower() != "*":
                            if board[start[1] + i][start[0] + j].lower() == "q":
                                if board[start[1] + i][start[0] + j].isupper() == color:
                                    if extra[0] != "*" or extra[1] != "*":
                                        if str(start[1] + i) == extra[0] or str(start[0] + j) == extra[1]:
                                            board[start[1]][start[0]] = board[(start[1] + i)][(start[0] + j)]
                                            board[(start[1] + i)][(start[0] + j)] = "*"
                                            return
                                    else:
                                        board[start[1]][start[0]] = board[(start[1] + i)][(start[0] + j)]
                                        board[(start[1] + i)][(start[0] + j)] = "*"
                                        return
                            a = False
                    else:
                        a = False
                    i += 1 * (q - 1)
                    j += 1 * (w - 1)


def king(start, color, board):
    for i in range(3):
        for j in range(3):
            if 0 <= start[1]+i-1 <= 7 and 0 <= start[0]+j-1 <= 7:
                if board[start[1]+i-1][start[0]+j-1].lower() == "k":
                    if board[start[1]+i-1][start[0]+j-1].isupper() == color:
                        board[start[1]][start[0]] = board[start[1]+i-1][start[0]+j-1]
                        board[start[1] + i - 1][start[0] + j - 1] = "*"
                        return


def rook(start, color, extra, board):
    for q in range(3):
        for w in range(3):
            a = True
            if q != 1 or w != 1:
                i = 1 * (q - 1)
                j = 1 * (w - 1)
                while a and (w - 1)*(q - 1) == 0:
                    if 7 >= start[1] + i >= 0 and 7 >= start[0] + j >= 0:
                        if board[start[1] + i][start[0] + j].lower() != "*":
                            if board[start[1] + i][start[0] + j].lower() == "r":
                                if board[start[1] + i][start[0] + j].isupper() == color:
                                    if extra[0] != "*" or extra[1] != "*":
                                        if str(start[1] + i) == extra[0] or str(start[0] + j) == extra[1]:
                                            board[start[1]][start[0]] = board[(start[1] + i)][(start[0] + j)]
                                            board[(start[1] + i)][(start[0] + j)] = "*"
                                            return
                                    else:
                                        board[start[1]][start[0]] = board[(start[1] + i)][(start[0] + j)]
                                        board[(start[1] + i)][(start[0] + j)] = "*"
                                        return
                            a = False
                    else:
                        a = False
                    i += 1 * (q - 1)
                    j += 1 * (w - 1)


def bishop(start, color, extra, board):
    for q in range(3):
        for w in range(3):
            a = True
            if q != 1 or w != 1:
                i = 1 * (q - 1)
                j = 1 * (w - 1)
                while a and (w - 1)*(q - 1) != 0:
                    if 7 >= start[1] + i >= 0 and 7 >= start[0] + j >= 0:
                        if board[start[1] + i][start[0] + j].lower() != "*":
                            if board[start[1] + i][start[0] + j].lower() == "b":
                                if board[start[1] + i][start[0] + j].isupper() == color:
                                    if extra[0] != "*" or extra[1] != "*":
                                        if start[1] + i == extra[0] or start[0] + j == extra[1]:
                                            board[start[1]][start[0]] = board[(start[1] + i)][(start[0] + j)]
                                            board[(start[1] + i)][(start[0] + j)] = "*"
                                            return
                                    else:
                                        board[start[1]][start[0]] = board[(start[1] + i)][(start[0] + j)]
                                        board[(start[1] + i)][(start[0] + j)] = "*"
                                        return
                            a = False
                    else:
                        a = False
                    i += 1 * (q - 1)
                    j += 1 * (w - 1)


def knight(start, color, extra, board):
    for i in range(5):
        for j in range(5):
            if (not 0 < j < 4) or (not 0 < i < 4):
                if (i + j) % 2 == 1:
                    if 0 <= start[1] + i - 2 <= 7 and 0 <= start[0] + j - 2 <= 7:
                        if board[start[1] + i - 2][start[0] + j - 2].lower() == "n":
                            if board[start[1] + i - 2][start[0] + j - 2].isupper() == color:
                                if extra[0] != "*" or extra[1] != "*":
                                    if str([start[1] + i - 2][0]) == extra[0] or str([start[0] + j - 2][0]) == str(extra[1]):
                                        board[start[1]][start[0]] = board[start[1] + i - 2][start[0] + j - 2]
                                        board[start[1] + i - 2][start[0] + j - 2] = "*"
                                        return
                                else:
                                    board[start[1]][start[0]] = board[start[1] + i - 2][start[0] + j - 2]
                                    board[start[1] + i - 2][start[0] + j - 2] = "*"
                                    return


def PrintBoard(board):
    for i in range(8):
        print(board[i])


StartFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR/ w KQkq - 0 1"
boardG = FenToBoard(StartFen)

PrintBoard(boardG)
game = []
f = open("chessgames.txt", "r")
while True:
    a = f.readline()
    if a == "\n":
        while True:
            b = f.readline()
            if b == "\n":
                break
            else:
                game.append(b.rstrip("\n") + " ")
        break

united = ""
for i in range(len(game)):
    united += game[i]
print(united)
g = StringToMoves(united)
print(g)
allPositions = PlayMoves(boardG, g)


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
gameFens.append(boardFen)
counter = 0
while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if not counter + 1 == len(allPositions):
                    counter += 1
                    BoardGraphics(allPositions[counter])
            elif event.key == pygame.K_LEFT:
                counter -= 1
                BoardGraphics(allPositions[counter])
            '''for i in range(len(allPositions)):
                BoardGraphics(allPositions[i])
                time.sleep(1)'''


pygame.quit()
quit()
