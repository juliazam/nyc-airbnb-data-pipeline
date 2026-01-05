''' All pipeline errors'''

class IngestionError(Exception):
    """Base class for ingestion errors"""

class SourceNotFoundError(IngestionError):
    """Source file not found"""

class EmptySourceError(IngestionError):
    """Source file is empty"""

class SourceReadError(IngestionError):
    """Failed to read source"""
