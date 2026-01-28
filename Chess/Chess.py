import copy
Files = ["a","b","c","d","e","f","g","h"]
Ranks = ["8","7","6","5","4","3","2","1"]
# r3k2r/1b1p1ppp/p3p2q/1p2n3/3NPKn1/P5R1/BPP5/RNBQ4 w kq - 10 19
def AlgebraicToCoords(pos):
    return((Ranks.index(pos[1]), Files.index(pos[0])))

def FromFEN(FEN):
    fields = FEN.split(" ")
    boardStr = fields[0].split("/")
    board = []
    EnPassant = ()
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
        EnPassant = (9,9)
    return((board, fields[1], fields[2], EnPassant, fields[4], fields[5]))

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
    if enPassant != (9,9):
        FEN += Files[enPassant[1]] + Ranks[enPassant[0]]
    else:
        FEN += "-"
    return(FEN + " " + halfmove + " " + fullmove)

def MakeMove(board, start, end, special):
    afterBoard = copy.deepcopy(board)
    Color = board[start[0]][start[1]].isupper()
    
    match special:
        case "normal":
            afterBoard[end[0]][end[1]] = board[start[0]][start[1]]
            afterBoard[start[0]][start[1]] = "0"
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
        case "queenCastle":
            afterBoard[end[0]][end[1]] = board[start[0]][start[1]]# Moves the king
            afterBoard[start[0]][start[1]] = "0"
            afterBoard[end[0]][end[1]+1] = board[end[0]][end[1]-2]# Move the rook
            afterBoard[end[0]][end[1]-2] = "0"
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
                return(board[pos[0]+offset[0]][pos[1]+offset[1]] == piece.lower())
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
        y+=1
    return(True)

def FindKing(board, Color):
    if Color == "white":
        for rank in range(len(board)):
            if "K" in board[rank]:
                return((rank, board[rank].index("K")))
    else:
        for rank in range(len(board)):
            if "k" in board[rank]:
                return((rank, board[rank].index("K")))
    
def ValidMoves(board, pos, enPassant, Castles):
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
                if pos[0] == 6 and Look(board,pos,(-2,0),"empty"): # pawn up 2
                    moves.append((pos,(pos[0]-2,pos[1]),"normal"))
                if Look(board,pos,(-1,-1),"black"):                # takes left
                    moves.append((pos,(pos[0]-1,pos[1]-1),"normal"))
                if Look(board,pos,(-1,1),"black"):                 # takes right
                    moves.append((pos,(pos[0]-1,pos[1]+1),"normal"))
                if (pos[0]-1,pos[1]-1) == enPassant:               # en passant left
                    moves.append((pos,(pos[0]-1,pos[1]-1),"enPassant"))
                if (pos[0]-1,pos[1]+1) == enPassant:               # en passant right
                    moves.append((pos,(pos[0]-1,pos[1]+1),"enPassant"))              
                if Look(board,pos,(-1,0),"empty") and pos[0] == 1: # promotions
                    moves.append((pos,(pos[0]-1,pos[1]),"prom_queen"))
                    moves.append((pos,(pos[0]-1,pos[1]),"prom_rook"))
                    moves.append((pos,(pos[0]-1,pos[1]),"prom_bishop"))
                    moves.append((pos,(pos[0]-1,pos[1]),"prom_knight"))
            else: # For black pawns
                if Look(board,pos,(1,0),"empty"):                 # pawn up 1
                    moves.append((pos,(pos[0]+1,pos[1]),"normal"))
                if pos[0] == 1 and Look(board,pos,(2,0),"empty"): # pawn up 2
                    moves.append((pos,(pos[0]+2,pos[1]),"normal"))
                if Look(board,pos,(1,-1),"white"):                # takes left
                    moves.append((pos,(pos[0]+1,pos[1]-1),"normal"))
                if Look(board,pos,(1,1),"white"):                 # takes right
                    moves.append((pos,(pos[0]+1,pos[1]+1),"normal"))
                if (pos[0]+1,pos[1]-1) == enPassant:               # en passant left
                    moves.append((pos,(pos[0]+1,pos[1]-1),"enPassant"))
                if (pos[0]+1,pos[1]+1) == enPassant:               # en passant right
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
            if Look(board,pos,(-1,2),"empty") or Look(board,pos,(-1,2),OppColor): # knight left up
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
        BoardAfter = MakeMove(board, move[0], move[1], move[2])
        KingPos = FindKing(BoardAfter, Color)
        if IsKingSafe(BoardAfter,KingPos,OppColor):

            validmoves.append(move)            
    return(validmoves)   
            
def PrintBoard(board):
    print("")
    for rank in board:
        print(rank)

StartPos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

def NewGame():  # CONFIG
    CurrentState = FromFEN("1n1qk1nr/pppppppp/6b1/r7/3K4/8/PPPPPPPP/RNBQ1BNR w k - 0 1")
    Board = CurrentState[0]

#    Board = MakeMove(Board, (6,4), (4,4), "normal") # Pawn to e4
    PrintBoard(Board)
    print(IsKingSafe(Board, (7,4), "black"))
    print(ValidMoves(Board, (4,3), (9,9), "QKqk"))

NewGame()

# [2,2,2,2,2,2,2,2]
# [1,1,1,1,1,1,1,1]
# [0,0,0,0,0,0,0,0]
# [0,0,0,0,0,0,0,0]
# [0,0,0,0,0,0,0,0]
# [0,0,0,0,0,0,0,0]
# [1,1,1,1,1,1,1,1]
# [2,2,2,2,2,2,2,2]
