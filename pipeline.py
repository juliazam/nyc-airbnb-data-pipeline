from errors import BusinessRuleValidationError, DataTypeValidationError, SchemaValidationError
from ingest import ingest_csv
from logger import get_logger
from validate import validate

def run_pipeline(config:dict):
    ''' Data pipeline'''
    logger = get_logger()
    logger.info("Pipeline started")

    data = ingest_csv(config)
    logger.debug(data.dtypes)

    # Data validation
    logger.info('Validation started')
    try:
        validated_data = validate(data, config)
    except (SchemaValidationError, DataTypeValidationError) as err:
        logger.critical("Validation failed. Pipeline stopped: %s", err)
        raise
    except BusinessRuleValidationError as err:
        logger.error('Validation completed with business rule violations: %s.\
                     Will be handled in transformation.', err)
        # At this point we know we have dirty data
        validated_data = data
    else:
        logger.info('Validation successed')

    logger.info("Pipeline successed")
