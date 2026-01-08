''' Tests ingest_csv function'''
from pathlib import Path
import pytest
from errors import EmptySourceError, SourceNotFoundError
from ingest import ingest_csv

def test_ingest_csv(tmp_path:Path):
    ''' Creates test csv-file and test configuration to test ingest_csv function'''
    csv_path = tmp_path / "test.csv"

    # Create test.csv
    csv_path.write_text("id,value\n1,10\n2,20")

    # Create test configuration
    config = {
        "source": {
            "path": str(csv_path),
            "source_name": "test_csv"
        }
    }

    df = ingest_csv(config)

    assert df.shape[0] == 2
    assert list(df.columns) == ["id", "value"]

def test_ingest_csv_file_not_found(tmp_path:Path):
    ''' If data file is not found should get FileNotFoundError '''
    csv_path = tmp_path / 'test_no_file.csv'

    # Create test configuration
    config = {
        "source": {
            "path": str(csv_path),
            "source_name": "test_csv"
        }
    }

    with pytest.raises(SourceNotFoundError) as err:
        df = ingest_csv(config)
    assert "Source data file not found" in str(err.value)
    assert err.type is SourceNotFoundError

def test_ingest_csv_empty_df(tmp_path:Path):
    ''' Tests that we can get empty dafaframe and its Ok '''
    csv_path = tmp_path / "test.csv"

    # Create test.csv
    csv_path.write_text("")

    # Create test configuration
    config = {
        "source": {
            "path": str(csv_path),
            "source_name": "test_csv"
        }
    }

    with pytest.raises(EmptySourceError) as err:
        df = ingest_csv(config)
    assert "Source data file has no data" in str(err.value)
    assert err.type is EmptySourceError
