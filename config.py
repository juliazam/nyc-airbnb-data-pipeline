''' Pipeline configuration '''

PIPELINE_CONFIG = {
    "source": {
        "path": "data/NYC-Airbnb-2023.csv",
        "source_name": "airbnb_nyc_2023",
        "required_columns": {
            "id" : "int",
            "name": "string",
            "host_id": "int",
            "host_name": "string",
            "neighbourhood_group": "category",
            "neighbourhood": "string",
            "room_type": "category",
            "price": "int",
            "minimum_nights": "int",
            "availability_365": "int"
        }
    },
    "ingestion": {
        "max_retries": 3,
        "retry_delay": 1.0,
    },
    "output": {
        "path": "data/output/result.json",
        'table_name': 'listings'
    }
}

LOGGING_CONFIG = {
    "level": "DEBUG",
    "log_file": "logs/pipeline.log",
    "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    "max_bytes": 5_000_000,
    "backup_count": 5
}
