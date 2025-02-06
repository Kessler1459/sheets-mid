import gspread
import string
from gspread.exceptions import WorksheetNotFound


class GSheet:
    def __init__(self, spreadsheet_id: str, spreadsheet_page: str, is_config= False):
        self.client = gspread.service_account('credentials.json')
        self.sheet = self.client.open_by_key(spreadsheet_id)
        self.init_page(spreadsheet_page, is_config)

    def init_page(self, spreadsheet_page: str, is_config=False):
        try:
            self.worksheet = self.sheet.worksheet(spreadsheet_page)
            if not is_config:
                self.worksheet.clear()
        except WorksheetNotFound:
            self.worksheet = self.sheet.add_worksheet(spreadsheet_page, 1000, 1000)

    def insert_table(self, value: dict) -> None:
        if not value:
            return
        total_inputs = len(value)
        actual_column = len(self.worksheet.row_values(1))+2
        start_letter = 'A' if actual_column == 2 else string.ascii_uppercase[actual_column]
        range_ = f'{start_letter}1:{string.ascii_uppercase[actual_column+total_inputs]}2'
        self.worksheet.update([list(value), list(value.values())], range_name=range_)

    def read_config(self) -> list[dict]:
        return self.worksheet.get_all_records()
