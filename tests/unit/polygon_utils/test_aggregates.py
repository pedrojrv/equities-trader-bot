import numpy as np
from datetime import datetime

from pedrino.polygon_utils import aggregates


def test_get_agg():
    from_date = datetime(2022, 9, 1, 6, 40, 0)
    to_date = datetime(2022, 9, 1, 6, 43, 0)
    agg = aggregates.get_agg('NVDA', from_date, to_date)

    # There should be a row for each minute inclusive
    assert len(agg) == 4

    expected_timestamps = np.array([1662039600, 1662039660, 1662039720, 1662039780])
    expected_opens = np.array([142.07 , 142.85 , 142.6  , 142.255])
    expected_volumes = np.array([460286, 458594, 405116, 407087])
    assert np.array_equal(expected_timestamps, agg.date_s.values)
    assert np.array_equal(expected_opens, agg.open.values)
    assert np.array_equal(expected_volumes, agg.volume.values)
