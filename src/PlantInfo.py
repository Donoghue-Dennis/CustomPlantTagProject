from src import *
import itertools

class PlantInfo:
    def __init__(self):
        self.ScientificName = None
        self.CommonNameList = None
        self.StampingOptions = None


    def __init__(self,iRow):
        self.ScientificName = iRow[0]
        self.CommonNameList = iRow[1:]
        self.StampingOptions = []
        self.__GenerateStampingOptions()


    def __init__(self,iScientificName,iCommonNameList):
        self.ScientificName = iScientificName
        self.CommonNameList = iCommonNameList
        self.StampingOptions = []
        self.__GenerateStampingOptions()


    def __init__(self,iScientificName,iCommonNameList,iStampingOptions):
        self.ScientificName = iScientificName
        self.CommonNameList = iCommonNameList
        self.StampingOptions = iStampingOptions


    def __GenerateStampingOptions(self):
        # make sure class was instantiated with values
        if ((self.iScientificName is not None) and
            (self.CommonNameList is not None) and
            (0 < self.CommonNameList.Count())):
            self.StampingOptions.append(PlantTag(self.ScientificName))
            for jCommonName in self.CommonNameList:
                self.StampingOptions.append(PlantTag(jCommonName))
        
            # sort Stamping options by complexity score
            self.StampingOptions.sort(key=lambda x:x.ComplexityScore, reverse=False)