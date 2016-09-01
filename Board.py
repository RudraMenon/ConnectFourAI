import copy
class Board():
    def __init__(self):
         self.board = [
                        [0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0]]
         """
         self.board = [[1, 2, 3, 4, 5, 6, 7],
                      [11, 12, 13, 14, 15, 26, 17],
                      [21, 22, 23, 24, 25, 36, 27],
                      [31, 32, 33, 34, 35, 46, 37],
                      [41, 42, 43, 44, 45, 46, 47],
                      [51, 52, 53, 54, 55, 56, 57],
                      [61, 62, 63, 64, 65, 66, 67],
                      [71, 72, 73, 74, 75, 76, 77]]"""

         self.size = 7

    def dropPlayerToken(self, player, col):
        for slotNum in range(self.size):
            slot = self.board[col][slotNum]
            if self.board[col][0] == 0:
                if slot != 0:
                    self.board[col][slotNum-1] = player
                    return [col, slotNum]
        self.board[col][6] = player
        return [col,6]

    def contains(self, player, big, length=4):
        fourInARow = [player]*length
        for i in xrange(len(big) - len(fourInARow) + 1):
            for j in xrange(len(fourInARow)):
                if big[i + j] != fourInARow[j]:
                    break
            else:
                return True
        return False

    def checkWinHorizontal(self, player):
        for rowNum in range(self.size):
            row = [self.board[colNum][rowNum] for colNum in range(self.size)]
            if self.contains(player, row):
                return True

        return False

    def checkWinVertical(self, player):
        for col in self.board:
            if self.contains(player, col) != False:
                return True
        return False

    def checkDiag(self, player):
        for diagColNum in range(8):
            diagColNum += 3
            offset = 0
            diagRow1 = []
            diagRow2 = []
            for diagRowNum in range(self.size):
                if diagColNum - offset >= 0:
                    try:
                        diagRow1.append(self.board[diagColNum-offset][diagRowNum])
                        diagRow2.append(self.board[diagColNum-offset][6-diagRowNum])
                    except:
                        pass
                offset += 1
                if self.contains(player,diagRow1) or self.contains(player,diagRow2):
                    return True

        return False



    def checkWin(self):
        for player in [1,2]:
            if self.checkWinHorizontal(player) or self.checkWinVertical(player)\
                    or self.checkDiag(player):
                return player
        return False

    def copyBoard(self, board):
        self.board = copy.deepcopy(board.board)

    def prtBoard(self):

        for rowNum in range(self.size):
            row =  [self.board[colNum][rowNum] for colNum in range(self.size)]
            print row
            """for slotNum,slot in enumerate(row):
                print rowNum, slotNum
                if slot == 1:
                    fill_circle(slotNum*50 + 25,rowNum*50 + 25,25,'red')
                elif slot == 2:
                    fill_circle(slotNum*50 + 25,rowNum*50 + 25,25,'blue')"""



    def getAllLowest(self):
        lowest = [6,6,6,6,6,6,6]
        for colNum in range(self.size):
            for rowNum in range(self.size):
                slot = self.board[colNum][rowNum]
                if slot != 0 and lowest[colNum] == 6:
                    lowest[colNum] = rowNum - 1
        return lowest

    def isFull(self):
        return self.getAllLowest() == [-1, -1, -1, -1, -1, -1, -1]

    def setBoard(self, matrix):
        self.board = matrix

