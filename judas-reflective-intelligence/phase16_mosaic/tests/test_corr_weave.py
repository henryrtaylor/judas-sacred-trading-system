import pandas as pd

from phase16_mosaic.correlation_weave import rolling_corr, load_prices

def test_corr_shape():
    df = load_prices(['AAA','BBB'])
    corr = rolling_corr(df, 30).dropna()

    # Check outermost index is multi-index (date, symbol)
    assert isinstance(corr.index, pd.MultiIndex)
    symbols = df.columns.tolist()

    # Extract last full 2x2 matrix
    last_date = corr.index.get_level_values(0).max()
    sub = corr.loc[last_date]

    assert sub.shape == (2, 2)
    assert set(sub.index) == set(symbols)
    assert set(sub.columns) == set(symbols)

    # Diagonal should be 1s
    for s in symbols:
        assert round(sub.loc[s, s], 10) == 1.0
