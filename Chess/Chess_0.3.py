import copy
import random

Files = ["a","b","c","d","e","f","g","h"]
Ranks = ["8","7","6","5","4","3","2","1"]
PieceVals = {
    "0" : 0,
    "p" : -1,
    "P" : 1,
    "n" : -3,
    "N" : 3,
    "b" : -3,
    "B" : 3,
    "r" : -5,
    "R" : 5,
    "q" : -9,
    "Q" : 9,
    "k" : 0,
    "K" : 0
}
CurrentState = []
# r3k2r/1b1p1ppp/p3p2q/1p2n3/3NPKn1/P5R1/BPP5/RNBQ4 w kq - 10 19
def AlgebraicToCoords(pos):
    return([Ranks.index(pos[1]), Files.index(pos[0])])

def FromFEN(FEN):
    fields = FEN.split(" ")
    boardStr = fields[0].split("/")
    board = []
    EnPassant = []
    for row in range(len(boardStr)):
        board.append([])
        for tile in boardStr[row]:
            try:
                for n in range(int(tile)):
                    board[row].append("0")
            except:
                board[row].append(tile)
    if fields[3] != "-":
        EnPassant = AlgebraicToCoords(fields[3])
    else:
        EnPassant = [9,9]
    return([board, fields[1], fields[2], EnPassant, fields[4], fields[5]])

def ToFEN(board, turn, castles, enPassant, halfmove, fullmove):
    FEN = ""
    boardStr = ""
    for rank in board:
        boardStr+="/"
        blanks = 0
        for file in rank:
            if file != "0":
                if blanks != 0:
                    boardStr+= str(blanks)
                boardStr+= file
                blanks = 0
            else:
                blanks+=1
                boardStr
        if blanks != 0:
            boardStr+= str(blanks)
    boardStr = boardStr[1:] # Removes the first "/"
    FEN += boardStr + " " + turn + " " + castles + " "
    if enPassant != [9,9]:
        FEN += Files[enPassant[1]] + Ranks[enPassant[0]]
    else:
        FEN += "-"
    return(FEN + " " + halfmove + " " + fullmove)

def MakeMove(board, start, end, special):
    global CurrentState
    afterBoard = copy.deepcopy(board)
    Color = board[start[0]][start[1]].isupper()
    CurrentState[3] = [9,9]
    match special:
        case "normal":
            afterBoard[end[0]][end[1]] = board[start[0]][start[1]]
            afterBoard[start[0]][start[1]] = "0"
            if board[start[0]][start[1]] == "P" or board[start[0]][start[1]] == "p": # Records the en passant
                if abs(start[0]-end[0]) == 2:
                    CurrentState[3] = (start[0]-(2/(start[0]-end[0])),start[1])
                    
            if "K" in CurrentState[2] or "Q" in CurrentState[2]: # Cancelling castling for white
                if start == (7,4): # If white moves its king
                    CurrentState[2] = CurrentState[2].replace("K","").replace("Q","")
                if start == (7,0) or end == (7,0): # If the rooks get moved or captured
                    CurrentState[2] = CurrentState[2].replace("Q","")
                if start == (7,7) or end == (7,7):
                    CurrentState[2] = CurrentState[2].replace("K","")
            if "k" in CurrentState[2] or "q" in CurrentState[2]: # Cancelling castling for black
                if start == (0,4): # If black moves its king
                    CurrentState[2] = CurrentState[2].replace("k","").replace("q","")
                if start == (0,0) or end == (0,0): # If the rooks get moved or captured
                    CurrentState[2] = CurrentState[2].replace("q","")
                if start == (0,7) or end == (0,7):
                    CurrentState[2] = CurrentState[2].replace("k","")                    
        case "prom_queen":
            if Color:
                afterBoard[end[0]][end[1]] = "Q"
            else:
                afterBoard[end[0]][end[1]] = "q"
            afterBoard[start[0]][start[1]] = "0"
        case "prom_rook":
            if Color:
                afterBoard[end[0]][end[1]] = "R"
            else:
                afterBoard[end[0]][end[1]] = "r"
            afterBoard[start[0]][start[1]] = "0"
        case "prom_bishop":
            if Color:
                afterBoard[end[0]][end[1]] = "B"
            else:
                afterBoard[end[0]][end[1]] = "b"
            afterBoard[start[0]][start[1]] = "0"
        case "prom_knight":
            if Color:
                afterBoard[end[0]][end[1]] = "N"
            else:
                afterBoard[end[0]][end[1]] = "n"
            afterBoard[start[0]][start[1]] = "0"
        case "kingCastle":
            afterBoard[end[0]][end[1]] = board[start[0]][start[1]]# Moves the king
            afterBoard[start[0]][start[1]] = "0"
            afterBoard[end[0]][end[1]-1] = board[end[0]][end[1]+1]# Move the rook
            afterBoard[end[0]][end[1]+1] = "0"
            if board[start[0]][start[1]] == "K":
                CurrentState[2] = CurrentState[2].replace("K","")
            else:
                CurrentState[2] = CurrentState[2].replace("k","")
        case "queenCastle":
            afterBoard[end[0]][end[1]] = board[start[0]][start[1]]# Moves the king
            afterBoard[start[0]][start[1]] = "0"
            afterBoard[end[0]][end[1]+1] = board[end[0]][end[1]-2]# Move the rook
            afterBoard[end[0]][end[1]-2] = "0"
            if board[start[0]][start[1]] == "K":
                CurrentState[2] = CurrentState[2].replace("Q","").replace("K","")
            else:
                CurrentState[2] = CurrentState[2].replace("q","").replace("k","")
        case "enPassant":
            afterBoard[end[0]][end[1]] = board[start[0]][start[1]]
            afterBoard[start[0]][start[1]] = "0"
            if Color:
                afterBoard[end[0]+1][end[1]] = "0"
            else:
                afterBoard[end[0]-1][end[1]] = "0"
    return(afterBoard)

def Look(board,pos,offset,piece):
    if pos[0]+offset[0]>=0 and pos[0]+offset[0]<=7 and pos[1]+offset[1]>=0 and pos[1]+offset[1]<=7:
        match piece:
            case "empty":
                return(board[pos[0]+offset[0]][pos[1]+offset[1]] == "0")
            case "white":
                return(board[pos[0]+offset[0]][pos[1]+offset[1]] != "0" and board[pos[0]+offset[0]][pos[1]+offset[1]].isupper())
            case "black":
                return(board[pos[0]+offset[0]][pos[1]+offset[1]] != "0" and board[pos[0]+offset[0]][pos[1]+offset[1]].islower())
            case _:
                return(board[pos[0]+offset[0]][pos[1]+offset[1]].lower() == piece)
    else:
        return(False)
def IsKingSafe(board, pos, OppColor):
    if OppColor == "black": # Checks for the pawn diagonals
        if Look(board, pos, (-1,1), "k") or (Look(board, pos, (-1,1), "p") and Look(board, pos, (-1,1), "black")): # attacked from up right by a king or pawn
            return(False)
        if Look(board, pos, (-1,-1), "k") or (Look(board, pos, (-1,-1), "p") and Look(board, pos, (-1,-1), "black")): # attacked from up left by a king or pawn
            return(False)
    else:
        if Look(board, pos, (1,1), "k") or (Look(board, pos, (1,1), "p") and Look(board, pos, (1,1), "white")): # attacked from down right by a king or pawn
            return(False)
        if Look(board, pos, (1,-1), "k") or (Look(board, pos, (1,-1), "p") and Look(board, pos, (1,-1), "white")): # attacked from down left by a king or pawn
            return(False)        
    if Look(board, pos, (-1,0), "k"): # attacked from up by a king
        return(False)
    if Look(board, pos, (0,1), "k"): # attacked from right by a king
        return(False)
    if Look(board, pos, (1,0), "k"): # attacked from down by a king
        return(False)
    if Look(board, pos, (0,-1), "k"): # attacked from left by a king
        return(False)
    if Look(board, pos, (-2, -1), "n") and Look(board, pos, (-2, -1), OppColor): # attacked from up left by a knight
        return(False)
    if Look(board, pos, (-2, 1), "n") and Look(board, pos, (-2, 1), OppColor): # attacked from up right by a knight
        return(False)
    if Look(board, pos, (-1, 2), "n") and Look(board, pos, (-1, 2), OppColor): # attacked from right up by a knight
        return(False)
    if Look(board, pos, (1, 2), "n") and Look(board, pos, (1, 2), OppColor): # attacked from right down by a knight
        return(False)
    if Look(board, pos, (2, 1), "n") and Look(board, pos, (2, 1), OppColor): # attacked from down right by a knight
        return(False)
    if Look(board, pos, (2, -1), "n") and Look(board, pos, (2, -1), OppColor): # attacked from down left by a knight
        return(False)
    if Look(board, pos, (1, -2), "n") and Look(board, pos, (1, -2), OppColor): # attacked from left down by a knight
        return(False)
    if Look(board, pos, (-1, -2), "n") and Look(board, pos, (-1, -2), OppColor): # attacked from left up by a knight
        return(False)
    y = -1 # attacked from up by a rook or queen
    while pos[0]+y >= 0:
        if Look(board, pos, (y,0), "empty"):
            y-=1
            continue
        elif Look(board, pos, (y,0), OppColor):
            if Look(board, pos, (y,0), "r") or Look(board, pos, (y,0), "q"):
                return(False)
            else:
                break            
            
        else:
            break
        y-=1
    x = 1 # queen or rook right
    while pos[1]+x <= 7:
        if Look(board, pos, (0,x), "empty"):
            x+=1
            continue
        elif Look(board, pos, (0,x), OppColor):
            if Look(board, pos, (0,x), "r") or Look(board, pos, (0,x), "q"):
                return(False)
            else:
                break            
        else:
            break
        x+=1            
    y = 1 # queen or rook down
    while pos[0]+y <= 7:
        if Look(board, pos, (y,0), "empty"):
            y+=1
            continue
        elif Look(board, pos, (y,0), OppColor):
            if Look(board, pos, (y,0), "r") or Look(board, pos, (y,0), "q"):
                return(False)
            else:
                break            
        else:
            break
        y+=1
    x = -1 # queen or rook left
    while pos[1]+x >= 0:
        if Look(board, pos, (0,x), "empty"):
            x-=1
            continue
        elif Look(board, pos, (0,x), OppColor):
            if Look(board, pos, (0,x), "r") or Look(board, pos, (0,x), "q"):
                return(False)
            else:
                break            
        else:
            break
        x-=1
    y = -1 # queen or bishop up left
    while pos[0]+y >= 0 and pos[1]+y >= 0:
        if Look(board, pos, (y,y), "empty"):
            y-=1
            continue
        elif Look(board, pos, (y,y), OppColor):
            if Look(board, pos, (y,y), "b") or Look(board, pos, (y,y), "q"):
                return(False)
            else:
                break            
        else:
            break
        y-=1
    y = -1 # queen or bishop up right
    while pos[0]+y >= 0 and pos[1]-y <= 7:
        if Look(board, pos, (y,-1*y), "empty"):
            y-=1
            continue
        elif Look(board, pos, (y,-1*y), OppColor):
            if Look(board, pos, (y,-1*y), "b") or Look(board, pos, (y,-1*y), "q"):
                return(False)
            else:
                break            
        else:
            break
        y-=1
    y = 1 # queen or bishop down right
    while pos[0]+y <= 7 and pos[1]+y <= 7:
        if Look(board, pos, (y,y), "empty"):
            y+=1
            continue
        elif Look(board, pos, (y,y), OppColor):
            if Look(board, pos, (y,y), "b") or Look(board, pos, (y,y), "q"):
                return(False)
            else:
                break
        else:
            break
        y+=1
    y = 1 # queen or bishop down left
    while pos[0]+y <= 7 and pos[1]-y >= 0:
        if Look(board, pos, (y,-1*y), "empty"):
            y+=1
            continue
        elif Look(board, pos, (y,-1*y), OppColor):
            if Look(board, pos, (y,-1*y), "b") or Look(board, pos, (y,-1*y), "q"):
                return(False)
            else:
                break            
        else:
            break
        y+=1
    return(True)
def GetBoardScore(board):
    Bscore = 0
    for rank in board:
        for piece in rank:
            Bscore+=PieceVals[piece]
    return(Bscore)
def FindKing(board, Color):
    if Color == "white":
        for rank in range(len(board)):
            if "K" in board[rank]:
                return((rank, board[rank].index("K")))
    else:
        for rank in range(len(board)):
            if "k" in board[rank]:
                return((rank, board[rank].index("k")))
    
def ValidMoves(board, pos, EnPassant, Castles):
    global CurrentState
    piece = board[pos[0]][pos[1]].lower()
    if board[pos[0]][pos[1]].isupper():
        OppColor = "black"
        Color = "white"
    else:
        OppColor = "white"
        Color = "black"
    moves = []
    validmoves = []
    match piece:
        case "p":                                                                                # PAWNS
            if Color == "white": # For white pawns
                if Look(board,pos,(-1,0),"empty"):                 # pawn up 1
                    moves.append((pos,(pos[0]-1,pos[1]),"normal"))
                if pos[0] == 6 and Look(board,pos,(-2,0),"empty") and Look(board,pos,(-1,0),"empty"): # pawn up 2
                    moves.append((pos,(pos[0]-2,pos[1]),"normal"))
                if Look(board,pos,(-1,-1),"black"):                # takes left
                    if pos[0] == 1: # promotions
                        moves.append((pos,(pos[0]-1,pos[1]-1),"prom_queen"))
                        moves.append((pos,(pos[0]-1,pos[1]-1),"prom_rook"))
                        moves.append((pos,(pos[0]-1,pos[1]-1),"prom_bishop"))
                        moves.append((pos,(pos[0]-1,pos[1]-1),"prom_knight"))
                    else:
                        moves.append((pos,(pos[0]-1,pos[1]-1),"normal"))
                if Look(board,pos,(-1,1),"black"):                 # takes right
                    if pos[0] == 1: # promotions
                        moves.append((pos,(pos[0]-1,pos[1]+1),"prom_queen"))
                        moves.append((pos,(pos[0]-1,pos[1]+1),"prom_rook"))
                        moves.append((pos,(pos[0]-1,pos[1]+1),"prom_bishop"))
                        moves.append((pos,(pos[0]-1,pos[1]+1),"prom_knight"))
                    else:
                        moves.append((pos,(pos[0]-1,pos[1]+1),"normal"))
                if (pos[0]-1,pos[1]-1) == EnPassant:               # en passant left
                    moves.append((pos,(pos[0]-1,pos[1]-1),"enPassant"))
                if (pos[0]-1,pos[1]+1) == EnPassant:               # en passant right
                    moves.append((pos,(pos[0]-1,pos[1]+1),"enPassant"))              
                if Look(board,pos,(-1,0),"empty") and pos[0] == 1: # promotions
                    moves.append((pos,(pos[0]-1,pos[1]),"prom_queen"))
                    moves.append((pos,(pos[0]-1,pos[1]),"prom_rook"))
                    moves.append((pos,(pos[0]-1,pos[1]),"prom_bishop"))
                    moves.append((pos,(pos[0]-1,pos[1]),"prom_knight"))
            else: # For black pawns
                if Look(board,pos,(1,0),"empty"):                 # pawn up 1
                    moves.append((pos,(pos[0]+1,pos[1]),"normal"))
                if pos[0] == 1 and Look(board,pos,(2,0),"empty") and Look(board,pos,(1,0),"empty"): # pawn up 2
                    moves.append((pos,(pos[0]+2,pos[1]),"normal"))
                if Look(board,pos,(1,-1),"white"):                # takes left
                    if pos[0] == 6: # promotions
                        moves.append((pos,(pos[0]+1,pos[1]-1),"prom_queen"))
                        moves.append((pos,(pos[0]+1,pos[1]-1),"prom_rook"))
                        moves.append((pos,(pos[0]+1,pos[1]-1),"prom_bishop"))
                        moves.append((pos,(pos[0]+1,pos[1]-1),"prom_knight"))
                    else:
                        moves.append((pos,(pos[0]+1,pos[1]-1),"normal"))
                if Look(board,pos,(1,1),"white"):                 # takes right
                    if pos[0] == 6: # promotions
                        moves.append((pos,(pos[0]+1,pos[1]+1),"prom_queen"))
                        moves.append((pos,(pos[0]+1,pos[1]+1),"prom_rook"))
                        moves.append((pos,(pos[0]+1,pos[1]+1),"prom_bishop"))
                        moves.append((pos,(pos[0]+1,pos[1]+1),"prom_knight"))
                    else:
                        moves.append((pos,(pos[0]+1,pos[1]+1),"normal"))
                if (pos[0]+1,pos[1]-1) == EnPassant:               # en passant left
                    moves.append((pos,(pos[0]+1,pos[1]-1),"enPassant"))
                if (pos[0]+1,pos[1]+1) == EnPassant:               # en passant right
                    moves.append((pos,(pos[0]+1,pos[1]+1),"enPassant"))              
                if Look(board,pos,(+1,0),"empty") and pos[0] == 6: # promotions
                    moves.append((pos,(pos[0]+1,pos[1]),"prom_queen"))
                    moves.append((pos,(pos[0]+1,pos[1]),"prom_rook"))
                    moves.append((pos,(pos[0]+1,pos[1]),"prom_bishop"))
                    moves.append((pos,(pos[0]+1,pos[1]),"prom_knight"))                
        case "k":                                                                                   # KINGS
            if Look(board,pos,(-1,-1),"empty") or Look(board,pos,(-1,-1),OppColor): # king up left
                moves.append((pos,(pos[0]-1,pos[1]-1),"normal"))
            if Look(board,pos,(-1,0),"empty") or Look(board,pos,(-1,0),OppColor): # king up 
                moves.append((pos,(pos[0]-1,pos[1]),"normal"))
            if Look(board,pos,(-1,1),"empty") or Look(board,pos,(-1,1),OppColor): # king up right
                moves.append((pos,(pos[0]-1,pos[1]+1),"normal"))
            if Look(board,pos,(0,1),"empty") or Look(board,pos,(0,1),OppColor): # king right
                moves.append((pos,(pos[0],pos[1]+1),"normal"))
            if Look(board,pos,(1,1),"empty") or Look(board,pos,(1,1),OppColor): # king down right
                moves.append((pos,(pos[0]+1,pos[1]+1),"normal"))
            if Look(board,pos,(1,0),"empty") or Look(board,pos,(1,0),OppColor): # king down
                moves.append((pos,(pos[0]+1,pos[1]),"normal"))
            if Look(board,pos,(1,-1),"empty") or Look(board,pos,(1,-1),OppColor): # king down left
                moves.append((pos,(pos[0]+1,pos[1]-1),"normal"))
            if Look(board,pos,(0,-1),"empty") or Look(board,pos,(0,-1),OppColor): # king left
                moves.append((pos,(pos[0],pos[1]-1),"normal"))
            if Color == "white":
                if "K" in Castles and Look(board,pos,(0,1),"empty") and Look(board,pos,(0,2),"empty"): # king castle
                    moves.append((pos,(pos[0],pos[1]+2),"kingCastle"))
                if "Q" in Castles and Look(board,pos,(0,-1),"empty") and Look(board,pos,(0,-2),"empty") and Look(board,pos,(0,-3),"empty"): # king castle
                    moves.append((pos,(pos[0],pos[1]-2),"queenCastle"))
            else:
                if "k" in Castles and Look(board,pos,(0,1),"empty") and Look(board,pos,(0,2),"empty"): # king castle
                    moves.append((pos,(pos[0],pos[1]+2),"kingCastle"))
                if "q" in Castles and Look(board,pos,(0,-1),"empty") and Look(board,pos,(0,-2),"empty") and Look(board,pos,(0,-3),"empty"): # king castle
                    moves.append((pos,(pos[0],pos[1]-2),"queenCastle"))                
        case "n":                                                                                         # KNIGHTS
            if Look(board,pos,(-2,-1),"empty") or Look(board,pos,(-2,-1),OppColor): # knight up left
                moves.append((pos,(pos[0]-2,pos[1]-1),"normal"))
            if Look(board,pos,(-2,1),"empty") or Look(board,pos,(-2,1),OppColor): # knight up right
                moves.append((pos,(pos[0]-2,pos[1]+1),"normal"))
            if Look(board,pos,(-1,2),"empty") or Look(board,pos,(-1,2),OppColor): # knight right up
                moves.append((pos,(pos[0]-1,pos[1]+2),"normal"))
            if Look(board,pos,(1,2),"empty") or Look(board,pos,(1,2),OppColor): # knight right down
                moves.append((pos,(pos[0]+1,pos[1]+2),"normal"))
            if Look(board,pos,(2,1),"empty") or Look(board,pos,(2,1),OppColor): # knight down right
                moves.append((pos,(pos[0]+2,pos[1]+1),"normal"))
            if Look(board,pos,(2,-1),"empty") or Look(board,pos,(2,-1),OppColor): # knight down left
                moves.append((pos,(pos[0]+2,pos[1]-1),"normal"))
            if Look(board,pos,(1,-2),"empty") or Look(board,pos,(1,-2),OppColor): # knight left down
                moves.append((pos,(pos[0]+1,pos[1]-2),"normal"))
            if Look(board,pos,(-1,-2),"empty") or Look(board,pos,(-1,-2),OppColor): # knight left up
                moves.append((pos,(pos[0]-1,pos[1]-2),"normal"))
        case "r":                                                                                         # ROOKS
            y = -1 # rook up
            while pos[0]+y >= 0:
                if Look(board, pos, (y,0), "empty"):
                    moves.append((pos,(pos[0]+y,pos[1]),"normal"))
                elif Look(board, pos, (y,0), OppColor):
                    moves.append((pos,(pos[0]+y,pos[1]),"normal"))
                    break
                else:
                    break
                y-=1
            x = 1 # rook right
            while pos[1]+x <= 7:
                if Look(board, pos, (0,x), "empty"):
                    moves.append((pos,(pos[0],pos[1]+x),"normal"))
                elif Look(board, pos, (0,x), OppColor):
                    moves.append((pos,(pos[0],pos[1]+x),"normal"))
                    break
                else:
                    break
                x+=1            
            y = 1 # rook down
            while pos[0]+y <= 7:
                if Look(board, pos, (y,0), "empty"):
                    moves.append((pos,(pos[0]+y,pos[1]),"normal"))
                elif Look(board, pos, (y,0), OppColor):
                    moves.append((pos,(pos[0]+y,pos[1]),"normal"))
                    break
                else:
                    break
                y+=1
            x = -1 # rook left
            while pos[1]+x >= 0:
                if Look(board, pos, (0,x), "empty"):
                    moves.append((pos,(pos[0],pos[1]+x),"normal"))
                elif Look(board, pos, (0,x), OppColor):
                    moves.append((pos,(pos[0],pos[1]+x),"normal"))
                    break
                else:
                    break
                x-=1
        case "b":                                                                                   # BISHOPS
            y = -1 # bishop up left
            while pos[0]+y >= 0 and pos[1]+y >= 0:
                if Look(board, pos, (y,y), "empty"):
                    moves.append((pos,(pos[0]+y,pos[1]+y),"normal"))
                elif Look(board, pos, (y,y), OppColor):
                    moves.append((pos,(pos[0]+y,pos[1]+y),"normal"))
                    break
                else:
                    break
                y-=1
            y = -1 # bishop up right
            while pos[0]+y >= 0 and pos[1]-y <= 7:
                if Look(board, pos, (y,-1*y), "empty"):
                    moves.append((pos,(pos[0]+y,pos[1]-y),"normal"))
                elif Look(board, pos, (y,-1*y), OppColor):
                    moves.append((pos,(pos[0]+y,pos[1]-y),"normal"))
                    break
                else:
                    break
                y-=1
            y = 1 # bishop down right
            while pos[0]+y <= 7 and pos[1]+y <= 7:
                if Look(board, pos, (y,y), "empty"):
                    moves.append((pos,(pos[0]+y,pos[1]+y),"normal"))
                elif Look(board, pos, (y,y), OppColor):
                    moves.append((pos,(pos[0]+y,pos[1]+y),"normal"))
                    break
                else:
                    break
                y+=1
            y = 1 # bishop down left
            while pos[0]+y <= 7 and pos[1]-y >= 0:
                if Look(board, pos, (y,-1*y), "empty"):
                    moves.append((pos,(pos[0]+y,pos[1]-y),"normal"))
                elif Look(board, pos, (y,-1*y), OppColor):
                    moves.append((pos,(pos[0]+y,pos[1]-y),"normal"))
                    break
                else:
                    break
                y+=1
        case "q":                                                                                   # QUEENS
            y = -1 # queen up
            while pos[0]+y >= 0:
                if Look(board, pos, (y,0), "empty"):
                    moves.append((pos,(pos[0]+y,pos[1]),"normal"))
                elif Look(board, pos, (y,0), OppColor):
                    moves.append((pos,(pos[0]+y,pos[1]),"normal"))
                    break
                else:
                    break
                y-=1
            x = 1 # queen right
            while pos[1]+x <= 7:
                if Look(board, pos, (0,x), "empty"):
                    moves.append((pos,(pos[0],pos[1]+x),"normal"))
                elif Look(board, pos, (0,x), OppColor):
                    moves.append((pos,(pos[0],pos[1]+x),"normal"))
                    break
                else:
                    break
                x+=1            
            y = 1 # queen down
            while pos[0]+y <= 7:
                if Look(board, pos, (y,0), "empty"):
                    moves.append((pos,(pos[0]+y,pos[1]),"normal"))
                elif Look(board, pos, (y,0), OppColor):
                    moves.append((pos,(pos[0]+y,pos[1]),"normal"))
                    break
                else:
                    break
                y+=1
            x = -1 # queen left
            while pos[1]+x >= 0:
                if Look(board, pos, (0,x), "empty"):
                    moves.append((pos,(pos[0],pos[1]+x),"normal"))
                elif Look(board, pos, (0,x), OppColor):
                    moves.append((pos,(pos[0],pos[1]+x),"normal"))
                    break
                else:
                    break
                x-=1
            y = -1 # queen up left
            while pos[0]+y >= 0 and pos[1]+y >= 0:
                if Look(board, pos, (y,y), "empty"):
                    moves.append((pos,(pos[0]+y,pos[1]+y),"normal"))
                elif Look(board, pos, (y,y), OppColor):
                    moves.append((pos,(pos[0]+y,pos[1]+y),"normal"))
                    break
                else:
                    break
                y-=1
            y = -1 # queen up right
            while pos[0]+y >= 0 and pos[1]-y <= 7:
                if Look(board, pos, (y,-1*y), "empty"):
                    moves.append((pos,(pos[0]+y,pos[1]-y),"normal"))
                elif Look(board, pos, (y,-1*y), OppColor):
                    moves.append((pos,(pos[0]+y,pos[1]-y),"normal"))
                    break
                else:
                    break
                y-=1
            y = 1 # queen down right
            while pos[0]+y <= 7 and pos[1]+y <= 7:
                if Look(board, pos, (y,y), "empty"):
                    moves.append((pos,(pos[0]+y,pos[1]+y),"normal"))
                elif Look(board, pos, (y,y), OppColor):
                    moves.append((pos,(pos[0]+y,pos[1]+y),"normal"))
                    break
                else:
                    break
                y+=1
            y = 1 # queen down left
            while pos[0]+y <= 7 and pos[1]-y >= 0:
                if Look(board, pos, (y,-1*y), "empty"):
                    moves.append((pos,(pos[0]+y,pos[1]-y),"normal"))
                elif Look(board, pos, (y,-1*y), OppColor):
                    moves.append((pos,(pos[0]+y,pos[1]-y),"normal"))
                    break
                else:
                    break
                y+=1
    for move in moves:
        BoardAfter = MakeMove(board, move[0], copy.deepcopy(move[1]), copy.deepcopy(move[2]))
        CurrentState[3] = copy.deepcopy(EnPassant)
        CurrentState[2] = copy.deepcopy(Castles)
        KingPos = FindKing(BoardAfter, Color)
        if IsKingSafe(BoardAfter,KingPos,OppColor):

            validmoves.append((GetBoardScore(BoardAfter),move))
    return(validmoves)   
            
def PrintBoard(board):
    print("")
    for rank in range(len(board)):
        rankstr = ""
        for piece in range(len(board[rank])):
            match board[rank][piece]:
                case "0":
                    if rank%2 == 0:
                        if piece%2 == 0:
                            rankstr+="▭▭" #▭▭ ▬▬ ▥▥ ▯▯
                        else:
                            rankstr+="▥▥"
                    else:
                        if piece%2 != 0:
                            rankstr+="▭▭" #▭▭ ▬▬ ▥▥ ▯▯
                        else:
                            rankstr+="▥▥"
                case "K":
                    rankstr+="♔"
                case "Q":
                    rankstr+="♕"
                case "P":
                    rankstr+="♙"
                case "R":
                    rankstr+="♖"
                case "B":
                    rankstr+="♗"
                case "N":
                    rankstr+="♘"
                case "k":
                    rankstr+="♚"
                case "q":
                    rankstr+="♛"
                case "p":
                    rankstr+="♟"
                case "r":
                    rankstr+="♜"
                case "b":
                    rankstr+="♝"
                case "n":
                    rankstr+="♞"
        print(rankstr, rank)

def SortByScore(moves, color):
    Moves = copy.deepcopy(moves)
    deleted = []
    if color == "white":
        Moves.sort(reverse = True)
        for move in range(len(Moves)):
            best = Moves[0][0]
            if Moves[move][0] < best:
                deleted.append(move)
    else:
        Moves.sort()
        best = Moves[0][0]
        for move in range(len(Moves)):
            if Moves[move][0] > best:
                deleted.append(move)
    deleted.sort(reverse = True)
    for move in deleted:
        Moves.pop(move)

    return(Moves)


                
def MakeRandomValid(Board, EnPassant, Castles, Color):
    Moves = []
    for rank in range(len(Board)):
        for file in range(len(Board[rank])):
            if Board[rank][file] != "0" and Board[rank][file].isupper() == (Color == "white"):
                Moves.extend(ValidMoves(Board, (rank,file), EnPassant, Castles))
    Moves = SortByScore(Moves, Color)
    move = random.choice(Moves)
    return(MakeMove(Board, move[1][0], move[1][1], move[1][2]))
    
StartPos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

def NewGame():  # CONFIG              THERE IS AN ERROR WHERE THE ENEMY KING DOESNT DETECT SAFE MOVES CORRECTLY AND PUTS HIMSELF IN CHECK
    global CurrentState
    CurrentState = FromFEN(StartPos)
    Board = CurrentState[0]

#    Board = MakeMove(Board, (6,4), (4,4), "normal") # Pawn to e4
#    Board = MakeRandomValid(Board,CurrentState[2], CurrentState[3], False)
    PrintBoard(Board)

NewGame()
running = True
while running:
    start = input("What piece do you want to move?")
    end = input("Where do you want to move it?")
    special = input("normal/enPassant/kingCastle/queenCastle/prom_queen/prom_rook/prom_bishop/prom_knight")
    if special == "":
        special = "normal"
    try:
        start = eval("["+start+"]")
        start.reverse()
        end = eval("["+end+"]")
        end.reverse()
        start = tuple(start)
        end = tuple(end)
        print(start, end)
        if (start, end, special) in map(lambda a : a[1],ValidMoves(CurrentState[0], start, copy.deepcopy(CurrentState[3]), copy.deepcopy(CurrentState[2]))): 
            CurrentState[0] = MakeMove(CurrentState[0], start, end, special)
            PrintBoard(CurrentState[0])
            CurrentState[0] = MakeRandomValid(CurrentState[0],copy.deepcopy(CurrentState[3]), copy.deepcopy(CurrentState[2]), "black")
            PrintBoard(CurrentState[0])
        else:
            print("Invalid move!")
            PrintBoard(CurrentState[0])
            valids = ValidMoves(CurrentState[0], start, copy.deepcopy(CurrentState[3]), copy.deepcopy(CurrentState[2]))
            valids = [row[1:] for row in valids]
            print("These are all the valid moves for the piece you tried moving:")
            print(valids)
    except:
        print("Invalid input! (Move format should be 'x,y'. For ex: 4,7 is the black king)")
        PrintBoard(CurrentState[0])      

# [2,2,2,2,2,2,2,2]
# [1,1,1,1,1,1,1,1]
# [0,0,0,0,0,0,0,0]
# [0,0,0,0,0,0,0,0]
# [0,0,0,0,0,0,0,0]
# [0,0,0,0,0,0,0,0]
# [1,1,1,1,1,1,1,1]
# [2,2,2,2,2,2,2,2]
