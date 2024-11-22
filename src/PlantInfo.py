from src import PlantTag
import itertools

class PlantInfo:
    def __init__(self,iRow=None,iScientificName=None,iCommonNameList=None,iStampingOptions=None):
        if iRow is not None:
            self.ScientificName = iRow[0]
            self.CommonNameList = iRow[1:]
            self.StampingOptions = []
            self.__GenerateStampingOptions()
        elif iScientificName is not None and iCommonNameList is not None:
            self.ScientificName = iScientificName
            self.CommonNameList = iCommonNameList
            if iStampingOptions is not None:
                self.StampingOptions = iStampingOptions
            else:
                self.StampingOptions = []
                self.__GenerateStampingOptions()
        else:
            self.ScientificName = None
            self.CommonNameList = None
            self.StampingOptions = None

    def __GenerateStampingOptions(self):
        # make sure class was instantiated with values
        if ((self.ScientificName is not None) and
            (self.CommonNameList is not None) and
            (0 < len(self.CommonNameList))):
            self.StampingOptions.append(PlantTag.PlantTag(self.ScientificName))
            for jCommonName in self.CommonNameList:
                self.StampingOptions.append(PlantTag.PlantTag(jCommonName))
        
            # sort Stamping options by complexity score
            self.StampingOptions.sort(key=lambda x:x.ComplexityScore, reverse=False)