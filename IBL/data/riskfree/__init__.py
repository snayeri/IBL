from pandas import DataFrame

from IBL.data.utility import load_file


def load() -> DataFrame:

    """
    Load the data for riskfree rate used in the examples
    Returns
    -------
    data : DataFrame
        Data set containing quotes for 90day t-bill converted to daily riskfree rate.
    """
    return load_file(__file__, "riskfree.csv.gz")
