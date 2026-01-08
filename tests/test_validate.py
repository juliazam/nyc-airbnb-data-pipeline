''' Tests validate function'''
import pandas as pd
import pytest

from errors import BusinessRuleValidationError, DataTypeValidationError, SchemaValidationError
from validate import validate

config = {
    "source": {
        "required_columns": {
            "id" : "int",
            "name": "string",
            "host_id": "int",
            "price": "int",
            "availability_365": "int"
        }
    }
}

def test_validate_missing_columns():
    ''' Check validate function if reguired column missing'''
    data = {
        "id": [1, 2, 3],
        "name": ['A', 'B', 'C'],
        'price': [10, 20, 30],
        'availability_365': [1, 1, 1]
    }
    df = pd.DataFrame(data)
    with pytest.raises(SchemaValidationError) as err:
        validated_df = validate(df, config)
    assert err.type is SchemaValidationError

def test_validate_datatypes():
    ''' Chech validate function id can't convert data type'''
    data = {
        "id": [1, 2, 3],
        "name": ['A', 'B', 'C'],
        'host_id': [22, 33, 44],
        'price': [10, 20, 'expensive'],
        'availability_365': [1, 1, 1]
    }
    df = pd.DataFrame(data)

    with pytest.raises(DataTypeValidationError) as err:
        validated_df = validate(df, config)
    assert err.type is DataTypeValidationError

def test_validate_id():
    ''' Checks validate function with null id'''
    data = {
        "id": [1, 'abc', None],
        "name": ['A', 'B', 'C'],
        'host_id': [22, 33, 44],
        'price': [10, 20, 30],
        'availability_365': [1, 1, 1]
    }
    df = pd.DataFrame(data)

    with pytest.raises(BusinessRuleValidationError) as err:
        validated_df = validate(df, config)
    assert err.type is BusinessRuleValidationError
    assert "Null values found in 'id' column" in str(err.value)

def test_validate_host_id():
    ''' Checks validate function with null host_id'''
    data = {
        "id": [1, 2, 3],
        "name": ['A', 'B', 'C'],
        'host_id': [None, 33, 44],
        'price': [10, 20, 30],
        'availability_365': [1, 1, 1]
    }
    df = pd.DataFrame(data)

    with pytest.raises(BusinessRuleValidationError) as err:
        validated_df = validate(df, config)
    assert err.type is BusinessRuleValidationError
    assert "Null values found in 'host_id' column" in str(err.value)

def test_validate_price():
    ''' Checks validate function with negative price'''
    data = {
        "id": [1, 2, 3],
        "name": ['A', 'B', 'C'],
        'host_id': [22, 33, 44],
        'price': [10, 20, -30],
        'availability_365': [1, 1, 1]
    }
    df = pd.DataFrame(data)

    with pytest.raises(BusinessRuleValidationError) as err:
        validated_df = validate(df, config)
    assert err.type is BusinessRuleValidationError
    assert "Negative prices detected" in str(err.value)

def test_validate_availability():
    ''' Checks validate function if availability in range [0, 365]'''
    data = {
        "id": [1, 2, 3],
        "name": ['A', 'B', 'C'],
        'host_id': [22, 33, 44],
        'price': [10, 20, 30],
        'availability_365': [1, 400, 1]
    }
    df = pd.DataFrame(data)

    with pytest.raises(BusinessRuleValidationError) as err:
        validated_df = validate(df, config)
    assert err.type is BusinessRuleValidationError
    assert "'availability_365' values out of range [0, 365]" in str(err.value)

def test_validate():
    ''' Checks validate function with correct data'''
    data = {
        "id": [1, 2, 3],
        "name": ['A', 'B', 'C'],
        'host_id': [22, 33, 44],
        'price': [10, 20, 30],
        'availability_365': [1, 1, 1]
    }
    df = pd.DataFrame(data)

    validated_df = validate(df, config)
    assert df.shape == (3, 5)
