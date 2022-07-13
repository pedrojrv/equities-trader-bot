"""Exchanges related data utilities."""
from typing import Dict
from pedrino import client


def get_stock_exchanges() -> Dict[str, str]:
    """Retrieve all US exchanges supported by Polygon.

    Returns
    -------
    dict
        {exchange_mic_code: exchange_name}
    """
    cl = client.get_client()

    all_exchanges = cl.get_exchanges()
    stock_exchanges = [exchange for exchange in all_exchanges if exchange.asset_class == "stocks"]
    stock_exchanges_dict = {exchange.mic: exchange.name for exchange in stock_exchanges}
    return stock_exchanges_dict
