import requests
import json
import os
import psutil
from PySide2.QtCore import QObject, QAbstractListModel, Qt, Slot, Signal

DISK = "C:"
ROOMS_FILE = "db-rooms.json"


#class CamerModel(QAbstractListModel):

#    def __init__(self, rooms):
#            super(CamerModel, self).__init__()
#            print(rooms)
#            self.rooms = rooms.keys()

#    def rowCount(self, parent=None, *args, **kwargs):
#            return len(self.rooms)




class AppCore(QObject):
    listview = Signal(str, arguments=['getCams'])

    @Slot(str)
    def getCams(self,str):
        print(self.info['504'])
        self.listview.emit(self.info[str])

    def __init__(self):
        QObject.__init__(self)
        self.data = {}
        self.info = {}

    def getCameras(self) -> dict:
        with open(ROOMS_FILE, 'w') as file:
            response = requests.get('https://nvr.miem.hse.ru/api/erudite/equipment',
                                    headers={'key': os.environ.get('ERUDITE_KEY')})

            response = response.content.decode('utf8').replace("'", '"')
            data = json.loads(response)
            info = {}

            for room in data:
                if room['room_name'] in info:
                    info[room["room_name"]]['cameras'].append(room)
                else:
                    info[str(room["room_name"])] = {
                        "cameras": [room],
                        "audio": []
                    }
            self.info = info
            return info


    #OpenCV
    #Goto Отображение Qtvideo/

    def getFreeSpace(self) -> str:
        free = psutil.disk_usage(DISK).free/(1024*1024*1024)
        return (f"{free:.4} Gb free on disk {DISK}")


