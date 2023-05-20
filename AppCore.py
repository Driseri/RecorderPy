import requests
import json
import os
import sys
import psutil
import configparser
import cv2
import vlc
from PySide2.QtCore import QObject, QAbstractListModel, Qt, Slot, Signal, QModelIndex, Property, QThread
from PySide2.QtGui import *
from numpy import *
from datetime import datetime
from TableModel import TableModel
import time
import logging
import subprocess
from pprint import pprint

config = configparser.ConfigParser()
config.read("config.ini")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'

DISK = config["main"]["disk"]
ROOMS_FILE = config["main"]["cameras"]
SAVE_PATH = config["main"]["savePath"]


class FFplayer(QThread):

    def __init__(self, parent=None):
        super(FFplayer, self).__init__(parent)
        self.isStart = True
        self.isChange = False
        self.currRtsp = ''
        #'subprocess.Popen(['ffplay', 'rtsp://172.18.191.38/306/3', '-an', '-x', '1280'], stdin=subprocess.PIPE)'
        self.prev1 = ''


    def play(self, rtsp):
        self.currRtsp = rtsp
        self.isChange = True



    def run(self):
        while True:
            if self.isChange:
                prev2 = subprocess.Popen(['ffplay', self.currRtsp, '-an', '-x', '1280'], stdin=subprocess.PIPE)
                time.sleep(4)
                if self.prev1 != '':
                    self.prev1.kill()
                self.prev1 = prev2
                self.isChange = False




class Player(QThread):
    def __init__(self, *args, parent=None):
        super(Player, self).__init__(parent)
        if args:
            instance = vlc.Instance(*args)
            self.media = instance.media_player_new()
        else:
            self.media = vlc.MediaPlayer()

    # Set the URL address or local file path to be played, and the resource will be reloaded every time it is called
    def set_uri(self, uri):
        self.media.set_mrl(uri)

    # Play success returns 0, failure returns -1
    def play(self, path=None):
        if path:
            self.set_uri(path)
            return self.media.play()
        else:
            return self.media.play()

    # time out
    def pause(self):
        self.media.pause()

    # Restore
    def resume(self):
        self.media.set_pause(0)

    # stop
    def stop(self):
        self.media.stop()

    # Release resources
    def release(self):
        return self.media.release()

    # Is it playing
    def is_playing(self):
        return self.media.is_playing()

    # Elapsed time, return millisecond value
    def get_time(self):
        return self.media.get_time()

    # Drag the specified millisecond value to play. Return 0 on success, -1 on failure (note that only the current multimedia format or streaming media protocol support will take effect)
    def set_time(self, ms):
        return self.media.get_time()

    # The total length of audio and video, returns the value in milliseconds
    def get_length(self):
        return self.media.get_length()

    # Get the current volume (0~100)
    def get_volume(self):
        return self.media.audio_get_volume()

    # Set the volume (0~100)
    def set_volume(self, volume):
        return self.media.audio_set_volume(volume)

    # Return to the current state: playing; paused; other
    def get_state(self):
        state = self.media.get_state()
        if state == vlc.State.Playing:
            return 1
        elif state == vlc.State.Paused:
            return 0
        else:
            return -1

    # Current playback progress. Returns a floating point number between 0.0 and 1.0
    def get_position(self):
        return self.media.get_position()

    # Drag the current progress and pass in a floating point number between 0.0 and 1.0 (note that only the current multimedia format or streaming protocol support will take effect)
    def set_position(self, float_val):
        return self.media.set_position(float_val)

    # Get the current file playback rate
    def get_rate(self):
        return self.media.get_rate()

    # Set the playback rate (for example: 1.2, which means to speed up the playback by 1.2 times)
    def set_rate(self, rate):
        return self.media.set_rate(rate)

    # Set the aspect ratio (such as "16:9", "4:3")
    def set_ratio(self, ratio):
        self.media.video_set_scale(0)  # Must be set to 0, otherwise the screen width and height cannot be modified
        self.media.video_set_aspect_ratio(ratio)

    # Register listener
    def add_callback(self, event_type, callback):
        self.media.event_manager().event_attach(event_type, callback)

    # Remove listener
    def remove_callback(self, event_type, callback):
        self.media.event_manager().event_detach(event_type, callback)


    def run(self):
        self.play("rtsp://172.18.191.38/305/2")
        while True:
            pass



class SavingCoder(QThread):
    def __init__(self, audio, name, args, parent=None):
        super(SavingCoder, self).__init__(parent)
        self.audio = audio
        self.args = args
        self.name = name
        self.isRecord = True

    def stopRecording(self):
        self.isRecord = False

    def run(self):
        process_audio = subprocess.Popen(['ffmpeg', '-thread_queue_size', '1024', '-use_wallclock_as_timestamps',
                                          '1', '-rtsp_transport', 'tcp', '-i', self.audio, '-map_metadata', '0',
                                          '-c', 'copy', SAVE_PATH + 'aud' + self.name], stdin=subprocess.PIPE)

        while True:
            if self.isRecord == False:
                process_audio.communicate(b'q')
                break





class SavingStream(QThread):
    def __init__(self, rtsp, name, audio, args, parent=None):
        super(SavingStream, self).__init__(parent)
        self.rtsp = rtsp
        self.isRecord = True
        self.isMerge = True
        self.name = name
        self.audio = audio
        self.args = args
        self.path = os.path.abspath(os.curdir)

    def stopRecording(self):
        self.isRecord = False

    def run(self):
        process_video = subprocess.Popen(['ffmpeg', '-thread_queue_size', '1024', '-use_wallclock_as_timestamps',
                                          '1', '-rtsp_transport', 'tcp', '-i', self.rtsp,'-map_metadata', '0', '-map', '0', '-c:v', 'copy', '-an',
                                          SAVE_PATH + self.name], stdin=subprocess.PIPE)


        while True:
            if self.isRecord == False:
                process_video.communicate(b'q')
                time.sleep(1)
                break

        for i in range(3):
            print(i)
            time.sleep(1)

        ewq = subprocess.call('ffmpeg -i ' + SAVE_PATH + self.name + ' -i ' + SAVE_PATH + 'aud' + self.audio + ' -c:v ' + 'copy ' + '-c:a ' + 'copy ' +
                              SAVE_PATH + 'final' + self.name, shell=True)
        # path = os.getcwd()
        # os.chdir("../opencast_uploader")
        #os.chdir("..\\opencast_uploader")

        # qwe = subprocess.call('python ..\\opencast_uploader\\video_uploader.py ' + str(self.args[0]) + ' ' +
        #                       str(self.args[1].split()[0].replace(':', '_')) + ' ' + str(self.args[2]) + ' ' + str(self.args[3]) +
        #                       ' ' + str(self.args[4]) + ' ' + str(self.args[5]) + ' ' + str(self.args[6]) + ' ' + path + '\\\\'  +'final' + self.name, shell=True)
        # # # qwe = subprocess.call('python3 video_uploader.py ' + str(self.args[0]) + ' ' +
        #                       str(self.args[1].split()[0].replace(':', '_')) + ' ' + str(self.args[2]) + ' ' + str(self.args[3]) +
        #                       ' ' + str(self.args[4]) + ' ' + str(self.args[5]) + ' ' + str(self.args[6]) + ' ' + path + '//' + 'final'+self.name, shell=True)
        # # print(self.args[0],self.args[1].split()[0].replace(':','_'),self.args[2],self.args[3],self.args[4], self.args[5], self.args[6], 'final'+self.name)

        logger.info('end of recording')



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

    def __init__(self, connect, parent=None):
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
        self.beginInsertRows(QModelIndex(), 0, len(cams) - 1)
        self._entries = cams
        self.endInsertRows()

    @Slot()
    def deleteCameras(self):
        if self.rowCount():
            self.beginRemoveColumns(QModelIndex(), 0, self.rowCount())
            del self._entries[self.rowCount() - 1]
            self.endRemoveRows()

class QueueConnect(QObject):

    queue_signal = Signal(str, list)
    def setQueue(self, queue):
        self.qwe = queue

    def run(self):
        while True:
            try:
                item = self.qwe.get()
                cmd = item[0]
                cams = ' '.join(item[1])
                self.queue_signal.emit(cmd, item[1])
            except:
                print('Смерть обработки сообщения API')

            QThread.msleep(2500)



class SettingsModel(QAbstractListModel):
    NameRole = Qt.UserRole + 1
    GenderRole = Qt.UserRole + 2
    AgeRole = Qt.UserRole + 3

    def __init__(self, data, parent=None):
        super().__init__(parent)
        self._data = data

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid() and role == Qt.DisplayRole:
            row = index.row()
            return f"{self._data[row]['name']} ({self._data[row]['gender']}, {self._data[row]['age']})"

        if role == SettingsModel.NameRole:
            return self._data[index.row()]['name']
        elif role == SettingsModel.GenderRole:
            return self._data[index.row()]['gender']
        elif role == SettingsModel.AgeRole:
            return self._data[index.row()]['age']

        return None

    def roleNames(self):
        return {
            SettingsModel.NameRole: b'name',
            SettingsModel.GenderRole: b'gender',
            SettingsModel.AgeRole: b'age',
        }



class AppCore(QObject):
    def __init__(self, connect, engine, q, parent=None):
        super(AppCore, self).__init__(parent)
        # self.thread = QThread()
        self.engine = engine
        freeSpace = self.getFreeSpace()
        self.engine.rootContext().setContextProperty("freeSpace", freeSpace)

        self.data = {}
        self.info = {}
        self.ipdict = {}
        self.current_room = ''
        self.connector = connect
        self.select_rtsp = []
        self.record_threads = []
        self.streaming = False
        self.isrecord = False
        self.vcap = 0
        self.current_audio = []
        self.list_files = []
        #
        self.fplayer = FFplayer()
        self.fplayer.start()

        self.queue = q

        self.thread = QThread()
        self.queue_an = QueueConnect()
        self.queue_an.setQueue(self.queue)
        self.queue_an.moveToThread(self.thread)
        self.queue_an.queue_signal.connect(self.api_message)
        self.thread.started.connect(self.queue_an.run)
        self.thread.start()

        # self.fortqwee = [
        #     {'name': 'Alice', 'gender': 'female', 'age': 25},
        #     {'name': 'Bob', 'gender': 'male', 'age': 30},
        #     {'name': 'Charlie', 'gender': 'male', 'age': 35},
        # ]
        # model_setting = SettingsModel(self.fortqwee)
        # self.engine.rootContext().setContextProperty('settingModel', model_setting)

        # cv2.namedWindow("main", cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('main', 900, 900)
        # cv2.setWindowProperty("main", 0, 1)
        # cv2.moveWindow('main', 800, 0)

        # self.singleStream = SingleStream()
        # self.singleStream.moveToThread(self.thread)
        # self.singleStream.newTextAndColor.connect(self.addNewTextAndColor)
        # self.thread.started.connect(self.singleStream.run)
        # self.thread.start()


    @Slot(str, list)
    def api_message(self, cmd, msg):
        if cmd == 'rec':
            print('Начало записи:')
            self.api_record_start(msg)

        elif cmd == 'stop':
            print('Конец записи')
            self.api_record_stop()
            print(msg)





    def api_record_stop(self):
        logger.info('Ending recordings From API')
        for threads in self.record_threads:
            threads.stopRecording()


    def api_record_start(self, cams):
        logger.info('Start record from API')
        string = 'naming'
        audio_rtsp = ""
        integer = 1
        timing = datetime.now()
        args_aud = [timing.year, timing.day, timing.month, timing.hour, timing.minute]
        audio_in = {}

        # for id, ad in self.ipdict.items():
        #     if not ad['room'] in audio_in:
        #         audio_in[ad['room']] = [ad['audio'][0]['rtsp_main']]

        for cms in cams:
            if not self.ipdict[cms]['room'] in audio_in:
                audio_in[self.ipdict[cms]['room']] = [self.ipdict[cms]['audio'][0]['rtsp_main']]

        for key, val in audio_in.items():
            audio_rtsp = val[0]
            audio_file = key
            naming_aud = self.videoNaming(audio_file)
            audio_in[key].append(naming_aud)
            audioRecorder = SavingCoder(audio_rtsp, naming_aud, args_aud)
            audioRecorder.start()
            self.record_threads.append(audioRecorder)

        for cms in cams:
            naming = self.videoNaming(self.ipdict[cms]['name'])
            self.list_files.append(naming)
            args = [self.ipdict[cms]['room'], self.ipdict[cms]['name'], timing.year, timing.day, timing.month, timing.hour, timing.minute]
            threadRecord = SavingStream(self.ipdict[cms]['video'], naming, audio_in[self.ipdict[cms]['room']][1], args)
            threadRecord.start()
            self.record_threads.append(threadRecord)
            integer = integer + 1


    def makeIPdict(self):
        '''
        Создание словаря с камерами и ip-адрессами
        :return:
        '''
        for key, value in self.info.items():
            aud = ''
            if value['audio']:
                aud = value['audio']
            for cam in value['cameras']:
                id = (cam['ip'].split('.'))[3]
                self.ipdict[str(id)] = {'room': key, 'audio': aud, 'video': cam['rtsp_main'], 'name': cam['name']}

        # pprint(self.ipdict)

    @Slot()
    def printTest(self):
        print('работает')


    @Slot()
    def getTrigger(self):
        qwerty = self.engine.rootObjects()[0]
        qwerty.onTestTrigger()

    @Slot(str)
    def getCams(self, str):
        list = []
        #self.select_rtsp.clear()

        self.current_room = str
        for camera in self.info[str]['cameras']:
            list.append({"name": camera['name'],
                         "type": camera['type'],
                         "rtsp": camera['rtsp_main']})
            #При переключениии аудиторий все камеры добаляются в запись сразу (ПОка закомментировано)
            #self.select_rtsp.append([camera['rtsp_main'],camera['name'], self.current_room])


        if len(self.info[str]['audio']) != 0:
            self.current_audio.clear()
            self.current_audio.append(self.info[str]['audio'][0])
            self.current_audio.append(str)


        # Изменить отправку на изменение
        self.connector.changeList(list)

    def getCameras(self) -> dict:
        with open(ROOMS_FILE, 'r') as file:
            info = json.loads(file.read())
            self.info = info
            self.makeIPdict()
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

    @Slot(str, str)
    def addSelect(self, rtsp, name) -> None:

        if [rtsp,name,self.current_room, self.current_audio[0]['rtsp_main']] in self.select_rtsp:
            self.select_rtsp.remove([rtsp, name, self.current_room, self.current_audio[0]['rtsp_main']])
            for cms in self.info[self.current_room]['cameras']:
                if cms['rtsp_main'] == rtsp:
                    cms['type'] = 0
        else:
            for cms in self.info[self.current_room]['cameras']:
                if cms['rtsp_main'] == rtsp:
                    cms['type'] = 1
            self.select_rtsp.append([rtsp, name, self.current_room, self.current_audio[0]['rtsp_main']])
        # print('-'*10)
        # pprint(self.select_rtsp)

    @Slot(str)
    def clearSelected(self, room) -> None:
        self.select_rtsp.clear()
        for camera in self.info[room]['cameras']:

            self.select_rtsp.append([camera['rtsp_main'], camera['name'], self.current_room])
        print(self.select_rtsp)

    # Тестовый на долгое нажатие
    @Slot(str)
    def goToView(self, rtsp) -> None:
        self.fplayer.play(rtsp)

    @Slot(str, str)
    def buttonReact(self, rtsp, name):
        self.addSelect(rtsp, name)
        print(self.select_rtsp)


    def getFreeSpace(self) -> str:
        free = psutil.disk_usage(DISK).free / (1024 * 1024 * 1024)
        return (f"{free:.4} Gb free on disk {DISK}")

    # @Slot(ndarray)
    # def addNewTextAndColor(self, string):
    #     cv2.imshow('main', string)

    @Slot()
    def recStop(self):
        logger.info('ending of recordings')
        for threads in self.record_threads:
            threads.stopRecording()




    def videoNaming(self, name) -> str:
        return ((('_'.join(name.split())).replace(':', '_') +
                 '_' +
                 ('_'.join(str(datetime.now()).split())).replace(':', '_')).replace('.', '_') + '.mkv')

    @Slot()
    def StartRecording(self):
        logger.info('trigger of slot StartRecording')
        string = 'naming'
        audio_rtsp = ""
        integer = 1
        timing = datetime.now()
        args_aud = [timing.year, timing.day, timing.month, timing.hour, timing.minute]
        audio_in = {}

        for cms in self.select_rtsp:
            if not cms[2] in audio_in:
                audio_in[cms[2]] = [cms[3]]

        for key, val in audio_in.items():
            audio_rtsp = val[0]
            audio_file = key
            naming_aud = self.videoNaming(audio_file)
            audio_in[key].append(naming_aud)
            audioRecorder = SavingCoder(audio_rtsp, naming_aud, args_aud)
            audioRecorder.start()
            self.record_threads.append(audioRecorder)

        for rtsp in self.select_rtsp:
            naming = self.videoNaming(rtsp[1])
            self.list_files.append(naming)
            args = [rtsp[2], rtsp[1], timing.year, timing.day, timing.month, timing.hour, timing.minute]
            threadRecord = SavingStream(rtsp[0], naming, audio_in[rtsp[2]][1], args)
            threadRecord.start()
            self.record_threads.append(threadRecord)
            integer = integer + 1