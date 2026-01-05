''' Transformation layer '''
import pandas as pd
from errors import DataTypeTransformationError

def transform(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    ''' Transforms dataframe'''

    # --- Step 0: Fill missing names BEFORE type conversion ---
    for col in ['name', 'host_name']:
        if col in df.columns:
            df[col] = df[col].astype('object').fillna('Unknown')

    # --- Step 1: Remove rows with null ids or host_ids ---
    df = df.dropna(subset=['id', 'host_id'])

    # --- Step 2: Keep only rows where price >= 0 ---
    df = df[df['price'] >= 0]

    # --- Step 3: Keep only rows where availability in range [0, 365] ---
    df = df[(df['availability_365'] >= 0) & (df['availability_365'] <= 365)]

    # --- Step 4: Drop empty 'license' column if exists ---
    if 'license' in df.columns and df['license'].isna().all():
        df = df.drop(columns=['license'])

    # --- Step 5: Drop duplicates by 'id' ---
    df = df.drop_duplicates(subset=['id'], keep='first')

    # --- Step 6: Convert data types as per config ---
    expected_types = config['source']['required_columns'].items()
    try:
        for col, expected_type in expected_types:
            if col in df.columns:
                df[col] = df[col].astype(expected_type)
    except ValueError as err:
        raise DataTypeTransformationError(f"Column conversion error: {err}") from err

    return df
