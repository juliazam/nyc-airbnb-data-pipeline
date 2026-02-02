'''Save DataFrame in SQLite database.'''
import os
from sqlalchemy import Engine, create_engine
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import pandas as pd

from logger import get_logger

load_dotenv()

def get_engine() -> Engine:
    '''Create and return a SQLAlchemy engine for the given SQLite database path.'''
    db_url = os.getenv('DATABASE_URL')
    return create_engine(db_url, echo = os.getenv('DEBUG', 'False') == 'True')

def save_to_db(df: pd.DataFrame, table_name: str) -> None:
    '''Save the given DataFrame to the specified table in the SQLite database.'''
    logger = get_logger()
    try:
        engine = get_engine()
        with engine.connect() as connection:
            df.to_sql(table_name, con=connection, if_exists='replace', index=False)
        logger.info("Successfully saved data to table '%s'", table_name)
    except SQLAlchemyError as e:
        logger.error("A SQLAlchemy error occurred: %s", e)
    except Exception as e:
        logger.error("An unexpected error occurred: %s", e)
