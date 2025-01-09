from typing import Iterable

import requests

from scraping.index.index_provider import IndexProvider


class Binance(IndexProvider):
    def __init__(self, searchs: Iterable, base_url: str, api_key: str) -> None:
        self._api_key = api_key
        self._base_url = base_url
        self._searchs = searchs
        self._http = requests.session()

    def update_values(self) -> dict[str, float]:
        self.indexes = {index: self.get_avg_price(index) for index in self._searchs}
        return self.indexes

    def get_avg_price(self, symbol: str) -> float:
        url = self._base_url + '/api/v3/avgPrice'
        print("{} {}".format('GET', url)) #TODO LOGGER
        response = self._http.get(
            url,
            headers={'X-MBX-APIKEY': self._api_key},
            params={'symbol': symbol.replace('/', '').upper()}
        )
        return response.json()['price']

