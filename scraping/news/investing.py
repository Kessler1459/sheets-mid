import re
from typing import Iterable
from collections import defaultdict

from bs4 import BeautifulSoup

from scraping.news.news_provider import NewsProvider
from utils.http import get_session
from utils.logging_handler import get_logger

logger = get_logger(__name__)
SEARCH_URL = 'https://www.investing.com/search/?q={}&tab=news'
MAX_NEWS = 2

class Investing(NewsProvider):
    def __init__(self, searchs: Iterable):
        self._searchs = searchs
        self._http = get_session()
        self.news = defaultdict(dict)

    def update_values(self) -> dict[str, dict]:
        for index in self._searchs:
            logger.debug("Searching %s news", index)
            res = self._http.get(SEARCH_URL.format(index))
            soup = BeautifulSoup(res.text, 'html.parser')
            anchors = soup.select('.searchSection a.title')
            links = [f"https://www.investing.com{anchor['href']}" for anchor in anchors if '{' not in anchor['href']]
            for link in links:
                res = self._http.get(link)
                soup = BeautifulSoup(res.text, 'html.parser')
                body = soup.select_one('.article_container')
                if not body:
                    continue
                if re.search(r"\W?{}\W".format(index), body.text, re.IGNORECASE): #talvez volver a lo anterior y que filtre bien gemini
                    self.news[index][link] = body.text
                if index in self.news and len(self.news[index]) == MAX_NEWS:
                    break
        return self.news