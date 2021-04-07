from pandas import DataFrame

from IBL.data.utility import load_file


def load() -> DataFrame:

    """
    Load the market weight of assets in the portfolio used in the examples
    Returns
    -------
    data : DataFrame
        Data set containing market cap for ETF's selected as portfolio of assets.
    """
    return load_file(__file__, "marketcap.csv.gz")
