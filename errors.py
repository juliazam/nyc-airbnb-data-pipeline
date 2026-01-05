''' All pipeline errors'''

class IngestionError(Exception):
    '''Base class for ingestion errors'''

class SourceNotFoundError(IngestionError):
    '''Source file not found'''

class EmptySourceError(IngestionError):
    '''Source file is empty'''

class SourceReadError(IngestionError):
    '''Failed to read source'''


class ValidationError(Exception):
    '''Base class for validation errors'''

class SchemaValidationError(ValidationError):
    '''Schema validation error'''

class DataTypeValidationError(ValidationError):
    '''Data type validation error'''

class BusinessRuleValidationError(ValidationError):
    ''' Errors in business rules'''

class TransformationErrors(Exception):
    ''' Base class for transformation Errors'''

class DataTypeTransformationError(TransformationErrors):
    ''' Data type transformation error'''
