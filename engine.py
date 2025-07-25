# responsible for move by computer 

class Gamestate():
    def __init__(self):
        self.board=[
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]

        # self.board=[
        #     ["--","--","--","bQ","wB","--","--","bR"],
        #     ["--","--","--","--","bK","--","--","--"],
        #     ["--","--","--","--","--","--","--","--"],
        #     ["--","--","--","--","--","--","--","--"],
        #     ["--","--","--","--","bp","--","--","--"],
        #     ["--","--","--","--","wQ","--","--","--"],
        #     ["wp","wp","wp","wp","wp","wp","wp","wp"],
        #     ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        # ]

        self.moveFunctions = {'p':self.getPawnMoves,'R':self.getRookMoves,'N':self.getKnightMoves,'B':self.getBishopMoves,'Q':self.getQueenMoves,'K':self.getKingMoves}

        self.whiteToMove=True
        self.moveLog=[]
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.checkMate = False
        self.staleMate = False
        self.incheck = False
        self.pins = []
        self.checks = []
        self.enpassantPossible = ()
        self.enpassantPossibleLog = [self.enpassantPossible]
        self.currentCastlingRight = CastleRights(True,True,True,True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wks,self.currentCastlingRight.bks,self.currentCastlingRight.wqs,self.currentCastlingRight.bqs)]

    def makeMove(self,move):
        self.board[move.startRow][move.startCol]="--"
        self.board[move.endRow][move.endCol]=move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove= not self.whiteToMove
        #if king is moved

        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow,move.endCol)

        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow,move.endCol)

        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol]=move.pieceMoved[0]+'Q'

        if move.isEnpassantMove :
            self.board[move.startRow][move.endCol] =  "--"

        if move.pieceMoved[1] == 'p' and abs(move.startRow-move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow)//2 , move.startCol)
        else:
            self.enpassantPossible = ()

        self.enpassantPossibleLog.append(self.enpassantPossible)

        if move.isCastleMove:
            if move.endCol - move.startCol == 2:
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1] = '--'
            else:
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2] = '--'

        self.updateCastleRights(move)

        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks,self.currentCastlingRight.bks,self.currentCastlingRight.wqs,self.currentCastlingRight.bqs))


    def undoMove(self):
        if len(self.moveLog)!=0:
            move=self.moveLog.pop()
            self.board[move.startRow][move.startCol]=move.pieceMoved
            self.board[move.endRow][move.endCol]=move.pieceCaptured
            self.whiteToMove= not self.whiteToMove

        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.startRow,move.startCol)

        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.startRow,move.startCol)

        if move.isEnpassantMove:
            self.board[move.endRow][move.endCol]="--"
            self.board[move.startRow][move.endCol]=move.pieceCaptured
            #self.enpassantPossible = (move.endRow,move.endCol)

        # if move.pieceMoved[1] == 'p' and abs(move.startRow-move.endRow) == 2:
        #     self.enpassantPossible = ()

        self.enpassantPossibleLog.pop()
        self.enpassantPossible = self.enpassantPossibleLog[-1]

        self.castleRightsLog.pop()
        castleRights = self.castleRightsLog[-1]

        self.currentCastlingRight.bks = castleRights.bks
        self.currentCastlingRight.bqs = castleRights.bqs
        self.currentCastlingRight.wks = castleRights.wks
        self.currentCastlingRight.wqs = castleRights.wqs

        if move.isCastleMove:
            if move.endCol - move.startCol == 2:
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                self.board[move.endRow][move.endCol-1] = '--'
            else:
                self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1] = '--'

        self.checkMate = False
        self.staleMate = False


    
    def updateCastleRights(self,move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False

        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False

        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRight.wqs = False

                elif move.startCol == 7:
                    self.currentCastlingRight.wks = False

        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRight.bqs = False

                elif move.startCol == 7:
                    self.currentCastlingRight.bks = False

    # def getValidMoves(self):
    #     moves = self.getAllPossibleMoves()

    #     for i in range(len(moves)-1,-1,-1):
    #         self.makeMove(moves[i])
    #         self.whiteToMove= not self.whiteToMove
    #         if self.inCheck():
    #             moves.remove(moves[i])
    #         self.whiteToMove= not self.whiteToMove
    #         self.undoMove()

    #     if len(moves) == 0:
    #         if self.inCheck():
    #             self.checkMate = True
    #         else:
    #             self.staleMate = True

    #     else:
    #         self.checkMate = False
    #         self.staleMate = False

    #     return moves
    
    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        moves = []
        self.incheck,self.pins,self.checks = self.checkForPinsAndChecks()

        tempCastleRights = CastleRights(self.currentCastlingRight.wks,self.currentCastlingRight.bks,self.currentCastlingRight.wqs,self.currentCastlingRight.bqs)

        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]

        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]

        if self.incheck:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                print(check)
                checkRow = check[0]
                checkCol = check[1]

                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []

                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow,checkCol)]

                else:
                    for i in range(1,8):
                        validSquare = (kingRow + check[2]*i,kingCol + check[3]*i)
                        validSquares.append(validSquare)

                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break

                for i in range(len(moves)-1,-1,-1):

                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow,moves[i].endCol) in validSquares:
                            moves.remove(moves[i])

                

            else:
                self.getKingMoves(kingRow,kingCol,moves)

        else:
            moves = self.getAllPossibleMoves()

        self.enpassantPossible = tempEnpassantPossible

        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0],self.whiteKingLocation[1],moves)

        else:
            self.getCastleMoves(self.blackKingLocation[0],self.blackKingLocation[1],moves)

        self.currentCastlingRight = tempCastleRights

        #check for the flags of checkmate and stalemate
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True

        else:
            self.checkMate = False
            self.staleMate = False

        return moves
    
    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        incheck = False

        if self.whiteToMove:
            enemyColor = 'b'
            allycolor = 'w'
            startRow = self.whiteKingLocation[0]
            startcol = self.whiteKingLocation[1]

        else:
            enemyColor = 'w'
            allycolor = 'b'
            startRow = self.blackKingLocation[0]
            startcol = self.blackKingLocation[1]

        directions = ((-1 ,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1))

        for j in range(len(directions)):
            d=directions[j]
            possiblePin = ()

            for i in range(1,8):
                endRow = startRow + d[0]*i
                endCol = startcol + d[1]*i

                if 0<= endRow <8 and 0<= endCol <8:  
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allycolor:
                        if possiblePin == ():
                            possiblePin = (endRow,endCol,d[0],d[1])
                        else:
                            break

                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]

                        if (0<=j<=3 and type == 'R') or \
                            (4<=j<=7 and type == 'B') or \
                            (i==1 and type == 'p' and ((enemyColor == 'w' and 6<=j<=7) or (enemyColor == 'b' and 4<=j<=5))) or \
                            (type == 'Q') or (i==1 and type == 'K'):

                            if possiblePin == ():
                                incheck = True
                                checks.append((endRow,endCol,d[0],d[1]))
                                break

                            else:
                                pins.append(possiblePin)
                                break

                        else:
                            break

                else:
                    break

        
        directions = ((2,-1),(-2,-1),(2,1),(-2,1),(1,2),(1,-2),(-1,2),(-1,-2))

        for d in directions:
            endrow = startRow+d[0]
            endcol = startcol+d[1]

            if 0 <= endrow < 8 and 0 <= endcol < 8 :
                endpiece = self.board[endrow][endcol]

                if endpiece[0] == enemyColor and endpiece[1] == 'N':
                    incheck = True
                    checks.append((endrow,endcol,d[0],d[1]))

        return incheck,pins,checks


            
    
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0],self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0],self.blackKingLocation[1])

    def squareUnderAttack(self,r,c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves(ignoreKing=True)
        self.whiteToMove = not self.whiteToMove

        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
            
        kingRow, kingCol = self.blackKingLocation if self.whiteToMove else self.whiteKingLocation
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                if kingRow + dr == r and kingCol + dc == c:
                    return True

        return False


    def getAllPossibleMoves(self, ignoreKing = False):
        moves=[]

        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn=self.board[r][c][0]

                if (turn=='w' and self.whiteToMove) or (turn=='b' and not self.whiteToMove) :
                    piece=self.board[r][c][1]
                    if ignoreKing and piece == 'K':
                        continue
                    self.moveFunctions[piece](r,c,moves)
        return moves


    def getPawnMoves(self,r,c,moves):
        piecePinned = False
        pinDirection = ()

        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

            
        if self.whiteToMove:
            moveAmount = -1
            startRow = 6
            enemyColor = 'b'
            kingRow ,kingCol = self.whiteKingLocation

        else:
            moveAmount = 1
            startRow = 1
            enemyColor = 'w'
            kingRow ,kingCol = self.blackKingLocation


        if self.whiteToMove:
            if self.board[r-1][c]=='--':
                if not piecePinned or pinDirection == (-1,0):
                    moves.append(Move((r,c),(r-1,c),self.board))

                    if r==6 and self.board[r-2][c]=='--':
                        moves.append(Move((r,c),(r-2,c),self.board))

            if c-1 >=0:
                if self.board[r-1][c-1][0] == 'b':
                    if not piecePinned or pinDirection == (-1,-1):
                        moves.append(Move((r,c),(r-1,c-1),self.board))

                elif (r-1,c-1) == self.enpassantPossible:
                    if not piecePinned or pinDirection == (-1,-1):
                        attackingPiece = blockingPiece = False
                        if kingRow == r:
                            if kingCol < c:
                                insideRange = range(kingCol+1,c-1)
                                outsideRange = range(c+1,8)
                            else:
                                insideRange = range(kingCol-1,c,-1)
                                outsideRange = range(c-2,-1,-1)

                            for i in insideRange:
                                if self.board[r][i] != '--':
                                    blockingPiece = True

                            for i in outsideRange:
                                square = self.board[r][i]
                                if square[0] == enemyColor and (square[1]=='R' or square[1] == 'Q'):
                                    attackingPiece = True

                                elif square != '--':
                                    blockingPiece = True
                        
                        if blockingPiece or not attackingPiece:
                            moves.append(Move((r,c),(r-1,c-1),self.board,isEnpassantMove=True))

            if c+1 <=7:
                if self.board[r-1][c+1][0] == 'b':
                    if not piecePinned or pinDirection == (-1,1):
                        moves.append(Move((r,c),(r-1,c+1),self.board))

                elif (r-1,c+1) == self.enpassantPossible:
                    if not piecePinned or pinDirection == (-1,1):
                        attackingPiece = blockingPiece = False
                        if kingRow == r:
                            if kingCol < c:
                                insideRange = range(kingCol+1,c)
                                outsideRange = range(c+2,8)
                            else:
                                insideRange = range(kingCol-1,c+1,-1)
                                outsideRange = range(c-1,-1,-1)

                            for i in insideRange:
                                if self.board[r][i] != '--':
                                    blockingPiece = True

                            for i in outsideRange:
                                square = self.board[r][i]
                                if square[0] == enemyColor and (square[1]=='R' or square[1] == 'Q'):
                                    attackingPiece = True

                                elif square != '--':
                                    blockingPiece = True
                        
                        if blockingPiece or not attackingPiece:
                            moves.append(Move((r,c),(r-1,c+1),self.board,isEnpassantMove=True))

        else :
            if self.board[r+1][c]=='--':
                if not piecePinned or pinDirection == (1,0):
                    moves.append(Move((r,c),(r+1,c),self.board))

                    if r==1 and self.board[r+2][c]=='--':
                        moves.append(Move((r,c),(r+2,c),self.board))
            #capture
            if c-1 >=0:
                if self.board[r+1][c-1][0] == 'w':
                    if not piecePinned or pinDirection == (1,-1):
                        moves.append(Move((r,c),(r+1,c-1),self.board))

                elif (r+1,c-1) == self.enpassantPossible:
                    if not piecePinned or pinDirection == (1,-1):
                        attackingPiece = blockingPiece = False
                        if kingRow == r:
                            if kingCol < c:
                                insideRange = range(kingCol+1,c-1)
                                outsideRange = range(c+1,8)
                            else:
                                insideRange = range(kingCol-1,c,-1)
                                outsideRange = range(c-2,-1,-1)

                            for i in insideRange:
                                if self.board[r][i] != '--':
                                    blockingPiece = True

                            for i in outsideRange:
                                square = self.board[r][i]
                                if square[0] == enemyColor and (square[1]=='R' or square[1] == 'Q'):
                                    attackingPiece = True

                                elif square != '--':
                                    blockingPiece = True
                        
                        if blockingPiece or not attackingPiece:
                            moves.append(Move((r,c),(r+1,c-1),self.board,isEnpassantMove=True))

            if c+1 <=7:
                if self.board[r+1][c+1][0] == 'w':
                    if not piecePinned or pinDirection == (1,1):
                        moves.append(Move((r,c),(r+1,c+1),self.board))

                elif (r+1,c+1) == self.enpassantPossible:
                    if not piecePinned or pinDirection == (1,1):
                        attackingPiece = blockingPiece = False
                        if kingRow == r:
                            if kingCol < c:
                                insideRange = range(kingCol+1,c)
                                outsideRange = range(c+2,8)
                            else:
                                insideRange = range(kingCol-1,c+1,-1)
                                outsideRange = range(c-1,-1,-1)

                            for i in insideRange:
                                if self.board[r][i] != '--':
                                    blockingPiece = True

                            for i in outsideRange:
                                square = self.board[r][i]
                                if square[0] == enemyColor and (square[1]=='R' or square[1] == 'Q'):
                                    attackingPiece = True

                                elif square != '--':
                                    blockingPiece = True
                        
                        if blockingPiece or not attackingPiece:
                            moves.append(Move((r,c),(r+1,c+1),self.board,isEnpassantMove=True))

    def getRookMoves(self,r,c,moves):
        piecePinned = False
        pinDirection = ()

        i = len(self.pins) - 1
        # print(self.pins)
        while i >= 0:
            # print(i)
            # print('\n')
            pr, pc, pd0, pd1 = self.pins[i]
            if pr == r and pc == c:
                piecePinned = True
                pinDirection = (pd0, pd1)
                # only strip non-queen pins
                if self.board[r][c][1] != 'Q':
                    self.pins.pop(i)
                break
            i -= 1


        directions = ((-1,0),(1,0),(0,-1),(0,1))
        enemycolor = "b" if self.whiteToMove else "w"

        for d in directions:
            for i in range(1,8):
                endrow = r + d[0]*i
                endcol = c + d[1]*i

                if 0 <= endrow < 8 and 0 <= endcol < 8 :
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0],-d[1]):
                        endpiece = self.board[endrow][endcol]

                        if endpiece == "--":
                            moves.append(Move((r,c),(endrow,endcol),self.board))

                        elif endpiece[0] == enemycolor:
                            moves.append(Move((r,c),(endrow,endcol),self.board))
                            break
                            
                        else:
                            break

                else:
                    break

    def getKnightMoves(self,r,c,moves):
        piecePinned = False

        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
        directions = ((2,-1),(-2,-1),(2,1),(-2,1),(1,2),(1,-2),(-1,2),(-1,-2))
        allycolor = "w" if self.whiteToMove else "b"

        for d in directions:
            endrow = r+d[0]
            endcol = c+d[1]

            if 0 <= endrow < 8 and 0 <= endcol < 8 :

                if not piecePinned:
                    endpiece = self.board[endrow][endcol]

                    if endpiece[0] != allycolor:
                        moves.append(Move((r,c),(endrow,endcol),self.board))

    def getBishopMoves(self,r,c,moves):
        piecePinned = False
        pinDirection = ()

        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1,-1),(1,1),(1,-1),(-1,1))
        enemycolor = "b" if self.whiteToMove else "w"

        for d in directions:
            for i in range(1,8):
                endrow = r + d[0]*i
                endcol = c + d[1]*i

                if 0 <= endrow < 8 and 0 <= endcol < 8 :
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0],-d[1]):
                        endpiece = self.board[endrow][endcol]

                        if endpiece == "--":
                            moves.append(Move((r,c),(endrow,endcol),self.board))

                        elif endpiece[0] == enemycolor:
                            moves.append(Move((r,c),(endrow,endcol),self.board))
                            break

                        else:
                            break
                
                else:
                    break

    def getQueenMoves(self,r,c,moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)
    
    def getKingMoves(self,r,c,moves):
        directions = ((1,-1),(0,-1),(-1,-1),(1,1),(0,1),(-1,1),(-1,0),(1,0))
        allycolor = "w" if self.whiteToMove else "b"

        for d in directions:
            endrow = r+d[0]
            endcol = c+d[1]

            if 0 <= endrow < 8 and 0 <= endcol < 8 :
                endpiece = self.board[endrow][endcol]

                if endpiece[0] != allycolor:
                    move = Move((r, c), (endrow, endcol), self.board)
                    self.makeMove(move)
                    self.whiteToMove = not self.whiteToMove
                    in_check = self.inCheck()
                    self.whiteToMove = not self.whiteToMove
                    self.undoMove()
                    if not in_check:
                        moves.append(move)


    def getCastleMoves(self,r,c,moves):
        if self.squareUnderAttack(r,c):
            return
        
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingSideCastleMoves(r,c,moves)

        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueenSideCastleMoves(r,c,moves)

        
    def getKingSideCastleMoves(self,r,c,moves):
        if self.board[r][c+1] == "--" and self.board[r][c+2] == "--" and self.board[r][c+3][1] == "R":
            if not self.squareUnderAttack(r,c+1) and not self.squareUnderAttack(r,c+2):
                moves.append(Move((r,c),(r,c+2),self.board,isCastleMove = True))


    def getQueenSideCastleMoves(self,r,c,moves):
        if self.board[r][c-1] == "--" and self.board[r][c-2] == "--" and self.board[r][c-3] == "--" and self.board[r][c-4][1] == 'R':
            if not self.squareUnderAttack(r,c-1) and not self.squareUnderAttack(r,c-2) and not self.squareUnderAttack(r,c-3):
                moves.append(Move((r,c),(r,c-2),self.board,isCastleMove = True)) 
    # def getPawnMoves(self,r,c,moves):
    #     pass

class CastleRights():
    def __init__(self,wks,bks,wqs,bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
        

class Move():

    ranksToRows={"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rowsToRanks={v:k for k,v in ranksToRows.items()}
    filesToCols={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    colsToFiles={v:k for k,v in filesToCols.items()}

    def __init__(self,startSq,endSq,board, isEnpassantMove = False,isCastleMove = False):
        self.startRow=startSq[0]
        self.startCol=startSq[1]
        self.endRow=endSq[0]
        self.endCol=endSq[1]

        self.pieceMoved=board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        self.isCastleMove = isCastleMove

        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'

        self.isPawnPromotion = False

        if self.pieceMoved == 'wp' and self.endRow == 0:
            self.isPawnPromotion = True

        if self.pieceMoved == 'bp' and self.endRow == 7:
            self.isPawnPromotion = True

        self.moveID=self.startRow*1000+self.startCol*100+self.endRow*10+self.endCol

    def __eq__(self, value):
        if isinstance(value,Move):
            return self.moveID == value.moveID
        return False
    
    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol)+self.getRankFile(self.endRow,self.endCol)

    def getRankFile(self,r,c):
        return self.colsToFiles[c]+self.rowsToRanks[r]