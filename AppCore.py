#vers1.1.1
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
    #
    pass



class SingleStream(QObject):
    '''Отдельнй поток под вывод изображения с камеры'''
    running = False
    newTextAndColor = Signal(ndarray)
    rtsp = "rtsp://172.18.191.63:554/Streaming/Channels/1"

    vcap = cv2.VideoCapture(rtsp)
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
        #todo Должно принимать еще всякие названия
        if rtsp in self.select_rtsp:
            self.select_rtsp.remove([rtsp,name])
        else:
            self.select_rtsp.append([rtsp,name])
        print(self.select_rtsp)


    #todo Добавить кноку обнуления выбора


    @Slot(str,str)
    def buttonReact(self, rtsp, name):
        if (self.isrecord):
            #todo Добавить запись потоков
            pass
        else:
            self.singleStream.chngStream(rtsp)
            # if (self.streaming):
            #     try:
            #         self.vcap = cv2.VideoCapture(rtsp)
            #     except:
            #         logging.ERROR('Поток с камеры не берется')
            # else:
            #     try:
            #         self.vcap = cv2.VideoCapture(rtsp)
            #         self.viewStream(rtsp)
            #     except:
            #         logging.ERROR('Поток с камеры не берется')


    def viewStream(self, camera) -> None:

        self.streaming = True

        while (self.vcap.isOpened() and self.streaming):
            ret, frame = self.vcap.read()
            # print(type(frame))
            try:
                cv2.imshow('main', frame)
            except:
                logging.ERROR('Вывод кадра накрылся')
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

        self.vcap.release()


    @Slot()
    def recStop(self):
        #print("QWEQWEQWE")
        self.streaming = False

    def getFreeSpace(self) -> str:
        free = psutil.disk_usage(DISK).free/(1024*1024*1024)
        return (f"{free:.4} Gb free on disk {DISK}")


    def videoNaming(self, name) -> str:
        time = datetime.now()
        return("{}-{}-{}-{}:{}-{}".format(time.year, time.month,time.day,time.hour,time.minute,name))
    #todo Создание имен

    @Slot(ndarray)
    def addNewTextAndColor(self, string):
        cv2.imshow('main', string)


    @Slot()
    def StartRecording(self):
        pass
        # thread = QThread()
        # singleStream = SingleStream()
        # singleStream.moveToThread(thread)
        # self.nextCameraView.connect(singleStream.chooseCamera)
        # thread.started.connect(singleStream.run)
        # thread.start()
        # self.nextCameraView.emit(self.select_rtsp[0][0])
        # for camp in self.select_rtsp:
        #     #todo ПОТОКИ СДЕЛАТЬ СРОЧНО!!!!
        #     pass
        #     #recording = Thread(target=self.videoNaming, args=(camp))
            #recording.start()
            #th = Thread(target=self.recordStream, args=())




    def recordStream(self,args) -> None:
        #todo Дописать запись (Добавить многопоточность)
        #todo Масштаб вывода настроить


        name = self.videoNaming(args[1])
        name = name + '.avi'
        print(args[0])
        vcap = cv2.VideoCapture(args[0])
        frame_width = int(vcap.get(3))
        frame_height = int(vcap.get(4))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        frame_size = (frame_width, frame_height)
        fps = vcap.get(cv2.CAP_PROP_FPS)
        out = cv2.VideoWriter('name.avi', fourcc, fps, frame_size)
        time1 = time.perf_counter()
        time2 = time.perf_counter()
        while (vcap.isOpened() and time2 - time1 < 10):
            time2 = time.perf_counter()
            ret, frame = vcap.read()
            out.write(frame)

        print(name+'IS OVER')
        vcap.release()
        out.release()
        # while (vcap.isOpened() and self.isrecord):
        #     ret, frame = vcap.read()
        #     #res = cv2.resize(frame, dsize=(500,500), interpolation=cv2.INTER_CUBIC)
        #     cv2.imshow('main', frame)
        #     if cv2.waitKey(20) & 0xFF == ord('q'):
        #         break
        #





