import os

from data.gsheet import GSheet

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = os.environ['SPREADSHEET']
SPREADSHEET_PAGE = os.environ['SPREADSHEET_PAGE']

gsheet = GSheet(SPREADSHEET_ID, SPREADSHEET_PAGE)
gsheet.worksheet.append_row(['1', '2', '3'])
