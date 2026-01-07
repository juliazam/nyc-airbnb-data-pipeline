from aggregate import aggregate
from transform import transform
from errors import BusinessRuleValidationError, DataTypeValidationError, SchemaValidationError
from ingest import ingest_csv
from logger import get_logger
from validate import validate

def run_pipeline(config:dict):
    ''' Data pipeline'''
    logger = get_logger()
    logger.info("Pipeline started")

    data = ingest_csv(config)

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

    logger.info('Transformation started')
    logger.debug('Rows before transfromation: %s', validated_data.shape[0])
    transformed_data = transform(validated_data, config)
    logger.info('Transfromation successed.')
    logger.debug('Rows after transfromation: %s', transformed_data.shape[0])
    logger.debug('Dataframe shape: %s', transformed_data.shape)
    logger.debug('Data types: %s', transformed_data.dtypes)

    logger.info('Aggregation started')
    aggregated_data = aggregate(transformed_data)
    logger.info('Aggregation successed')
    logger.debug('New dataframe with aggregated data shape: %s', aggregated_data.shape)

    logger.info("Pipeline successed")
