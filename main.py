import argparse
import os
import json

from data.gsheet import GSheet
from scraping.index.binance import Binance
from scraping.index.rava_bursatil import Rava
from scraping.news.investing import Investing
from scraping.news.lanacion import LaNacion
from utils.gemini import Gemini
from utils.logging_handler import get_logger, setup_logger

root_logger = get_logger()
setup_logger(root_logger)


SPREADSHEET_ID = os.environ['SPREADSHEET']
SPREADSHEET_PAGE = os.environ['SPREADSHEET_PAGE']
BINANCE_API_KEY = os.environ['BINANCE_API_KEY']
BINANCE_SECRET_KEY = os.environ['BINANCE_SECRET_KEY']
BINANCE_ROOT_URL = os.environ['BINANCE_ROOT_URL']
GEMINI_KEY = os.environ['GEMINI_KEY']
GEMINI_MODEL= os.environ['GEMINI_MODEL']

if not all((SPREADSHEET_ID, SPREADSHEET_PAGE, BINANCE_API_KEY, BINANCE_SECRET_KEY, BINANCE_ROOT_URL, GEMINI_KEY, GEMINI_MODEL)):
    raise EnvironmentError("Missing environment variables")


parser = argparse.ArgumentParser(description="Scrap stocks, cryptos and indexes news, and generate insights")
parser.add_argument('inputs', type=str, nargs='+', help="List of stocks, cryptos and indexes to search")
parser.add_argument('--insights', type=str, nargs='+', default=None, help="List of stocks, cryptos and indexes to generate insights")
args = parser.parse_args()
symbol_inputs = args.inputs or []
insight_inputs = args.insights or []

# SYMBOL SCRAPING
remaining_keys = set(symbol_inputs)
indexes = {}
for args, provider_class in (((), Rava), ((BINANCE_ROOT_URL,BINANCE_API_KEY), Binance)):
    root_logger.info("Updating indexes for %s from %s", remaining_keys, provider_class.__name__)
    provider_instance = provider_class(remaining_keys, *args)
    values = provider_instance.update_values()
    indexes.update({k: float(v) for k,v in values.items() if v})
    remaining_keys -= set(values.keys())
    if not remaining_keys:
        break

# INSIGHTS
gemini = Gemini(GEMINI_KEY, GEMINI_MODEL)
insights = {}
remaining_keys = set(insight_inputs)
for news_source in (Investing, ):
    root_logger.info("Updating news %s from %s", remaining_keys, news_source.__name__)
    source = news_source(remaining_keys)
    news = source.update_values()
    prompt = f"""
        Based on a JSON with stock names, indexes and cryptos as keys and multiple news related to them as value,
        i need a short insight about the news from everyone of the keys.
        STEPS:
        1-Filter the news that are not related to the stock symbols, indexes or crypto that we are looking for, if there is no info about a symbol, index or crypto, set the field as null
        2-You MUST answer with a JSON with same keys as the initial, but with a string value as a resume and insights from multiple news for that symbol.
        IMPORTANT:
        -Never use info that is not in the provided news
        -Only resume and set keys that are in the provided DATA
        JSON FORMAT:
            <SYMBOL>: <INSIGHT>,
            <SYMBOL2>: <INSIGHT2>,
            <SYMBOL3>: <INSIGHT3>
        DATA:{json.dumps(news)}
    """
    res = gemini.json_request(prompt)
    insights.update({k: v for k, v in res if v})
    remaining_keys -= set(insights.keys())
    if not remaining_keys:
        break



#gsheet = GSheet(SPREADSHEET_ID, SPREADSHEET_PAGE)
