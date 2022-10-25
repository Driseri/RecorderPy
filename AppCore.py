import requests
import json
import os
import psutil
import configparser
import cv2
from PySide2.QtCore import QObject, QAbstractListModel, Qt, Slot, Signal, QModelIndex, Property, QThread
from PySide2.QtGui import *
from threading import Thread
import threading
from datetime import datetime
import time

config = configparser.ConfigParser()
config.read("config.ini")

DISK = config["main"]["disk"]
ROOMS_FILE = config["main"]["cameras"]


#
# class SingleStream(QThread):
#     cv2.namedWindow("main", cv2.WINDOW_NORMAL)
#     cv2.resizeWindow('main', 900, 900)
#     def __init__(self):
#         QThread.__init__(self)
#
#     def run(self):
#
#         while (self.vcap.isOpened() and self.streaming):
#             ret, frame = self.vcap.read()
#
#             cv2.imshow('main', frame)
#             if cv2.waitKey(20) & 0xFF == ord('q'):
#                 break
#
#         self.vcap.release()



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
        self.data = {}
        self.info = {}
        self.connector = connect
        self.select_rtsp = []
        self.streaming = False
        self.isrecord = False
        self.vcap = 0

        cv2.namedWindow("main", cv2.WINDOW_NORMAL)
        cv2.resizeWindow('main', 900, 900)



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
            if (self.streaming):
                self.vcap = cv2.VideoCapture(rtsp)
            else:
                self.vcap = cv2.VideoCapture(rtsp)
                self.viewStream(rtsp)


    def viewStream(self, camera) -> None:

        self.streaming = True

        while (self.vcap.isOpened() and self.streaming):
            ret, frame = self.vcap.read()

            cv2.imshow('main', frame)
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

    @Slot()
    def StartRecording(self):
        print("\n\n")
        for camp in self.select_rtsp:
            #todo ПОТОКИ СДЕЛАТЬ СРОЧНО!!!!

            thr1 = threading.Thread(target=self.recordStream, args=(camp,)).start()
            #recording = Thread(target=self.videoNaming, args=(camp))
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
        out = cv2.VideoWriter(name, fourcc, fps, frame_size)
        time1 = time.perf_counter()
        time2 = time.perf_counter()
        while (vcap.isOpened() and time2 - time1 < 20):
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





