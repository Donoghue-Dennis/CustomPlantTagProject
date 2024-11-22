import numpy as np
import logging
logger = logging.getLogger(__name__)

ROW_COUNT = 3
COLUMN_COUNT = 17

class PlantTag:
    def __init__(self, iPlantName=None, iStampingPlan=None, iComplexityScore=None, iStampingOrder=None, i__PlantNameRowList=None):
        if iPlantName is not None:
            self.PlantName = iPlantName
            self.StampingPlan = None
            self.ComplexityScore = None
            self.StampingOrder = None
            self.__PlantNameRowList = []
            self.__GenerateStampingPlan()
            self.__GetComplexityScore()
            self.__GetStampingOrder()
        else:
            self.PlantName = None
            self.StampingPlan = None
            self.ComplexityScore = None
            self.StampingOrder = None
            self.__PlantNameRowList = None


    def __GetComplexityScore(self):
        self.ComplexityScore = 1

    def __GetStampingOrder(self):
        self.StampingOrder = "ABC"


    def __GenerateStampingPlan(self):
        if self.PlantName is not None:
            if 0 < len(self.PlantName):
                # initialize Plant Tag construction values
                self.StampingPlan = np.empty(shape=[ROW_COUNT,COLUMN_COUNT],dtype=np.dtypes.StringDType)
                
                # split string into rows, cut and merge to size
                lRawPlantNameRowList = self.PlantName.split()
                __PlantNameRowList = self.__RightSizeStringsForRowLength(lRawPlantNameRowList)

                if ROW_COUNT < len(__PlantNameRowList):
                    logger.error("Unable to Generate Stamping Plan, Plant name is too way long")
                    raise Exception("Unable to Generate Stamping Plan, Plant name is too way long")

                # slot strings into rows
                for index in range(len(__PlantNameRowList)):
                    self.__CenterStringInRow(__PlantNameRowList[index], index)
            else:
                logger.error("Unable to Generate Stamping Plan, Plant name is empty")
                raise Exception("Unable to Generate Stamping Plan, Plant name is empty")
        else:
            logger.error("Unable to Generate Stamping Plan, Plant name is empty")
            raise Exception("Unable to Generate Stamping Plan, Plant name is null")


    def __RightSizeStringsForRowLength(self, iStringList):
        for j in range(len(iStringList)):
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
        return iStringList

    def __CenterStringInRow(self, iString, iRowIndex):
        # init reused values
        mCol = COLUMN_COUNT//2
        mStr = len(iString)//2

        # handle middle slot
        lIsEven = len(iString) % 2
        if(lIsEven):
            # middle slot is whitespace char
            self.StampingPlan[iRowIndex][mCol] = " "
        else:
            # fill middle slot with middle char, remove middle char
            self.StampingPlan[iRowIndex][mCol] = iString[mStr]
            iString = iString[:mStr] + iString[mStr+1:]

        # handle other slots
        for k in range(len(iString)//2):
            self.StampingPlan[iRowIndex][mCol + k] = iString[mStr + k]
            self.StampingPlan[iRowIndex][mCol - k] = iString[mStr - k]