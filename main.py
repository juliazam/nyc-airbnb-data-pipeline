''' Main point to start pipeline'''
from logger import get_logger
from pipeline import run_pipeline
from config import PIPELINE_CONFIG

def main():
    logger = get_logger()
    logger.info("Starting pipeline from main")
    run_pipeline(PIPELINE_CONFIG)

if __name__ == "__main__":
    main()
