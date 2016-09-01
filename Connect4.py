from Board import Board
import random

board = Board()
def getLengthInARow(player, big, length=4):
    lengthInARow = []
    for i in range(len(big)):
        slot = big[i]
        if slot == player:
            lengthInARow.append(i)
        else:
            lengthInARow = []
        if len(lengthInARow) >= length:
            return lengthInARow
    return []

def makesARow(player, big, center, length=4):
    lenghInARow = getLengthInARow(player, big, length)
    return center in lenghInARow

def getOpp(player):
    if player == 1:
        return 2
    return 1

def getThreat(currBoard, player):
    opp = getOpp(player)
    allLines = getAllLines()
    lowest = currBoard.getAllLowest()
    threats = []
    for coordList in allLines:
        line = [currBoard.board[x][y] for x,y in coordList]
        lengthInRow = getLengthInARow(opp,line,3)
        if lengthInRow != []:

            leftEnd, rightEnd = lengthInRow[0] - 1, lengthInRow[-1] + 1
            if leftEnd >= 0:
                coordX, coordY = coordList[leftEnd]
                if coordY == lowest[coordX]:
                    threats.append(coordList[leftEnd])

            if rightEnd <= 6 and rightEnd < len(coordList):
                coordX, coordY = coordList[rightEnd]
                if coordY == lowest[coordX]:
                    threats.append(coordList[rightEnd])
    return threats




def getAllLines():
    allLines = []
    allLines = allLines + getGridLines()
    allLines = allLines + getDiagLines()
    return allLines


def getGridLines ():
    lines = [[(colNum,rowNum) for rowNum in range(7)] for colNum in range(7)]
    lines = lines + [[(colNum,rowNum) for colNum in range(7)] for rowNum in range(7)]
    return lines


def getDiagLines():
    diags = []
    for diagColNum in range(8):
        diagColNum += 3
        offset = 0
        diagRow1 = []
        diagRow2 = []
        for diagRowNum in range(7):
            if diagColNum - offset >= 0:
                if 0 <= diagColNum - offset <= 6 and 0 <= diagRowNum <= 6:
                    diagRow1.append((diagColNum - offset,diagRowNum))
                if 0 <= diagColNum - offset <=6 and 0 <= 6-diagRowNum <= 6:
                    diagRow2.append((diagColNum - offset,6 - diagRowNum))
            offset += 1
        diags.append(diagRow1)
        diags.append(diagRow2)
    return diags

def getInfluenceLines(currBoard ,coord):
    x,y = coord
    row = [currBoard.board[colNum][y] for colNum in range(currBoard.size)]
    col = currBoard.board[x]
    diagColNum1 = x + y
    diagColNum2 = x - y
    diagRow1 = []
    diagRow2 = []
    offset = 0
    for diagRowNum in range(currBoard.size):
        if 0 <= diagColNum1 - offset <= 6 and 0 <= diagRowNum <= 6:
            diagRow1.append(currBoard.board[diagColNum1 - offset][diagRowNum])
        if 0 <= diagColNum2 + offset <= 6 and 0 <= diagRowNum <= 6:
            diagRow2.append(currBoard.board[diagColNum2 + offset][diagRowNum])
        offset += 1
    return row,col,diagRow1,diagRow2

def checkInRow(player, currBoard ,coord, length):
    x,y = coord
    row,col,diagRow1,diagRow2 =  getInfluenceLines(currBoard,coord)

    return (makesARow(player, col, y, length)
            or makesARow(player, row, x, length)
            or makesARow(player, diagRow1, x, length)
            or makesARow(player, diagRow2, x, length))

def ifEmpty(currBoard):
    return currBoard.board == [[0,0,0,0,0,0,0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0]]



moves = [0,0,0,0,0,0,0]
newBoard = Board()
newBoard.copyBoard(board)
depth = 3



defaultMultipliers = [18, 900, 19000, 450]

def getMinMax(severity, checkDepth, player, multipliers = defaultMultipliers):
    if player == myNumber:
        plusOrMinus = 1
    else:
        plusOrMinus = -1
    if severity == 1 and checkDepth == depth:
        return 10000000000000
    return plusOrMinus * (checkDepth* multipliers[0]) * [multipliers[1],multipliers[2],multipliers[3]][severity]


def getBestMove (player, currDepth = depth, testBoard=board, baseMove = 0):
    global moves
    multipliers = getMultiplier(player)
    if ifEmpty(testBoard):
        moves = [0,0,0,10,0,0,0]
        return
    if currDepth > 0:
        for option in range(len(moves)):
            lowest = testBoard.getAllLowest()
            if lowest[option] != -1:
                if currDepth == depth:
                    baseMove = option
                copyBoard = Board()
                copyBoard.copyBoard(testBoard)
                threat = getThreat(copyBoard, player)
                if threat != []:
                    if len(threat) < 1:
                        option = threat[0][0]
                x,y = copyBoard.dropPlayerToken(player, option)
                threat = getThreat(copyBoard, player)
                if threat != []:
                    if len(threat) > 1:
                        moves[baseMove] -= getMinMax(1,currDepth,player, multipliers)
                    else:
                        moves[baseMove] -= getMinMax(1,currDepth,player, multipliers)
                if checkInRow(player, copyBoard, [x,y], 4):
                    moves[baseMove] += getMinMax(1,currDepth,player, multipliers)
                    #print 'can win', depth, option, getMinMax(1, currDepth, player, multipliers)
                    if depth >= 3:

#                        print option
                        return option
                elif checkInRow(player, copyBoard, [x,y], 3):
                    moves[baseMove] += getMinMax(0,currDepth,player, multipliers)
                elif checkInRow(player, copyBoard, [x,y], 2):
                    moves[baseMove] += getMinMax(2,currDepth,player, multipliers)


                getBestMove(getOpp(player), currDepth - 1, copyBoard, baseMove)

        for i, x in enumerate(moves):
            if board.getAllLowest()[i] == -1:
                moves[i] = min(moves) - 1
        indices = [i for i, x in enumerate(moves) if x == max(moves)]
        return random.choice(indices)


def CVC():
    global myNumber, moves
    board.__init__()

    while not board.checkWin() and not board.isFull():
        moves = [0,0,0,0,0,0,0]
        getBestMove(myNumber)
        for i,x in enumerate(moves):
            if board.getAllLowest()[i] == -1:
                moves[i] = min(moves)-1

        indices = [i for i, x in enumerate(moves) if x == max(moves)]
        whichSlot = indices[0]
        board.dropPlayerToken(myNumber,whichSlot)
        myNumber = getOpp(myNumber)
    if board.checkWin() == 1:
        #print 'player 1 wins'
        return 1

    elif board.checkWin() == 2:
        print 'player 2 wins'
        return 2
    else:
        print 'tie'
        return 0


def resetMoves():
    global moves
    moves = [0,0,0,0,0,0,0]

myNumber = 1
def PVC():
    global myNumber, moves
    board.__init__()
    player = 2
    for iterate in range(1):
        while not board.checkWin() and not board.isFull():
            board.prtBoard()
            playerMove = int(raw_input('Enter A Slot: '))
            board.dropPlayerToken(player, playerMove)
            player = getOpp(player)
            resetMoves()
            computerMove = getBestMove(player, testBoard=board)
            print moves, computerMove
            board.dropPlayerToken(player, computerMove)
            player = getOpp(player)
        board.prtBoard()
        if board.checkWin() == 1:
            return 1

        elif board.checkWin() == 2:
            return 2
        else:
            print 'tie'
        print iterate
        board.__init__()



maxMultiplier = [20,1000,20000,500]
player1Multipliers, player2Multipliers = [],[]
player1Multipliers, player2Multipliers = [],[]

def getMultiplier(player):
    #print player2Multipliers
    if player == 1:
        if player1Multipliers != []:
            return player1Multipliers
    if player2Multipliers != []:
        return player2Multipliers
    return defaultMultipliers


def main():
    global player1Multipliers, player2Multipliers, defaultMultipliers
    for a in range(4, maxMultiplier[0], 2):
        for b in range(400, maxMultiplier[1], 100):
            for c in range(5000, maxMultiplier[2], 1000):
                for d in range(400, maxMultiplier[3], 50):
                    newMultiplier =  [a,b,c,d]
                    player1Multipliers = defaultMultipliers
                    player2Multipliers = newMultiplier
                    result = CVC()
                    print defaultMultipliers, player2Multipliers, result
                    #print ('testing: ', player2Multipliers)
                    if result == 2:
                        print '-----------------', newMultiplier, 'beat', defaultMultipliers
                        defaultMultipliers = newMultiplier



board.setBoard([
                        [0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0],
                        [0,0,0,0,2,2,2],
                        [0,0,0,0,1,1,1],
                        [0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0]])
print moves
print getBestMove(1, testBoard=board)
PVC()