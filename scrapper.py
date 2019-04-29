import os
import re
import requests
import urllib
from bs4 import BeautifulSoup
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
        self._key = api_key
        self.responses = {}
        self._queries = set([])
        if not self._key:
            raise NoApiKeyException('API key required')

    def search(self, q: str, time_period: int = 2, **kwargs):
        '''
        q (str): query string
        time_period (int): in days, the time period to search
        kwargs:

        '''
        if q not in self._queries:
            self._queries.add(q)
            begin = datetime.today()
            if time_period > 0:
                begin = begin - timedelta(days=time_period)
            begin = self._format_date(begin)

            q = self._format_string(q)
            query = f'?q={q}&fq={q}&begin_date={begin}&news_desk=politics'
            api_key = f'&api-key={self._key}'
            url = f'{_NYT_API}{query}{api_key}'

            r = requests.get(url)
            r = r.json()['response']['docs']
            r = {response['_id']: response for response in r}
            self.responses.update(r)

    def scrap(self):
        for r in self.responses.values():
            if not r.get('full_article'):
                url = r['web_url']
                r['full_article'] = self._scrap_article(url)

    def _scrap_article(self, url):
        webpage = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(webpage, features="html.parser")
        text = '/n'.join(map(lambda x: x.text, soup.find_all('p'))).lower()
        return text

    @property
    def articles(self):
        articles = []
        for r in self.responses.values():
            if r.get('full_article'):
                articles.append(r.get('full_article'))
        return articles

    @property
    def matches(self):
        matches = {}
        for article in self.articles:
            for q in self._queries:
                matches[q] = []
                query = re.compile(q)
                if re.search(query, article):
                    matches[q].append(article)
        return matches

    def _format_date(self, day):
        return f'{day.year}{day.month:02}{day.day:02}'

    def _format_string(self, string):
        return '+'.join(string.lower().split())

    def _format_query(self, args):
        pass


if __name__ == '__main__':
    scrapper = NewYorkTimesScrapper(os.environ['NYT_API_KEY'])
    scrapper.search('win for democrats')
    scrapper.search('win for republicans')
    scrapper.search('win for the democrat')
    scrapper.search('win for the republican')
    scrapper.scrap()
