import pandas as pd


# Calculate analytics per ticker
def calculate_quote_analytics(quotes):
    if not quotes:
        return pd.DataFrame()

    # Create DataFrame
    df = pd.DataFrame(quotes)

    # Sort by 'ticker' and 'update_time'
    if "update_time" in df.columns:
        df = df.sort_values(["ticker", "update_time"])

    # Aggregate analytics
    analytics = (
        df.groupby(["ticker", "name"], dropna=False)
        .agg(
            observations=("ticker", "size"),
            avg_price=("last_price", "mean"),
            median_price=("last_price", "median"),
            min_price=("last_price", "min"),
            max_price=("last_price", "max"),
            avg_change=("change", "mean"),
            avg_change_percent=("change_percent", "mean"),
            total_volume=("volume", "sum"),
            total_value=("value", "sum"),
        )
        .reset_index()
    )

    return analytics
