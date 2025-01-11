import re
import json
from typing import Iterable

from bs4 import BeautifulSoup
from utils.http import get_session
from scraping.index.index_provider import IndexProvider


class Rava(IndexProvider):
    #def __init__(self, searchs: Iterable, base_url: str, api_key: str) -> None:
    def __init__(self) -> None:
        self._base_url = 'https://www.rava.com/cotizaciones/dolares'
        #self._searchs = searchs
        self._http = get_session()
    
    def _get_page(self, page: str):
        pass
        

    def update_values(self) -> dict[str, float]:
        response = self._http.get(
                    f'{self._base_url}',
                    #headers={'X-MBX-APIKEY': self._api_key},
                    #params={'symbol': symbol.replace('/', '').upper()}
                )
        #self.indexes = {index: self.get_avg_price(index) for index in self._searchs}
        return self.indexes

    def get_avg_price(self) -> float:
        response = self._http.get(
            f'{self._base_url}'
        )
        list_values = re.split(('&quot;:(.*])'),response.text)
        raw_json = list_values[1].replace('&quot;', '"')
        data = json.loads(raw_json)

        return response.json()['price']
