from pandas import DataFrame

from IBL.data.utility import load_file


def load() -> DataFrame:

    """
    Load the asset prices used in the examples
    Returns
    -------
    data : DataFrame
        Data set containing prices for ETF's selected as portfolio of assets.
    """
    return load_file(__file__, "portfolio.csv.gz")
