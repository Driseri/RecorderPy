import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

Window {
    id: win
    width: 700
    height: 700
    visible: true
    color: "lightgrey"
    title: qsTr("REcorderGUI1.0")
//    Component.onCompleted: {
//        var component = Qt.createComponent("stream.qml")
//        var window    = component.createObject(win)
//        window.show()
//    }
    //flags: Qt.Window | Qt.FramelessWindowHint //Включить в финале
    //visibility: Window.FullScreen  // НЕ ЗАБЫТЬ ВКЛЮЧИТЬ ПОТОМ!!!!!


    Page {
        id: page
        anchors.fill: parent
        footer: Rectangle {
            id: footer
            width: win.width
            height: win.height * 0.05
            color: "#01004e"
            border.color: "#01004e"
            border.width: 2
            Text {
                anchors.centerIn: parent
                text: freeSpace
                color: "#ffecde"
                font.bold: true
            }
        }


        Rectangle {
            id: scrol
            width: parent.width * 0.2
            height: parent.height
            color: "#01004e"
            ListView {
                id: listview
                anchors.fill: parent
                anchors.margins: 15
                spacing: 15
                model: listModel
                delegate: ButtonDelegate{}
            }
        }

        Rectangle {
            id: screen
            height: parent.height
            width: parent.width - scrol.width
            anchors.right: parent.right
            color: "#ffecde"

            GridView {
                id: grid
                cellWidth: parent.width / 4 - 8
                cellHeight: parent.height / 4 - 8
                anchors.fill: parent
                anchors.margins: 15
                model: videoModel
                delegate: ScreenDelegate {}
            }

            StopRecordingButton {id: choi}
            StartRecordingButton {id: startRec}
            ClearChoiceButton {id: clearChoi}
            SelectCamerasButton {id: select}
        }
    }
}
