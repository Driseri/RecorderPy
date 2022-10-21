import requests
import json
import os
import psutil
import configparser
import cv2
import time
from PySide2.QtCore import QObject, QAbstractListModel, Qt, Slot, Signal, QModelIndex, Property

config = configparser.ConfigParser()
config.read("config.ini")

DISK = config["main"]["disk"]
ROOMS_FILE = config["main"]["cameras"]



class Connector():
    def __init__(self):
        self.newListCam = []

    def changeList(self, newList):
        self.newListCam = newList.copy()

    def getList(self):
        return self.newListCam


class VideoModel(QAbstractListModel):

    NameRole = Qt.UserRole + 1
    TypeRole = Qt.UserRole + 2
    RtspRole = Qt.UserRole + 3

    modelChanged = Signal()



    def __init__(self,connect, parent=None):
        super().__init__(parent)
        self.connector = connect
        self._entries = []

    def rowCount(self, parent=QModelIndex()):
        if parent.isValid(): return 0
        return len(self._entries)

    def data(self, index, role=Qt.DisplayRole):
        if 0 <= index.row() < self.rowCount() and index.isValid():
            item = self._entries[index.row()]
            if role == VideoModel.NameRole:
                return item["name"]
            elif role == VideoModel.TypeRole:
                return item["type"]
            elif role == VideoModel.RtspRole:
                return item["rtsp"]

    def roleNames(self):
        roles = dict()
        roles[VideoModel.NameRole] = b"name"
        roles[VideoModel.TypeRole] = b"type"
        roles[VideoModel.RtspRole] = b"rtsp"
        return roles


    def getConnector(self):
        pprint(self.connector.getList())

    @Slot()
    def addCamera(self):
        cams = self.connector.getList()
        self.beginInsertRows(QModelIndex(), 0, len(cams)-1)
        self._entries = cams
        self.endInsertRows()

    @Slot()
    def deleteCameras(self):
        if self.rowCount():
            self.beginRemoveColumns(QModelIndex(), 0, self.rowCount())
            del self._entries[self.rowCount()-1]
            self.endRemoveRows()




class AppCore(QObject):
#    listview = Signal(str, arguments=['cam'])

    def __init__(self,connect, parent=None):
        super(AppCore, self).__init__(parent)
        self.data = {}
        self.info = {}
        self.connector = connect
        self.select_rtsp = []
        self.record = False


    @Slot(str)
    def getCams(self,str):
        list = []
        for camera in self.info[str]['cameras']:
            list.append({"name": camera['name'],
                         "type": camera['type'],
                         "rtsp": camera['rtsp_main']})

        #Изменить отправку на изменение
        self.connector.changeList(list)



    def getCameras(self) -> dict:
        with open(ROOMS_FILE, 'r') as file:
            info = json.loads(file.read())
            self.info = info
            return info

    def updateCameras(self) -> None:
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

            json.dump(info, file)

    @Slot(str)
    def addSelect(self, rtsp) -> None:
        #todo Должно принимать еще всякие названия
        if rtsp in self.select_rtsp:
            self.select_rtsp.remove(rtsp)
        else:
            self.select_rtsp.append(rtsp)
        print(self.select_rtsp)


    #todo Метод для начала\остановки записи
    @Slot()
    def recStart(self):
        self.record = True
        self.recordStream('qwe')

    @Slot()
    def recStop(self):
        self.record = False

    def getFreeSpace(self) -> str:
        free = psutil.disk_usage(DISK).free/(1024*1024*1024)
        return (f"{free:.4} Gb free on disk {DISK}")


    def videoNaming(self) -> str:
        pass
    #todo Создание имен


    def recordStream(self, rtsp) -> None:
        #todo Дописать запись (Добавить многопоточность)
        vcap = cv2.VideoCapture(self.select_rtsp[0])
        frame_width = int(vcap.get(3))
        frame_height = int(vcap.get(4))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        frame_size = (frame_width, frame_height)
        fps = vcap.get(cv2.CAP_PROP_FPS)
        #out = cv2.VideoWriter('output.avi', fourcc, fps, frame_size)

        # while (1):
        #     time2 = time.perf_counter()
        #     ret, frame = vcap.read()
        #     out.write(frame)
        #     if time2 - time1 > 10:
        #         break

        while (vcap.isOpened() and self.record):
            ret, frame = vcap.read()
            cv2.imshow('frame', frame)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
        vcap.release()
        #out.release()

