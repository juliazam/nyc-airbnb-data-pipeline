''' Writing layer '''
from pathlib import Path
import pandas as pd
from logger import get_logger

def write_output(df: pd.DataFrame, config: dict) -> None:
    ''' Writes final dataframe to output formats. '''
    logger = get_logger()

    output_path = Path(config['output']['path'])
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # --- Write JSON ---
    try:
        df.to_json(output_path, orient='records', lines=True, force_ascii=False)
        logger.info("JSON output written to %s", output_path)
    except Exception:
        logger.exception("Failed to write JSON output")
        raise

    # --- Write CSV ---
    csv_path = output_path.with_suffix('.csv')
    try:
        df.to_csv(csv_path, index=False)
        logger.info("CSV output written to %s", csv_path)
    except Exception:
        logger.exception("Failed to write CSV output")
        raise
