"""Exchanges related data utilities."""
from pedrino import client


def get_stock_exchanges():
    """Retrieve all US exchanges supported by Polygon.

    Returns
    -------
    dict
        {exchange_mic_code: exchange_name}
    """
    polygon_client = client.get_client()

    all_exchanges = polygon_client.get_exchanges()
    stock_exchanges = [exchange for exchange in all_exchanges if exchange.asset_class == "stocks"]
    stock_exchanges_dict = {exchange.mic: exchange.name for exchange in stock_exchanges}
    return stock_exchanges_dict
