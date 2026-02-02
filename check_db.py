'''Check the data saved in the database.'''
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def verify_data():
    engine = create_engine(os.getenv('DATABASE_URL'))

    # Read data back from the database
    df_from_db = pd.read_sql('listings', con=engine)

    print("--- Database check ---")
    print(f"Total rows: {len(df_from_db)}")
    print(f"Data types:\n{df_from_db.dtypes}")

    # Check a specific date column if it exists
    if 'last_review' in df_from_db.columns:
        print(f"\nDate example: {df_from_db['last_review'].iloc[0]}")
        print(f"Date type: {type(df_from_db['last_review'].iloc[0])}")

if __name__ == "__main__":
    verify_data()
