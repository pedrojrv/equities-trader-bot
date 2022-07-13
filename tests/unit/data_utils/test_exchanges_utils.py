from pedrino.polygon_utils import exchanges


def test_get_stock_exchanges():
    """Assert main market symbols in polygon exchanges."""
    stock_exchanges_dict = exchanges.get_stock_exchanges()
    assert len(stock_exchanges_dict) != 0
    exchanges_keys = stock_exchanges_dict.keys()
    for key in ['XCIS', 'XBOS', 'XASE']:
        assert key in exchanges_keys
