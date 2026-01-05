''' Validation layer '''
import pandas as pd

from errors import BusinessRuleValidationError, DataTypeValidationError, SchemaValidationError

def validate(df:pd.DataFrame,  config: dict) -> pd.DataFrame:
    '''Validates schema, data types, non-null id, price >=0, availability in [0, 365]'''
    errors = []

    # Check for requred columns
    required_columns = config["source"]["required_columns"].keys()
    missing = set(required_columns) - set(df.columns)
    if missing:
        raise SchemaValidationError(f"Missing required columns: {missing}")

    # Check column's data types and null values
    expected_types = config['source']['required_columns'].items()
    try:
        for col, expected_type in expected_types:
            # Dataframe shouldn't have Null values in required columns
            if df[col].isnull().any():
                errors.append(f"Null values found in '{col}' column")
                continue
            df[col] = df[col].astype(expected_type)
    except ValueError as err:
        raise DataTypeValidationError(f"Column conversion error: {err}") from err

    # Business rules
    # price must be >= 0
    if (df["price"] < 0).any():
        errors.append('Negative prices detected')

    # availability_365 must be in [0, 365]
    if ((df["availability_365"] < 0) | (df["availability_365"] > 365)).any():
        errors.append("'availability_365' values out of range [0, 365]")

    if errors:
        raise BusinessRuleValidationError(errors)

    return df
