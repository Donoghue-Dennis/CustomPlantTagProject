import numpy as np
import logging
import os
logger = logging.getLogger(__name__)

def printPlantInfoListToCSV(iOutputFilePath,iPlantInfoList):
    for jPlantInfo in iPlantInfoList:
        print("foo")

def printPlantInfoListToConsole(iPlantInfoList):
    for jPlantInfo in iPlantInfoList:
        pMsg = "Plant: " + jPlantInfo.ScientificName
        print(pMsg)
        logger.info(pMsg)

        pMsg = "Common names: " + ", ".join(jPlantInfo.CommonNameList)
        print(pMsg)
        logger.info(pMsg)

        pMsg = "Plant Tag Options: "
        print(pMsg)
        logger.info(pMsg)
        for jPlantTag in jPlantInfo.StampingOptions:
            lRowCount, lColumnCount = jPlantTag.StampingPlan.shape
            for iR in range(len(jPlantTag.PlantNameRowList)):
                pMsg = "    " + "".join(["—"]*(lColumnCount*2 + 1))
                print(pMsg)
                logger.info(pMsg)

                pMsg = "    |"
                for iC in range(lColumnCount):
                    pMsg += jPlantTag.StampingPlan[iR,iC] + "|"
                print(pMsg)
                logger.info(pMsg)

            pMsg = "    Complexity Score: " + str(jPlantTag.ComplexityScore)
            print(pMsg)
            logger.info(pMsg)

            pMsg = "    Complexity Score: " + jPlantTag.StampingOrder + "\n"
            print(pMsg)
            logger.info(pMsg)
        lTerminalWidth = os.get_terminal_size()[0]
        pMsg = "\n" + "".join(["="]*lTerminalWidth) + "\n\n"
        print(pMsg)
        logger.info(pMsg)
            