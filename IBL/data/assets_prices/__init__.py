from pandas import DataFrame

from IBL.data.utility import load_file


def load() -> DataFrame:

    """
    Load the asset prices used in the examples
    Returns
    -------
    data : DataFrame
        Data set containing the asset prices.
    """
    return load_file(__file__, "assets_prices.csv.gz")
