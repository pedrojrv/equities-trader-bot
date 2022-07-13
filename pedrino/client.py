"""Provides authenticated Polygon REST API client."""
import os
from polygon import RESTClient


def get_client() -> RESTClient:
    """Get authenticated Polygon RESTClient.

    Returns
    -------
    polygon.RESTClient
        Authenticated client.

    Raises
    ------
    ValueError
        If POLYGON_API_KEY environmental variable is not detected.
    """
    os.environ['POLYGON_API_KEY'] = '45lJarByEgEjiabROm6ZTbphYP9jTGqa'
    api_key = os.environ.get("POLYGON_API_KEY", False)
    if not api_key:
        raise ValueError("POLYGON_API_KEY enviornmental variable not detected.")

    client = RESTClient(api_key)
    return client
