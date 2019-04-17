import os
import requests
from datetime import datetime, timedelta

_NYT_API = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'


class NoApiKeyException(Exception):
    def __init__(self, value):
        self.value = value


class NewYorkTimesScrapper:
    ''' Scraps NYT Articles API for political content'''
    def __init__(self, api_key: str):
        '''
        api_key (str): API key for New York Times, available at
            developer.nytimes.com
        '''
        self.key = api_key
        if not self.key:
            raise NoApiKeyException('API key required')

    def search(self, q: str, time_period: int = 2, **kwargs):
        '''
        q (str): query string
        time_period (int): in days, the time period to search
        kwargs:

        '''
        begin = datetime.today()
        if time_period > 0:
            begin = begin - timedelta(days=time_period)
        begin = self._format_date(begin)

        q = self._format_string(q)
        query = f'?q={q}&begin_date={begin}&news_desk=politics'
        api_key = f'&api-key={self.key}'
        url = f'{_NYT_API}{query}{api_key}'

        r = requests.get(url)
        return r.json()

    def _format_date(self, day):
        return f'{day.year}{day.month:02}{day.day:02}'

    def _format_string(self, string):
        return '+'.join(string.lower().split())

    def _format_query(self, args):
        pass


if __name__ == '__main__':
    api = NewYorkTimesScrapper(os.environ['NYT_API_KEY'])
    dem_articles = api.search('win for democrats')
    rep_articles = api.search('win for republicans')
