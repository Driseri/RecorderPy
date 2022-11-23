import json
import requests
from pprint import pprint
import pandas as pd
from datetime import datetime


class GoogleToData():
    def __init__(self):
        self.data1 = pd.read_csv(
            "https://docs.google.com/spreadsheets/d/1QW5-yBn6ip3eeNz-RR4F3hGo80yjXYygM0LL1VKOxJk/export?format=csv")
        self.data1 = self.data1[['Помещение','Чем закрашивать A-столбец камер','Прокси','Доступность proxy-ссылки','RTSP_1','Звук','Наименование','Тип']]
        self.rooms = self.data1.Помещение.unique()
        self.db_rooms = {}

        for i, row in self.data1.iterrows():
            if str(row[1]) != 'RED' and type(row[0]) != float:
                if str(row[0]) in self.db_rooms:
                    if str(row[5]) == 'Да' and str(row[2])[len(str(row[2]))-1] == '1':
                        if str(row[1]) == 'GREEN':
                            self.db_rooms[row[0]]['audio'].append({'name': str(row[6]),
                                                                    'rtsp_main': str(row[2]),
                                                                "type": str(row[7]) })
                        else:
                            self.db_rooms[row[0]]['audio'].append({'name': str(row[6]),
                                                                   'rtsp_main': str(row[4]),
                                                                "type": str(row[7])})
                    else:
                        if str(row[1]) == 'GREEN':
                            self.db_rooms[row[0]]['cameras'].append({'name': str(row[6]),
                                                                    'rtsp_main': str(row[2]),
                                                                "type": str(row[7]) })
                        else:
                            self.db_rooms[row[0]]['cameras'].append({'name': str(row[6]),
                                                                   'rtsp_main': str(row[4]),
                                                                "type": str(row[7])})
                else:
                    if str(row[5]) == 'Да' and str(row[2])[len(str(row[2]))-1] == '1':
                        if str(row[1]) == 'GREEN':
                            self.db_rooms[str(row[0])] = {'cameras': [],
                                                     'audio': [{'name': str(row[6]),
                                                                'rtsp_main': str(row[2]),
                                                                "type": str(row[7])}]}
                        else:
                            self.db_rooms[str(row[0])] = {'cameras': [],
                                                     'audio': [{'name': str(row[6]),
                                                                'rtsp_main': str(row[4]),
                                                                "type": str(row[7])}]}
                    else:
                        if str(row[1]) == 'GREEN':
                            self.db_rooms[str(row[0])] = {'cameras': [{'name': str(row[6]),
                                                                'rtsp_main': str(row[2]),
                                                                "type": str(row[7])}],
                                                     'audio': []}
                        else:
                            self.db_rooms[str(row[0])] = {'cameras': [{'name': str(row[6]),
                                                                  'rtsp_main': str(row[4]),
                                                                  "type": str(row[7])}],
                                                     'audio': []}

        pprint(self.db_rooms)
        naming = "db_rooms"+str(datetime)+'.json'
        with open('naming.json', 'w') as fp:
            json.dump(self.db_rooms, fp, ensure_ascii=False)


    def updateCSV(self):
        self.data1 = pd.read_csv(
            "https://docs.google.com/spreadsheets/d/1QW5-yBn6ip3eeNz-RR4F3hGo80yjXYygM0LL1VKOxJk/export?format=csv")

    def workingLink(self, ):
        pass

    def modeling(self):
        pass


qwerty = GoogleToData()


# print(data)
#
# print(data.columns)
#
# print(data[['Помещение','Наименование','RTSP_1']])