import sys
import time
from pathlib import Path

from PySide2.QtCore import QStringListModel
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2 import QtCore

from AppCore import AppCore
from AppCore import Connector
from AppCore import VideoModel
from AppCore import SettingsModel

class Recorder():
    def __init__(self):
        app = QGuiApplication(sys.argv)
        engine = QQmlApplicationEngine()
        # Подгрузка ядра приложения
        connector = Connector()
        appCore = AppCore(connector, engine)
        videoModel = VideoModel(connector)
        # Подгрузка данных камер с API
        data = appCore.getCameras()
        #    models = CamerModel(data)

        # Запуск приложения

        qml_file = Path(__file__).resolve().parent / "main.qml"

        # Подсчет свободного места на диске
        # freeSpace = appCore.getFreeSpace()
        # engine.rootContext().setContextProperty("freeSpace", freeSpace)

        # Подключение ядра к QML
        engine.rootContext().setContextProperty("appCore", appCore)

        #
        rooms = list(data.keys())
        rooms_model = QStringListModel()
        rooms_model.setStringList(rooms)
        engine.rootContext().setContextProperty("listModel", rooms_model)

        engine.rootContext().setContextProperty("videoModel", videoModel)

        engine.load(str(qml_file))
        if not engine.rootObjects():
            sys.exit(-1)
        sys.exit(app.exec_())



def start(q):
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    # Подгрузка ядра приложения
    connector = Connector()
    appCore = AppCore(connector, engine, q)

    videoModel = VideoModel(connector)
    # Подгрузка данных камер с API
    data = appCore.getCameras()

    data_rtsp = [
            {'name': 'Alice', 'gender': 'female', 'age': 25},
            {'name': 'Bob', 'gender': 'male', 'age': 30},
            {'name': 'Charlie', 'gender': 'male', 'age': 35},
        ]
    model_setting = SettingsModel(data_rtsp)
    engine.rootContext().setContextProperty('settingModel', model_setting)

    # Запуск приложения

    qml_file = Path(__file__).resolve().parent / "main.qml"

    # Подсчет свободного места на диске
    # freeSpace = appCore.getFreeSpace()
    # engine.rootContext().setContextProperty("freeSpace", freeSpace)

    # Подключение ядра к QML
    engine.rootContext().setContextProperty("appCore", appCore)

    #
    rooms = list(data.keys())
    rooms_model = QStringListModel()
    rooms_model.setStringList(rooms)
    engine.rootContext().setContextProperty("listModel", rooms_model)

    engine.rootContext().setContextProperty("videoModel", videoModel)

    engine.load(str(qml_file))



    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
# start()