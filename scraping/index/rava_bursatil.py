import re
import json
import time
from typing import Iterable, Optional

from bs4 import BeautifulSoup
from utils.http import get_session
from scraping.index.index_provider import IndexProvider
from utils.logging_handler import get_logger

logger = get_logger(__name__)


class Rava(IndexProvider):
    def __init__(self) -> None:
        self.base_url = 'https://www.rava.com/cotizaciones'
        self.urls = {
            f'{self.base_url}/dolares',
            f'{self.base_url}/acciones-argentinas',
            f'{self.base_url}/cripto',
            f'{self.base_url}/cedears',
            f'{self.base_url}/bonos',
            f'{self.base_url}/opciones',
            f'{self.base_url}/letras',
            f'{self.base_url}/futuros',
            f'{self.base_url}/mercados-globales'
        }
        self._http = get_session()

        
    def _filter_dict(self, data: dict) -> dict:
        result = {}
        for key, value in data.items():
            if isinstance(value, list):
                result[key] = value
        return result

    def update_values(self) -> dict[str, Optional[float]]:
        tick = time.time()
        results = {}
        for url in self.urls:
            data = self._get_avg_price(url)
            if 'count' in data and not data['count']:
                continue
            filtered_data = self._filter_dict(data)
            results.update({body[""]: (None if isinstance(body['ultimo'], str) else body['ultimo']) for symbol in filtered_data for body in filtered_data[symbol]})
        logger.info(f'runtime update_values: {time.time()-tick}')
        return results

    def _get_avg_price(self, url: str) -> dict:
        response = self._http.get(url)
        try:
            list_values = re.split((':datos=\"(.*})'),response.text)
            raw_json = list_values[1].replace('&quot;', '"')
            data = json.loads(raw_json)
            return data
        except Exception as e:
            logger.error(e)
            return {
                'body' : [],
                'link' : '',
                'count' : 0,
                'exactime' : 0.0
            }
