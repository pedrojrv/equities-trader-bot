"""Module to get all available news for a given ticker."""
import time
import pandas as pd
from datetime import datetime
from collections import OrderedDict, defaultdict

from pedrino import client


def get_news(ticker: str, timestamp: datetime) -> pd.DataFrame:
    cl = client.get_client()
    published_utc = time.strftime('%Y-%m-%d', time.gmtime(timestamp))
    news_iterator = cl.list_ticker_news(ticker, published_utc, limit=1000)

    ids = []
    dates_utc = []
    titles = []
    descriptions = []
    article_urls = []

    for ticker_news in news_iterator:
        ids.append(ticker_news.id)
        dates_utc.append(ticker_news.published_utc)
        titles.append(ticker_news.title)
        descriptions.append(ticker_news.description)
        article_urls.append(ticker_news.article_url)

    stock_news = pd.DataFrame({
        'id': ids,
        'date_utc': dates_utc,
        'title': titles,
        'description': descriptions,
        'article_urls': article_urls,
    })

    return stock_news
