import copy

#converts games from move information to FEN
#Then converts FEN to similar structure, where
#Pieces are described with their value
# white pawn 1
# black knight -3
# white rook 5
# and so on
# also white king 40 > all other pieces combined
# Each position described as a list on their own lines
# in ChessData.csv. The last nuber on each row tells game
# result.

# Saves the data in "ChessData.csv". This file must pre-exists.
# Everything seems to work as intended

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
        try:
            if moves[i] == " ":
                copy -= 1
                game.append(move)
                move = ""
                i += 1
        except IndexError:
            print(moves)
            break
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
                    if board[8 - int(moves[i][3])][letterD] == "*":#en passant
                        board[8 - int(moves[i][3]) + a][letterD] = "*"
                    board[8 - int(moves[i][3])][letterD] = board[8 - int(moves[i][3]) + a][letterS]
                    board[8 - int(moves[i][3]) + a][letterS] = "*"
                    if len(moves[i]) >= 6:#takes with promotion(exf8=D)
                        if i % 2 == 0:
                            board[8 - int(moves[i][3])][letterD] = moves[i][5].upper()
                        else:
                            board[8 - int(moves[i][3])][letterD] = moves[i][5].lower()

        elif moves[i][1] == "x" or moves[i][2] == "x":
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
        #PrintBoard(board)
        #print(i+1)
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


def WriteToFile(game, result):
    StartFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR/ w KQkq - 0 1"
    boardG = FenToBoard(StartFen)
    united = ""
    for i in range(len(game)):
        united += game[i]
    g = StringToMoves(united)
    allPositions = PlayMoves(boardG, g)
    another = open("ChessData.csv", "a")
    for i in range(len(allPositions)-1):
        tempo = ""
        for j in range(8):
            for k in range(8):
                tempo += allPositions[i+1][j][k]
        tempo += str(result)
        if i % 2 == 1:
            tempo+="w"
        else:
            tempo+="b"
        tempo += "\n"
        t = len(tempo)
        for j in range(t-3):
            if tempo[j] == "*":
                another.write(str(0) + ",")
            elif tempo[j] == "K":
                another.write(str(1) + ",")
            elif tempo[j] == "Q":
                another.write(str(9/40) + ",")
            elif tempo[j] == "R":
                another.write(str(5/40) + ",")
            elif tempo[j] == "N":
                another.write(str(3/40) + ",")
            elif tempo[j] == "B":
                another.write(str(3/40) + ",")
            elif tempo[j] == "P":
                another.write(str(1/40) + ",")
            elif tempo[j] == "k":
                another.write(str(-1) + ",")
            elif tempo[j] == "q":
                another.write(str(-9/40) + ",")
            elif tempo[j] == "r":
                another.write(str(-5/40) + ",")
            elif tempo[j] == "b":
                another.write(str(-3/40) + ",")
            elif tempo[j] == "n":
                another.write(str(-3/40) + ",")
            elif tempo[j] == "p":
                another.write(str(-1/40) + ",")
        if tempo[t-2] == "w":
            another.write(str(1) + ",")
        else:
            another.write(str(-1) + ",")
        if tempo[t-3] == "0":
            another.write(str(-1) + "\n")
        elif tempo[t-3] == "2":
            another.write(str(1) + "\n")
        else:
            another.write(str(0) + "\n")
    another.close()


f = open("adams.txt", "r")
mode = False
result = 0
game = []
totalGames = 0
totalPositions = 0
for line in f:
    if line[0] == "\n":
        mode = not mode
        if not mode:
            totalGames += 1
            totalPositions += len(game)
            WriteToFile(game, result)
            game = []
    elif not mode and line[2] == "e":
        if line[12] == "-":
            result = 1
        elif line[9] == "1":
            result = 2
        else:
            result = 0
    elif mode:
        game.append(line.rstrip("\n")+" ")
print(str(totalGames) + " games converted")


f.close()
