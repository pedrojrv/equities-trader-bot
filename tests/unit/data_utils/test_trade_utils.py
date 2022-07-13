import random
from pedrino.polygon_utils import trades


class MockTradeObject():
    def __init__(self, price, size):
        self.price = price
        self.size = size


def test_get_average_data_trades():
    exp_num_trades = 10
    random_prices = [random.uniform(10, 100) for _ in range(exp_num_trades)]
    random_sizes = [int(size) for size in random_prices]
    trades_iterable = []

    exp_average_price = []
    exp_total_volume = 0
    for price, size in zip(random_prices, random_sizes):
        exp_average_price.append(price)
        exp_total_volume += size
        trades_iterable.append(MockTradeObject(price, size))

    average_price, total_volume, num_trades = trades._get_average_data_trades(trades_iterable)
    assert average_price == exp_average_price
    assert total_volume == exp_total_volume
    assert num_trades == exp_num_trades
