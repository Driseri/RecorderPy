# This Python file uses the following encoding: utf-8
import sys
from AppCore import AppCore
from AppCore import VideoModel
from AppCore import Connector

from pathlib import Path

from PySide2.QtCore import Qt, QUrl, QStringListModel
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine



if __name__ == "__main__":
    #Подгрузка ядра приложения
    connector = Connector()
    appCore = AppCore(connector)
    videoModel = VideoModel(connector)


    #Подгрузка данных камер с API
    data = appCore.getCameras()
#    models = CamerModel(data)

    #Запуск приложения
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    qml_file = Path(__file__).resolve().parent / "main.qml"

    #Подсчет свободного места на диске
    freeSpace = appCore.getFreeSpace()
    engine.rootContext().setContextProperty("freeSpace",freeSpace)

    #Подключение ядра к QML
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
