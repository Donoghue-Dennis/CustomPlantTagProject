import numpy as np
import logging
from src import LetterCounter
logger = logging.getLogger(__name__)


ROW_COUNT = 3
COLUMN_COUNT = 17

class PlantTag:
    def __init__(self, iPlantName=None, iStampingPlan=None, iComplexityScore=None, iStampingOrder=None, iPlantNameRowList=None):
        if iPlantName is not None:
            self.PlantName = iPlantName
            self.StampingPlan = None
            self.ComplexityScore = None
            self.StampingOrder = None
            self.PlantNameRowList = []
            self.__LetterCounterList = []
            self.__GenerateStampingPlan()
            self.__GetComplexityScore()
            self.__GetStampingOrder()
        else:
            self.PlantName = None
            self.StampingPlan = None
            self.ComplexityScore = None
            self.StampingOrder = None
            self.PlantNameRowList = None


    def __GenerateStampingPlan(self):
        if self.PlantName is not None:
            if 0 < len(self.PlantName):
                # initialize Plant Tag construction values to 2d array of whitespace chars
                self.StampingPlan = np.empty(shape=[ROW_COUNT,COLUMN_COUNT],dtype=np.dtypes.StringDType)
                self.StampingPlan.fill(" ")

                # split string into rows, cut and merge to size
                lRawPlantNameRowList = self.PlantName.split()
                self.PlantNameRowList = self.__RightSizeStringsForRowLength(lRawPlantNameRowList)

                if ROW_COUNT < len(self.PlantNameRowList):
                    logger.error("Unable to Generate Stamping Plan, Plant name is too way long")
                    raise Exception("Unable to Generate Stamping Plan, Plant name is too way long")

                # slot strings into rows
                for index in range(len(self.PlantNameRowList)):
                    self.__CenterStringInRow(self.PlantNameRowList[index], index)
            else:
                logger.error("Unable to Generate Stamping Plan, Plant name is empty")
                raise Exception("Unable to Generate Stamping Plan, Plant name is empty")
        else:
            logger.error("Unable to Generate Stamping Plan, Plant name is empty")
            raise Exception("Unable to Generate Stamping Plan, Plant name is null")


    def __GetStampingOrder(self):
        lLetterList = []
        oStampingOrder = ""
        
        # build list of LetterCounter objects
        for x in range(len(self.PlantNameRowList)):
            lRowSortedCharList = sorted(self.PlantNameRowList[x])
            for y in range (len(lRowSortedCharList)):
                matchingLetterList = list(filter(lambda z: z.Letter == lRowSortedCharList[y], lLetterList))
                if 0 < len(matchingLetterList):
                    matchingLetterList[0].LetterCount+=1
                    matchingLetterList[0].RowSet.add(x)
                else:
                    lLetterList.append(LetterCounter.LetterCounter(lRowSortedCharList[y],x))

        # sort list of LetterCounter objects by LetterCount then RowSet Length
        # and save sorted list
        self.__LetterCounterList = sorted(lLetterList, key=lambda l: (l.LetterCount, -len(l.RowSet)),reverse=True)

        # convert sorted list to string
        for jLetterCounter in self.__LetterCounterList:
            oStampingOrder += "".join([jLetterCounter.Letter]*jLetterCounter.LetterCount)

        self.StampingOrder = oStampingOrder


    def __GetComplexityScore(self):
        oComplexityScore = 0

        # +10    - swapping stamps takes a long time
        # +n     - sliding tag to position prior to each stamping within row takes less time
        # +(r-1) - sliding tag up or down rows takes less time, first row is free
        # Simple heuristic for now
        for jLetterCounter in self.__LetterCounterList:
            oComplexityScore += 10 + jLetterCounter.LetterCount + len(jLetterCounter.RowSet-1)
        self.ComplexityScore = oComplexityScore


    def __RightSizeStringsForRowLength(self, iStringList):
        for j in range(len(iStringList)):
            logger.debug("Rightsizing " + iStringList[j])
            if(len(iStringList[j]) > COLUMN_COUNT):
                # truncate long word
                logger.debug("Truncated " + iStringList[j] + " to " + iStringList[j][:COLUMN_COUNT])
                iStringList[j] = iStringList[j][:COLUMN_COUNT]
            elif j+1 < len(iStringList):
                # merge short words
                if COLUMN_COUNT >= (len(iStringList[j]) + len(iStringList[j+1]) + 1):
                    logger.debug("Combined Row: " + iStringList[j] + " " + iStringList[j])
                    iStringList[j] = iStringList[j] + " " + iStringList[j+1]
                    iStringList.pop(j+1)
                    # call recursively, with merged string
                    return self.__RightSizeStringsForRowLength(iStringList)
            logger.debug("Rightsized " + iStringList[j])
        return iStringList

    def __CenterStringInRow(self, iString, iRowIndex):
        logger.debug("Centering " + iString + " in Row " + str(iRowIndex))
        # init reused values
        mCol = COLUMN_COUNT//2
        mStr = len(iString)//2

        # handle middle slot
        lIsOdd = len(iString) % 2
        if(lIsOdd):
            # fill middle slot with middle char, remove middle char
            self.StampingPlan[iRowIndex][mCol] = iString[mStr]
            iString = iString[:mStr] + iString[mStr+1:]

        # handle other slots
        debugStr = ""
        for k in range((len(iString)//2)):
            lowColIndex = mCol - k - 1
            highColIndex = mCol + k + 1
            lowStrIndex = mStr - k - 1
            highStrIndex = mStr + k
            lowChar = iString[lowStrIndex]
            highChar = iString[highStrIndex]
            self.StampingPlan[iRowIndex][lowColIndex] = lowChar
            self.StampingPlan[iRowIndex][highColIndex] = highChar
            debugStr = lowChar + debugStr + highChar
        logger.debug("Inserted string " + debugStr)