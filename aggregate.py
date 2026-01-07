''' Aggregate layer'''
import pandas as pd

def aggregate(df:pd.DataFrame) -> pd.DataFrame:
    ''' Aggregates metrics in dataframe'''

    # Calculated neighbourhood-level aggregates
    neighbourhood_df = (
        df
        .groupby('neighbourhood_group', observed=True)
        .agg(
            neighbourhood_avg_price = ('price', 'mean'),
            neighbourhood_min_price = ('price', 'min'),
            neighbourhood_max_price = ('price', 'max'),
            neighbourhood_adv_count = ('id', 'count'),
        )
        .reset_index()
    )

    # and enriched listing-level dataset via left join
    df = df.merge(neighbourhood_df, on='neighbourhood_group', how='left')

    # Price difference from neighbourhood average
    df['price_vs_neighbourhood_avg'] = df['price'] - df['neighbourhood_avg_price']

    return df
