import os

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

gemini = Gemini(GEMINI_KEY, GEMINI_MODEL)

insights = {}
remaining_keys = set(inputs)
for news_source in (LaNacion, Investing,):
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
    for k, insight in res.items():
        if insight:
            insights[k] = insight
    remaining_keys -= set(insights.keys())
    if not remaining_keys:
        break



#gsheet = GSheet(SPREADSHEET_ID, SPREADSHEET_PAGE)
