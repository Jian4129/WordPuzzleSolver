'''
Created on Jan 11, 2020

@author: Liang412903
'''
from multiprocessing import Pool, Manager, Queue
import threading
class WordPuzzleSolver:
    def __init__(self, row, column, puzzle):
        self._row = row 
        self._column = column
        self.puzzleList = self.turnToList(self.getRow(), self.getColumn(), puzzle)
    def solve(self, keyword):
        self.keyword = keyword
        self.processQueue = Manager().Queue()
        #create a process for each row
        po = Pool()
        for row in range(len(self.puzzleList)):
            po.apply_async(self.newProcess, (row, self.keyword))
        po.close()
        po.join()
        if(self.processQueue.empty()):
            print("No result find for keyword: %s"%(self.keyword))
        while not self.processQueue.empty():
            result = self.processQueue.get()
            print("%s find in row: %d and column %d in the direction of %s"%(self.keyword, result[0] + 1, result[1] + 1, result[2]))
    #the new process will find the first char of the keyword and pass it's location to new thread
    def newProcess(self, row, keyWord):
        keyChar = keyWord[0]
        for column in range(len(self.puzzleList[row])):
            if keyChar == self.puzzleList[row][column]:
                t = threading.Thread(target= self.newThread, args = (row, column, keyWord))
                t.start()
    #the new thread will check the surrounding for match word
    def newThread(self, row, column, keyWord):
        #checking for matching word in direction: direction
        def checkDirection(changeInRow, changeInColumn):
            tempRow = row 
            tempColumn = column
            for i in range(len(keyWord)):
                #the following if statement rely on the fact that cpu will not even run the last and statement if the previous statement are false.
                #can be resolved by wrap another repetitive if-else statement outside
                if (-1 < tempRow < self.getRow()) and (-1 < tempColumn < self.getColumn()) and keyWord[i] == self.puzzleList[tempRow][tempColumn]:
                    tempRow -= changeInRow 
                    tempColumn += changeInColumn 
                else:
                    return None 
            return True
        #load the data into the main process for it to display
        def returnData(direction):
            self.processQueue.put((row, column, direction))
        #checking each direction
        if len(keyWord) > 1:
            if checkDirection(1, 0):
                returnData("top")
            if checkDirection(1, 1):
                returnData("topRight")
            if checkDirection(0, 1):
                returnData("right")
            if checkDirection(-1, 1):
                returnData("buttomRight")
            if checkDirection(-1, 0):
                returnData("buttom")
            if checkDirection(-1, -1):
                returnData("buttomLeft")
            if checkDirection(0, -1):
                returnData("left")
        else:
            returnData("not applicable")
    #convert a single string into a matrix 
    def turnToList(self, row, column, puzzle):
        puzzleList = [[0 for x in range(column)] for y in range(row)]
        i = 0
        for r in range(row):
            for c in range(column):
                puzzleList[r][c] = puzzle[i]
                i += 1
        return puzzleList
    def getRow(self):
        return self._row
    def getColumn(self):
        return self._column 
if __name__ == '__main__':
    #puzzle used in the test: https://www.gmpuzzles.com/blog/word-search-rules-and-info/
    solver = WordPuzzleSolver(7, 8, "jsolutissunaruuaneptunetsonieisurcevtrerahtraesnmmercury")
    while True:
        solver.solve(input("keyWord: "))
