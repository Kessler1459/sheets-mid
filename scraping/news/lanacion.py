import re
from typing import Iterable
from collections import defaultdict

from bs4 import BeautifulSoup

from scraping.news.news_provider import NewsProvider
from utils.http import get_session
from utils.logging_handler import get_logger

logger = get_logger(__name__)
SEARCH_SITEMAP = 'https://www.lanacion.com.ar/sitemap-index.xml'
MAX_NEWS = 2

class LaNacion(NewsProvider):
    def __init__(self, searchs: Iterable):
        self._searchs = searchs
        self._http = get_session()
        self.news = defaultdict(dict)

    def update_values(self) -> dict[str, dict]:
        response = self._http.get(SEARCH_SITEMAP)
        soup = BeautifulSoup(response.text, 'lxml')
        all_articles = soup.find_all('loc', text = re.compile('articles'))
        for arcticles in all_articles:
            soup = BeautifulSoup(self._http.get(arcticles.text).text, 'lxml')
        return super().update_values()
