#main function

import pygame as p
import engine,smartMoveFinder
from multiprocessing import Process,Queue

BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = 512
DIMENSION = 8
SQ_SIZE=BOARD_HEIGHT//DIMENSION
MAX_FPS=15

IMAGES={}

def loadImages():
    pieces=["bR","bN","bB","bQ","bK","wR","wN","wB","wQ","wK","bp","wp"]

    for piece in pieces:
        IMAGES[piece]=p.transform.scale(p.image.load("pieces/"+piece+".png"),(SQ_SIZE,SQ_SIZE))


def main():
    p.init()
    screen=p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH,BOARD_HEIGHT))
    clock=p.time.Clock()
    screen.fill(p.Color("white"))
    moveLogFont = p.font.SysFont("Helvitca",30,False,False)

    gs=engine.Gamestate()

    validMoves=gs.getValidMoves()
    moveMade=False

    animate =False

    print(gs.board)
    loadImages()
    running=True

    sqSelected=()
    playerClicks=[]

    gameOver = False

    playerOne = True # True for human turn ,color white 
    playerTwo = False # same for black

    AIThinking = False
    moveFinderProcess = None

    moveUndone = False

    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type==p.QUIT:
                running=False

            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE 

                    if sqSelected == (row,col) or col>=8:
                        sqSelected = ()
                        playerClicks=[]
                    else:
                        sqSelected = (row,col)
                        playerClicks.append(sqSelected)

                    if len(playerClicks) == 2 and humanTurn:
                        move=engine.Move(playerClicks[0],playerClicks[1],gs.board)
                        print(move.getChessNotation())


                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade=True
                                animate = True
                                sqSelected = ()
                                playerClicks=[]

                        if not moveMade:
                            playerClicks = [sqSelected]

            elif e.type==p.KEYDOWN :
                if e.key == p.K_z :
                    gs.undoMove()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = True
                    animate = False
                    gameOver = False

                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False

                    moveUndone = True

                if e.key == p.K_r :
                    gs = engine.Gamestate()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False

                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False

                    moveUndone = True

        if not gameOver and not humanTurn and not moveUndone:
            if not AIThinking:
                AIThinking = True
                returnQueue = Queue()
                moveFinderProcess = Process(target=smartMoveFinder.findBestMoveMinMax,args=(gs,validMoves,returnQueue))
                moveFinderProcess.start()
                #AIMove = smartMoveFinder.findBestMoveMinMax(gs,validMoves)
            if not moveFinderProcess.is_alive():
                AIMove = returnQueue.get()
                if AIMove is None:
                    AIMove = smartMoveFinder.findRandomMove(validMoves)
                gs.makeMove(AIMove)
                moveMade = True
                animate = True 
                AIThinking = False

        if moveMade :
            if animate:
                animateMove(gs.moveLog[-1],screen,gs.board,clock)
            validMoves=gs.getValidMoves()
            moveMade=False       
            animate = False 
            moveUndone = False

        drawGameState(screen,gs,validMoves,sqSelected,moveLogFont)

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawEndGameText(screen,'Black Wins By Checkmate !')

            else:
                drawEndGameText(screen,'White Wins By Checkmate !')

        elif gs.staleMate:
            gameOver = True
            if gs.whiteToMove:
                drawEndGameText(screen,'Draw ! White is Stalemate')

            else:
                drawEndGameText(screen,'Draw ! Black is Stalemate')


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


def drawGameState(screen,gs,validMoves,sqSelected,moveLogFont):
    drawBoard(screen)
    highlightSquares(screen,gs,validMoves,sqSelected)
    drawPieces(screen,gs.board)
    drawMoveLog(screen,gs,moveLogFont)


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
            if move.isEnpassantMove:
                enPassantRow = (move.endRow + 1) if move.pieceCaptured[0] == 'b' else (move.endRow - 1)
                endSquare = p.Rect(move.endCol*SQ_SIZE,enPassantRow*SQ_SIZE,SQ_SIZE,SQ_SIZE)

            screen.blit(IMAGES[move.pieceCaptured], endSquare)

        screen.blit(IMAGES[move.pieceMoved],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawMoveLog(screen,gs,font):
    moveLogRect = p.Rect(BOARD_WIDTH,0,MOVE_LOG_PANEL_WIDTH,MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen,p.Color('black'),moveLogRect)
    moveLog = gs.moveLog
    # moveTexts = moveLog
    padding = 5
    textY = padding
    textX = padding
    linespacing = 2
    movesPerRow = 2

    moveTexts = []

    for i in range(0, len(moveLog), 2):
        moveString = str(i//2 + 1) + ". " + moveLog[i].getChessNotation()
        if i + 1 < len(moveLog):
            moveString += " " + moveLog[i+1].getChessNotation()
        moveTexts.append(moveString)

    textY = padding

    for i in range(0,len(moveTexts),movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i+j < len(moveTexts):
                text += moveTexts[i+j] + "   "

        textObject = font.render(text,True,p.Color('White'))
        textLocation = moveLogRect.move(textX,textY)
        textY+=textObject.get_height() + linespacing
        screen.blit(textObject,textLocation)


def drawEndGameText(screen,text):
    font = p.font.SysFont("Helvitca",32,True,False)
    textObject = font.render(text,0,p.Color('Gray'))
    textLocation = p.Rect(0,0,BOARD_WIDTH,BOARD_HEIGHT).move(BOARD_WIDTH/2 - textObject.get_width()/2,BOARD_HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject,textLocation)
    textObject = font.render(text,0,p.Color('Black'))
    screen.blit(textObject,textLocation.move(2,2))

if __name__=="__main__":
    main()