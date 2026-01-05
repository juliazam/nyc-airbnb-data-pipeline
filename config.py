''' Pipeline configuration '''

PIPELINE_CONFIG = {
    "source": {
        "path": "data/NYC-Airbnb-2023.csv",
        "source_name": "airbnb_nyc_2023"
    },
    "ingestion": {
        "max_retries": 3,
        "retry_delay": 1.0,
    },
    "output": {
        "path": "data/output/result.json"
    }
}

LOGGING_CONFIG = {
    "level": "INFO",
    "log_file": "logs/pipeline.log",
    "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    "max_bytes": 5_000_000,
    "backup_count": 5
}
