import random

pieceScore = {'K':0,'Q':9,'R':5,'B':3,'N':3,'p':1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3

def findRandomMove(validMoves):
    move = random.randint(0,len(validMoves)-1)
    return validMoves[move]

def findBestMoves(gs,validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    bestScore = CHECKMATE
    bestMove = None

    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        random.shuffle(opponentsMoves)

        if gs.checkMate:
            opponentBestScore = -CHECKMATE
        elif gs.staleMate:
            opponentBestScore = STALEMATE
        else:
            # Assume opponent plays best move
            opponentBestScore = -CHECKMATE
            for opponentMove in opponentsMoves:
                gs.makeMove(opponentMove)
                gs.getValidMoves()
                if gs.checkMate:
                    currScore = CHECKMATE
                elif gs.staleMate:
                    currScore = STALEMATE
                else:
                    currScore = -turnMultiplier * scoreMaterial(gs.board)
                if currScore > opponentBestScore:
                    opponentBestScore = currScore
                gs.undoMove()
            score = opponentBestScore

        if opponentBestScore < bestScore:
            bestScore = opponentBestScore
            bestMove = playerMove

        gs.undoMove()

    return bestMove


def findBestMoveMinMax(gs,validMoves):
    global bestMove
    bestMove = None

    #findMoveMinMaxRecursively(gs,validMoves,DEPTH,gs.whiteToMove)
    #findMoveNegaMax(gs,validMoves,DEPTH,1 if gs.whiteToMove else -1)
    findMoveNegaMaxAlphaBeta(gs,validMoves,DEPTH,-CHECKMATE,CHECKMATE,1 if gs.whiteToMove else -1)


    return bestMove

def findMoveMinMaxRecursively(gs,validMoves,depth,whiteToMove):
    global bestMove

    if depth == 0:
        return scoreMaterial(gs.board)
    
    if whiteToMove:
        maxScore = -CHECKMATE
    else :
        minScore = CHECKMATE

    random.shuffle(validMoves)

    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()

        if gs.checkMate:
            score = CHECKMATE if whiteToMove else -CHECKMATE
        elif gs.staleMate:
            score = STALEMATE 
        else:
            score = findMoveMinMaxRecursively(gs,nextMoves,depth - 1,not whiteToMove)

        if whiteToMove:
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    bestMove = move

        else:            
            if score < minScore:
                minScore =score
                if depth == DEPTH:
                    bestMove = move

        gs.undoMove()

    
    return maxScore if whiteToMove else minScore

def findMoveNegaMax(gs,validMoves,depth,whiteToMove):
    global bestMove

    if depth == 0:
        return whiteToMove*scoreBoard(gs)
    
    maxScore = -CHECKMATE

    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs,nextMoves,depth-1,-whiteToMove)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                bestMove = move
        gs.undoMove()

    return maxScore

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, whiteToMove):
    global bestMove

    if depth == 0:
        return whiteToMove*scoreBoard(gs)
    
    random.shuffle(validMoves)
    
    maxScore = -CHECKMATE

    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs,nextMoves,depth-1,-beta,-alpha,-whiteToMove)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                bestMove = move
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore

        if alpha >= beta:
            break

    return maxScore


def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE
        
        else:
            return CHECKMATE
        
    if gs.staleMate:
        return STALEMATE
    
    return scoreMaterial(gs.board)



def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]

            elif square[0] == 'b':
                score-=pieceScore[square[1]]

    return score
