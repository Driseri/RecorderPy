import json
import requests
from pprint import pprint
import pandas as pd
from datetime import datetime
import numpy as np

class GoogleToData():
    def __init__(self):
        self.data1 = pd.read_csv(
            "https://docs.google.com/spreadsheets/d/1QW5-yBn6ip3eeNz-RR4F3hGo80yjXYygM0LL1VKOxJk/export?format=csv")
        self.dataS = self.data1[['git merge ', 'IP-adress', 'Помещение', 'RTSP_1', 'Прокси', 'Звук']]
        self.peremen = {}


        for i, row in self.dataS.iterrows():

            if str(row[2]) != 'nan' and str(row[1]) != 'nan':
                if row[2] not in self.peremen:
                    self.peremen[row[2]] = {'cameras': [], "audio": []}
                    if row[1][len(row[1])-1] == '1':
                        self.peremen[row[2]]['audio'].append({'name': row[0], 'rtsp_main': row[4], "type": "Enc/Dec", 'ip': row[1]})
                    else:
                        if str(row[4]) != 'nan':
                            self.peremen[row[2]]['cameras'].append({'name': row[0], 'rtsp_main': row[4], "type": "ONVI", 'ip': row[1]})
                        elif str(row[3]) != 'nan':
                            self.peremen[row[2]]['cameras'].append({'name': row[0], 'rtsp_main': row[3], "type": "ONVI", 'ip': row[1]})
                else:
                    if row[1][len(row[1])-1] == '1':
                        self.peremen[row[2]]['audio'].append({'name': row[0], 'rtsp_main': row[4], "type": "Enc/Dec", 'ip': row[1]})
                    else:
                        if str(row[4]) != 'nan':
                            self.peremen[row[2]]['cameras'].append({'name': row[0], 'rtsp_main': row[4], "type": "ONVI", 'ip': row[1]})
                        elif str(row[3]) != 'nan':
                            self.peremen[row[2]]['cameras'].append({'name': row[0], 'rtsp_main': row[3], "type": "ONVI", 'ip': row[1]})


        #pprint(self.peremen)

        with open('naming1.json', 'w') as fp:
            json.dump(self.peremen, fp, ensure_ascii=False)



qwerty = GoogleToData()
