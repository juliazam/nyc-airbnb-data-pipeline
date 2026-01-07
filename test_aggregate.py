import pandas as pd

from aggregate import aggregate

data = {
    "id": [1, 2, 3, 4],
    "name": ['A', 'B', 'C', 'D'],
    "host_id": [10, 20, 30, 40],
    "host_name": ['X', 'W', 'Y', 'Z'],
    "neighbourhood_group": ["Queens", "Brooklyn", "Queens", "Manhattan"],
    "price": [10, 15, 20, 15],
    "availability_365": [100, 200, 150, 50],
}
df = pd.DataFrame(data)

def test_aggregate_columns_exist():
    aggregated = aggregate(df)

    expected_cols = [
        'neighbourhood_avg_price',
        'neighbourhood_min_price',
        'neighbourhood_max_price',
        'neighbourhood_adv_count',
        'price_vs_neighbourhood_avg'
    ]

    for col in expected_cols:
        assert col in aggregated.columns

def test_price_vs_neighbourhood_avg_logic():
    aggregated = aggregate(df)

    diff = (
        aggregated['price']
        - aggregated['neighbourhood_avg_price']
    )

    assert (aggregated['price_vs_neighbourhood_avg'] == diff).all()

def test_neighbourhood_metrics_not_null():
    aggregated = aggregate(df)

    assert aggregated['neighbourhood_avg_price'].isnull().sum() == 0
