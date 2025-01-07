import gspread
from gspread.exceptions import WorksheetNotFound

class GSheet:
    def __init__(self, spreadsheet_id: str, spreadsheet_page: str):
        self.client = gspread.service_account('credentials.json')
        self.sheet = self.client.open_by_key(spreadsheet_id)
        self.init_page(spreadsheet_page)

    def init_page(self, spreadsheet_page: str):
        try:
            self.worksheet = self.sheet.worksheet(spreadsheet_page)
        except WorksheetNotFound:
            self.worksheet = self.sheet.add_worksheet(spreadsheet_page, 1000, 1000)
