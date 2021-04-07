from pandas import DataFrame

from IBL.data.utility import load_file


def load() -> DataFrame:

    """
    Load the prices for global market portoflio
    Returns
    -------
    data : DataFrame
        Data set containing prices for ACWI ETF, representing the market portfolio.
    """
    return load_file(__file__, "market.csv.gz")
