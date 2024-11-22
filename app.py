import src
import sys
import logging
logger = logging.getLogger(__name__)

def main():
    args = sys.argv[1:]
    logging.basicConfig(filename='PlantTag.log', level=logging.root)
    logger.info('Started')

    defaultInputFile = "./TestPlants.csv"
    defaultOutputFile = "./output/TestPlantTags.csv"
    if 0 == args.count():
        src.ProcessingUtilities.processPlantCSV(defaultInputFile,defaultOutputFile)
    elif 1 == args.count():
        src.ProcessingUtilities(args[0],defaultOutputFile)
    elif 2 == args.count():
        src.ProcessingUtilities(args[0],args[1])
    else:
        logger.error("Too many arguments passed in")
        raise Exception("Too many arguments passed in")
    logger.info('Finished')

if __name__ == '__main__':
    main()