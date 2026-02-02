'''Unit tests for database operations using SQLAlchemy and Pandas'''
from sqlalchemy import create_engine
import pandas as pd

def test_save_to_db_function():
    '''Testing saving a DataFrame to the database'''
    # Create an in-memory SQLite database for testing
    test_engine = create_engine('sqlite:///:memory:')
    df = pd.DataFrame({'col1': [1, 2]})
    # Save the DataFrame to a SQL table named 'test_table'
    df.to_sql('test_table', test_engine, index=False)

    # Check if the table was created and contains the correct data
    result = pd.read_sql('test_table', test_engine)
    assert result.equals(df), "DataFrame was not saved correctly to the database"
    assert len(result) == 2, "DataFrame does not contain the expected number of rows"
