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
        soup = BeautifulSoup(response.text, 'html.parser')
        all_articles = soup.find_all('loc', text = re.compile('articles'))
        notices_urls = set()
        for arcticles in all_articles:
            soup = BeautifulSoup(self._http.get(arcticles.text).text, 'html.parser')
            economy_notices = soup.find_all('loc', text = re.compile('/economia/'))
            notices_urls.update(economy_notices)
        for loc in notices_urls:
            body = BeautifulSoup(self._http.get(loc.text).text, 'html.parser')
            body = self.unify_body(body)
            if not body:
                raise ValueError('No vino el cuerpito.')
            for index in self._searchs:
                if re.search(r"\W?{}\W".format(index), body, re.IGNORECASE):
                    self.news[index][loc.text] = body
                if index in self.news and len(self.news[index]) == MAX_NEWS:
                    break
        return self.news

    def unify_body(self, soup:BeautifulSoup) -> str | None:
        body_note = soup.select_one('.cuerpo__nota').text
        return body_note.split('Seguí leyendo')[0]
