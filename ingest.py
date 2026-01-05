''' Ingestion layer'''
import pandas as pd
from errors import EmptySourceError, SourceNotFoundError, SourceReadError
from logger import get_logger

def ingest_csv(config:dict) -> pd.DataFrame:
    ''' Ingests data from csv-file in config and returns DataFrame'''
    logger = get_logger()
    logger.info('Imgestion started', extra={"source": config['source']["source_name"]})

    csv_file = config['source']['path']

    try:
        df = pd.read_csv(csv_file, encoding='utf-8')
    except FileNotFoundError as err:
        logger.error("Source data file %s not found", csv_file, exc_info=True)
        raise SourceNotFoundError("Source data file not found") from err
    except (pd.errors.ParserError, UnicodeDecodeError) as err:
        logger.error("Can't read %s file", csv_file, exc_info=True)
        raise SourceReadError('Source data file reading error') from err
    except pd.errors.EmptyDataError as err:
        logger.error("Can't read %s file", csv_file, exc_info=True)
        raise EmptySourceError('Source data file has no data') from err
    except Exception:
        logger.exception("Unexpected ingestion error")
        raise

    if df.empty:
        logger.warning('Data frame is empty')
        return df

    logger.info('Ingestion succeeded', extra={"source": config['source']["source_name"]})

    return df
