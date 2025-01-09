import os

from data.gsheet import GSheet
from scraping.index.binance import Binance


SPREADSHEET_ID = os.environ['SPREADSHEET']
SPREADSHEET_PAGE = os.environ['SPREADSHEET_PAGE']
BINANCE_API_KEY = os.environ['BINANCE_API_KEY']
BINANCE_SECRET_KEY = os.environ['BINANCE_SECRET_KEY']
BINANCE_ROOT_URL= os.environ['BINANCE_ROOT_URL']

binance = Binance(['ETHUSDT'], BINANCE_ROOT_URL, BINANCE_API_KEY)
res = binance.update_values()

gsheet = GSheet(SPREADSHEET_ID, SPREADSHEET_PAGE)
gsheet.worksheet.append_row(['1', '2', '3'])
