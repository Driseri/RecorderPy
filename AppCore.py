import requests
import json
import os
import sys
import psutil
import configparser
import cv2
from PySide2.QtCore import QObject, QAbstractListModel, Qt, Slot, Signal, QModelIndex, Property, QThread
from PySide2.QtGui import *
from numpy import *
from datetime import datetime
import time
import logging

config = configparser.ConfigParser()
config.read("config.ini")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)


DISK = config["main"]["disk"]
ROOMS_FILE = config["main"]["cameras"]


class SavingStream(QThread):
    def __init__(self, rtsp, name, parent =None):
        super(SavingStream, self).__init__(parent)
        self.rtsp = rtsp
        self.isRecord = True
        try:
            self.vcap = cv2.VideoCapture(self.rtsp)
        except:
            logger.error('Problem in read rtsp (SavingStream)')
        self.frame_width = int(self.vcap.get(3))
        self.frame_height = int(self.vcap.get(4))
        self.fourcc = cv2.VideoWriter_fourcc(*'H264')
        self.frame_size = (self.frame_width, self.frame_height)
        self.fps = self.vcap.get(cv2.CAP_PROP_FPS)
        self.out = cv2.VideoWriter(name, self.fourcc, self.fps, self.frame_size)

    def videoNaming(self, name) -> str:
        time = datetime.now()
        #todo Настроить наименование видео
        return("{}-{}-{}-{}:{}-{}.avi".format(time.year, time.month,time.day,time.hour,time.minute,name))

    def stopRecording(self):
        self.isRecord = False

    def run(self):
        while self.isRecord:
            ret, frame = self.vcap.read()
            self.out.write(frame)

        self.vcap.release()
        self.out.release()

        logger.info('end of recording')



class SingleStream(QObject):
    '''Отдельнй поток под вывод изображения с камеры'''
    running = False
    newTextAndColor = Signal(ndarray)
    rtsp = ""

    vcap = cv2.VideoCapture(0)
    def __init__(self, parent=None):
        super(SingleStream, self).__init__(parent)
    def chngStream(self, str):
        self.rtsp = str
        self.vcap = cv2.VideoCapture(self.rtsp)

    # method which will execute algorithm in another thread
    def run(self):
        while True:
            # send signal with new text and color from aonther thread
            # self.newTextAndColor.emit(
            #     self.common_string
            # )
            ret, frame = self.vcap.read()
            self.newTextAndColor.emit(frame)
            QThread.msleep(10)
        self.vcap.release()







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
        print(self.connector.getList())

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
    def __init__(self,connect, parent=None):
        super(AppCore, self).__init__(parent)
        # self.thread = QThread()
        self.data = {}
        self.info = {}
        self.connector = connect
        self.select_rtsp = []
        self.record_threads = []
        self.streaming = False
        self.isrecord = False
        self.vcap = 0
        cv2.namedWindow("main", cv2.WINDOW_NORMAL)
        cv2.resizeWindow('main', 900, 900)
        cv2.moveWindow('main', 500, 0)
        self.thread = QThread()
        # create object which will be moved to another thread
        self.singleStream = SingleStream()
        # move object to another thread
        self.singleStream.moveToThread(self.thread)
        # after that, we can connect signals from this object to slot in GUI thread
        self.singleStream.newTextAndColor.connect(self.addNewTextAndColor)
        # connect started signal to run method of object in another thread
        self.thread.started.connect(self.singleStream.run)
        # start thread
        self.thread.start()






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

    @Slot()
    def setRecord(self):
        if self.isrecord:
            self.isrecord = False
        else:
            self.isrecord = True


    @Slot(str,str)
    def addSelect(self, rtsp, name) -> None:
        if rtsp in self.select_rtsp:
            self.select_rtsp.remove([rtsp,name])
        else:
            self.select_rtsp.append([rtsp,name])
        print(self.select_rtsp)


    #todo Добавить кноку обнуления выбора
    @Slot()
    def clearSelected(self) -> None:
        self.select_rtsp.clear()
        print(self.select_rtsp)

    @Slot(str,str)
    def buttonReact(self, rtsp, name):
        if (self.isrecord):
            #todo Добавить запись потоков
            pass
        else:
            self.singleStream.chngStream(rtsp)

    def getFreeSpace(self) -> str:
        free = psutil.disk_usage(DISK).free/(1024*1024*1024)
        return (f"{free:.4} Gb free on disk {DISK}")


    @Slot(ndarray)
    def addNewTextAndColor(self, string):
        cv2.imshow('main', string)

    @Slot()
    def recStop(self):
        logger.info('ending of recordings')
        for threads in self.record_threads:
            threads.stopRecording()

    @Slot()
    def StartRecording(self):
        logger.info('trigger of slot StartRecording')
        string = 'naming'
        integer = 1
        for rtsp in self.select_rtsp:
            threadRecord = SavingStream(rtsp[0],(string+str(integer)+'.avi'))
            threadRecord.start()
            self.record_threads.append(threadRecord)
            integer = integer + 1
