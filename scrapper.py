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
        self.key = api_key
        self.api_responses = []
        self.articles = set([])
        self.urls = set([])
        self._queries = set([])
        if not self.key:
            raise NoApiKeyException('API key required')

    def search(self, q: str, time_period: int = 2, **kwargs):
        '''
        q (str): query string
        time_period (int): in days, the time period to search
        kwargs:

        '''
        self._queries.add(q)
        begin = datetime.today()
        if time_period > 0:
            begin = begin - timedelta(days=time_period)
        begin = self._format_date(begin)

        q = self._format_string(q)
        query = f'?q={q}&fq={q}&begin_date={begin}&news_desk=politics'
        api_key = f'&api-key={self.key}'
        url = f'{_NYT_API}{query}{api_key}'

        r = requests.get(url)
        self.api_responses.extend(r.json()['response']['docs'])
        self.urls.update(map(lambda x: x['web_url'], self.api_responses))

    def extract_headlines(self):
        headlines = list(map(lambda x: x['headline']['main'], self.api_responses))
        return headlines

    def extract_snippets(self):
        snippets = list(map(lambda x: x['snippet'], self.api_responses))
        return snippets

    def _scrap_articles(self, q):
        for url in self.urls:
            article = self._scrap_article(q, url)
            if article:
                self.articles.add(article)

    def _scrap_article(self, q, url):
        webpage = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(webpage)
        text = '/n'.join(map(lambda x: x.text, soup.find_all('p'))).lower()

        query = re.compile(q)
        if re.search(query, text):
            return text

    def _format_date(self, day):
        return f'{day.year}{day.month:02}{day.day:02}'

    def _format_string(self, string):
        return '+'.join(string.lower().split())

    def _format_query(self, args):
        pass


if __name__ == '__main__':
    api = NewYorkTimesScrapper(os.environ['NYT_API_KEY'])
    api.search('win for democrats')
    api.search('win for republicans')
    api.search('win for the democrat')
    api.search('win for the republican')
