from ingest import ingest_csv
from logger import get_logger

def run_pipeline(config:dict):
    logger = get_logger()
    logger.info("Pipeline started")

    data = ingest_csv(config)

    logger.info("Pipeline successed")
