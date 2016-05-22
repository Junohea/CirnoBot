from conf import config
import gspread
from datetime import datetime, date
from oauth2client.service_account import ServiceAccountCredentials


class Googspread(object):
    def __init__(self):
        sheetjson = config['API']['spreadsheet_json']
        spreadsheet_base = config['API']['spreadsheet_base']
        spreadsheet_schedule = config['API']['spreadsheet_schedule']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            sheetjson, 'https://spreadsheets.google.com/feeds')
        gc = gspread.authorize(credentials)
        self.base = gc.open_by_key(spreadsheet_base)
        self.schedule = gc.open_by_key(spreadsheet_schedule)
        self.base_sheet = self.base.get_worksheet(2)
        self.shedule_sheet = self.schedule.get_worksheet(0)

    def extenddata(self, data):
        cut = data.split('|')
        title = cut[0].rstrip()
        if len(cut) > 1:
            series = cut[1].split(',')
            return title, series
        else:
            return title

    def frombase(self, data):
        data = self.extenddata(data)
        anime_list = self.base_sheet.col_values(1)
        if type(data) is str and data in anime_list:
            pos = anime_list.index(data)
            series_list = self.base_sheet.row_values(pos + 1)
            result = [ser for ser in series_list[2:] if ser]
            return result
        elif type(data) is tuple and data[0] in anime_list:
            title = data[0]
            series = data[1]
            pos = anime_list.index(title)
            row = self.base_sheet.row_values(pos + 1)
            series_list = row[2:]
            serv = [int(i) for i in series]
            result = [series_list[i - 1] for i in serv]
            return result
        else:
            return

    def datashedule(self):
        now = datetime.now()
        today_list = self.shedule_sheet.col_values(date.isoweekday(now))
        return today_list
