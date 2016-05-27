from conf import config
import gspread
from datetime import datetime, date
from oauth2client.service_account import ServiceAccountCredentials
from random import choice


class Googspread(object):

    def connect(self):
        sheetjson = config['API']['spreadsheet_json']
        spreadsheet_base = config['API']['spreadsheet_base']
        spreadsheet_schedule = config['API']['spreadsheet_schedule']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            sheetjson, 'https://spreadsheets.google.com/feeds')
        gc = gspread.authorize(credentials)
        base = gc.open_by_key(spreadsheet_base)
        schedule = gc.open_by_key(spreadsheet_schedule)
        self.base_sheet = base.get_worksheet(2)
        self.shedule_sheet = schedule.get_worksheet(0)
        self.anime_list = self.base_sheet.col_values(1)

    def extenddata(self, data):
        self.connect()
        cut = data.split('|')
        title = cut[0].rstrip()
        if len(cut) > 1 and '-' not in cut[1]:
            series = cut[1].split(',')
            data = title, series
            result = self.seriesdb(data)
            return result
        elif len(cut) > 1:
            series = cut[1].split('-')
            if len(series) == 2:
                data = title, series
                result = self.rangedb(data)
                return result
        elif data == 'random':
            return self.randomdb()
        else:
            return self.getallseries(title)

    def getallseries(self, data):
        if data in self.anime_list:
            pos = self.anime_list.index(data)
            series_list = self.base_sheet.row_values(pos + 1)
            result = [ser for ser in series_list[2:] if ser]
            return result

    def seriesdb(self, data):
        if data[0] in self.anime_list:
            title = data[0]
            series = data[1]
            pos = self.anime_list.index(title)
            row = self.base_sheet.row_values(pos + 1)
            series_list = row[2:]
            serv = [int(i) for i in series]
            result = [series_list[i - 1] for i in serv]
            return result
        else:
            return

    def rangedb(self, data):
        if data[0] in self.anime_list:
            title = data[0]
            serrange = data[1]
            start = int(serrange[0])
            end = int(serrange[1])
            pos = self.anime_list.index(title)
            row = self.base_sheet.row_values(pos + 1)
            series_list = row[2:]
            result = [ser for ser in series_list[start-1:end] if ser]
            return result

    def randomdb(self):
        data = [i for i in self.base_sheet.col_values(3) if i.startswith('http')]
        result = choice(data).split()
        return result

    def datashedule(self):
        now = datetime.now()
        today_list = self.shedule_sheet.col_values(date.isoweekday(now))
        return today_list
