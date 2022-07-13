"""Pedrino constants."""
from enum import Enum, unique


@unique
class Years(str, Enum):
    """ONNX Layers and Attributes Names."""

    STOCKS = 2004
    FOREX = 2009
    CRYPTO = 2017
    OPTIONS = 2014

POLYGON_AGG_LIMIT = 50000
