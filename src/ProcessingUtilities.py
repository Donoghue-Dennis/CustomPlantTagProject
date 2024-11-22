from src import *
import csv

def processPlantCSV(iInputFilePath,iOutputFilePath):
    lPlantInfoList = []

    # write the input CSV
    with open(iInputFilePath, newline='' ) as iFile:
        plantReader = csv.reader(iFile)

        # skip the header
        next(plantReader, None)

        # construct plant list from other rows
        for row in plantReader:
            lPlantInfoList.append(PlantInfo(row))
    # write to output csv
    PrintingUtilities.printPlantInfoListToCSV(iOutputFilePath,lPlantInfoList)