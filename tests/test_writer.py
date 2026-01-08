from pathlib import Path
import pandas as pd
from writer import write_output

def test_write_output(tmp_path):
    df = pd.DataFrame({
        "id": [1, 2],
        "price": [10, 20]
    })

    config = {
        "output": {
            "path": str(tmp_path / "result.json")
        }
    }

    write_output(df, config)

    output_json = Path(config['output']['path'])
    output_csv = output_json.with_suffix('.csv')

    assert output_json.is_file()
    assert output_csv.is_file()
