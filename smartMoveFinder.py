import random

def findRandomMove(validMoves):
    move = random.randint(0,len(validMoves)-1)
    return validMoves[move]


