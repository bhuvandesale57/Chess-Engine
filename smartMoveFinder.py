import random

pieceScore = {'K':0,'Q':9,'R':5,'B':3,'N':3,'p':1}
CHECKMATE = 1000
STALEMATE = 0

def findRandomMove(validMoves):
    move = random.randint(0,len(validMoves)-1)
    return validMoves[move]

def findBestMoves(gs,validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    bestScore = CHECKMATE
    bestMove = None

    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        random.shuffle(opponentsMoves)

        if gs.checkMate:
            score = CHECKMATE
        elif gs.staleMate:
            score = STALEMATE
        else:
            # Assume opponent plays best move
            opponentBestScore = CHECKMATE
            for opponentMove in opponentsMoves:
                gs.makeMove(opponentMove)
                if gs.checkMate:
                    currScore = -CHECKMATE
                elif gs.staleMate:
                    currScore = STALEMATE
                else:
                    currScore = -turnMultiplier * scoreMaterial(gs.board)
                if currScore < opponentBestScore:
                    opponentBestScore = currScore
                gs.undoMove()
            score = opponentBestScore

        if score > bestScore:
            bestScore = score
            bestMove = playerMove

        gs.undoMove()

    return bestMove

def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]

            elif square[0] == 'b':
                score-=pieceScore[square[1]]

    return score
