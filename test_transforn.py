''' Tests transform function '''
import pandas as pd
from transform import transform

config = {
    "source": {
        "required_columns": {
            "id": "int",
            "name": "string",
            "host_id": "int",
            "host_name": "string",
            "price": "int",
            "availability_365": "int"
        }
    }
}

def test_transform_basic():
    ''' Check transform function '''
    import pandas as pd
    from transform import transform

    data = {
        "id": [1, 2, 3, 4],
        "name": ['A', None, 'C', 'D'],
        "host_id": [10, 20, 30, 40],
        "host_name": ['X', None, 'Y', 'Z'],
        "price": [10, 15, 20, 15],
        "availability_365": [100, 200, 150, 50],
        "license": [None, None, None, None]
    }
    df = pd.DataFrame(data)

    transformed = transform(df, config)

    # Check null id/host_id dropped
    assert transformed['id'].isnull().sum() == 0
    assert transformed['host_id'].isnull().sum() == 0

    # Check price >=0
    assert (transformed['price'] < 0).sum() == 0

    # Check availability
    assert transformed['availability_365'].between(0, 365).all()

    # Check all name/host_name columns filled
    assert transformed['name'].isnull().sum() == 0
    assert transformed['host_name'].isnull().sum() == 0
    assert 'Unknown' in transformed['name'].values
    assert 'Unknown' in transformed['host_name'].values

    # Check 'license' column removed
    assert 'license' not in transformed.columns

    # Check data types
    for col, data_type in config['source']['required_columns'].items():
        if data_type == 'int':
            assert transformed[col].dtype.name.startswith('int')
        elif data_type == 'string':
            assert transformed[col].dtype.name in ('string', 'object')
        else:
            raise ValueError(f"Unexpected type {data_type} in config")

def test_transform_duplicates_and_types():
    ''' Check if duplicates removed '''
    # Data with duplicated id=2
    data = {
        "id": [1, 2, 2, 3],
        "name": ['A', 'B', 'B_dup', 'C'],
        "host_id": [10, 20, 20, 30],
        "host_name": ['X', 'Y', 'Y_dup', 'Z'],
        "price": [100, 200, 200, 150],
        "availability_365": [10, 20, 20, 30]
    }

    df = pd.DataFrame(data)

    transformed = transform(df, config)

    # Check no more duplicated id
    assert transformed['id'].duplicated().sum() == 0

    # Check if dtypes were transformed correctly
    for col, dtype in config['source']['required_columns'].items():
        if dtype == 'int':
            assert pd.api.types.is_integer_dtype(transformed[col])
        elif dtype == 'string':
            assert pd.api.types.is_string_dtype(transformed[col])
