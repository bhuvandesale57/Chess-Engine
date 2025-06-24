#main function

import pygame as p
import engine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE=HEIGHT//DIMENSION
MAX_FPS=15

IMAGES={}

def loadImages():
    pieces=["bR","bN","bB","bQ","bK","wR","wN","wB","wQ","wK","bp","wp"]

    for piece in pieces:
        IMAGES[piece]=p.transform.scale(p.image.load("pieces/"+piece+".png"),(SQ_SIZE,SQ_SIZE))


def main():
    p.init()
    screen=p.display.set_mode((WIDTH,HEIGHT))
    clock=p.time.Clock()
    screen.fill(p.Color("white"))
    gs=engine.Gamestate()

    validMoves=gs.getValidMoves()
    moveMade=False

    print(gs.board)
    loadImages()
    running=True

    sqSelected=()
    playerClicks=[]

    while running:
        for e in p.event.get():
            if e.type==p.QUIT:
                running=False

            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE 

                if sqSelected == (row,col):
                    sqSelected = ()
                    playerClicks=[]
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected)

                if len(playerClicks) == 2:
                    move=engine.Move(playerClicks[0],playerClicks[1],gs.board)
                    print(move.getChessNotation())


                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveMade=True
                            sqSelected = ()
                            playerClicks=[]

                    if not moveMade:
                        playerClicks = [sqSelected]

            elif e.type==p.KEYDOWN :
                if e.key == p.K_z :
                    gs.undoMove()
                    moveMade = True

        if moveMade :
            animateMove(gs.moveLog[-1],screen,gs.board,clock)
            validMoves=gs.getValidMoves()
            moveMade=False       

        drawGameState(screen,gs,validMoves,sqSelected)
        clock.tick(MAX_FPS)
        p.display.flip()


def highlightSquares(screen,gs,validMoves,sqSelected):
    if sqSelected != ():
        r,c =sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100) #transparency from 0 to 255(opaque)
            s.fill(p.Color('blue'))
            screen.blit(s,(c*SQ_SIZE,r*SQ_SIZE))
            s.fill(p.Color('yellow'))

            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s,(move.endCol*SQ_SIZE,move.endRow*SQ_SIZE))


def drawGameState(screen,gs,validMoves,sqSelected):
    drawBoard(screen)
    highlightSquares(screen,gs,validMoves,sqSelected)
    drawPieces(screen,gs.board)


def drawBoard(screen):
    global colors
    colors = [p.Color("white"),p.Color("dark gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen,color,p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))



def drawPieces(screen,board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece=board[r][c]

            if piece!="--":
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

# Animated a move

def animateMove(move,screen,board,clock):
    global colors
    coords = []
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR)+abs(dC))*framesPerSquare

    for frame in range(frameCount+1):
        r,c =(move.startRow + dR*frame/frameCount,move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen,board)
        color = colors[((move.endRow+move.endCol)%2)]
        endSquare = p.Rect(move.endCol*SQ_SIZE,move.endRow*SQ_SIZE,SQ_SIZE,SQ_SIZE)
        p.draw.rect(screen,color,endSquare)

        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)

        screen.blit(IMAGES[move.pieceMoved],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
        p.display.flip()
        clock.tick(60)
    pass




if __name__=="__main__":
    main()