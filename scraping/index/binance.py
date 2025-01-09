from typing import Iterable

from utils.http import get_session
from scraping.index.index_provider import IndexProvider


class Binance(IndexProvider):
    def __init__(self, searchs: Iterable, base_url: str, api_key: str) -> None:
        self._api_key = api_key
        self._base_url = base_url
        self._searchs = searchs
        self._http = get_session()

    def update_values(self) -> dict[str, float]:
        self.indexes = {index: self.get_avg_price(index) for index in self._searchs}
        return self.indexes

    def get_avg_price(self, symbol: str) -> float:
        response = self._http.get(
            self._base_url + '/api/v3/avgPrice',
            headers={'X-MBX-APIKEY': self._api_key},
            params={'symbol': symbol.replace('/', '').upper()}
        )
        return response.json()['price']
