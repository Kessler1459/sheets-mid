import os

from data.gsheet import GSheet
from scraping.index.binance import Binance
from scraping.index.rava_bursatil import Rava
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

rava = Rava()
dict_results = rava.update_values()
gemini = Gemini(GEMINI_KEY, GEMINI_MODEL)
gsheet = GSheet(SPREADSHEET_ID, SPREADSHEET_PAGE)
