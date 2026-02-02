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

    # --- Step 4: Drop license' column if exists ---
    if 'license' in df.columns and df['license'].notna().sum() <= 1:
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

    # --- Step 7: Convert data types that are not in config
    if 'last_review' in df.columns:
        df['last_review'] = pd.to_datetime(df['last_review'], format='%d-%m-%Y', errors='coerce')

    if 'latitude' in df.columns:
        df['latitude'] = df['latitude'].astype('float')

    if 'longitude' in df.columns:
        df['longitude'] = df['longitude'].astype('float')

    if 'reviews_per_month' in df.columns:
        df['reviews_per_month'] = df['reviews_per_month'].astype('float')

    if 'number_of_reviews' in df.columns:
        df['number_of_reviews'] = df['number_of_reviews'].astype('int')

    if 'calculated_host_listings_count' in df.columns:
        df['calculated_host_listings_count'] = df['calculated_host_listings_count'].astype('int')

    if 'number_of_reviews_ltm' in df.columns:
        df['number_of_reviews_ltm'] = df['number_of_reviews_ltm'].astype('int')

    if 'room_type' in df.columns:
        df['room_type'] = df['room_type'].astype('category')

    if 'neighbourhood_group' in df.columns:
        df['neighbourhood_group'] = df['neighbourhood_group'].astype('category')

    return df
