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
        property string currRoom: "cocky"
        property string currCam: "pocky"
        property string selectRoom: "suki"
        property int isSelection: 0
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
            height: parent.height * 0.6
            width: parent.width - scrol.width
            anchors.right: parent.right
            color: "#ffecde"

            GridView {
                id: grid
                cellWidth: parent.width / 4 - 7.5
                cellHeight: parent.height / 2 - 7.5
                anchors.fill: parent
                anchors.margins: 15
                model: videoModel
                delegate: ScreenDelegate {}
            }
        }

//            СПИСОК КАМЕР БЕЗ БЭКА
//            ЕСЛИ РАСКОММЕНТИРОВАТЬ, ТО НУЖНО ПОМЕНЯТЬ У НИЖНЕГО RECTANGLE ВЫСОТУ НА (*0.15)

//            Rectangle
//            {
//                id: list
//                height: parent.height - buttons.height - screen.height
//                width: parent.width - scrol.width
//                color: "#ffecde"
//                anchors.top: screen.bottom
//                anchors.bottom: buttons.top
//                anchors.right: parent.right
//                border.color: "#01004e"
//                border.width: 3
//                radius: 10
//                Text
//                {
//                    id: chosencameras
//                    text: "Chosen cameras"
//                    color: "#01004e"
//                    anchors.horizontalCenter: parent.horizontalCenter
//                    font.bold: true
//                    font.pointSize: parent.width / 50
//                }
//                ListView
//                {
//                    id: listview1
//                    anchors.fill: parent
//                    anchors.margins: 25
//                    spacing: 30
//                    model: select_rtsp
//                    delegate: ListDelegate {}
//                }
//            }

            Rectangle{
                id: buttons
                height: parent.height * 0.4
                width: parent.width - scrol.width
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                color: "#ffecde"
                StopRecordingButton {id: choi}
                StartRecordingButton {id: startRec}
                ClearChoiceButton {id: clearChoi}
                SelectCamerasButton {id: select}
            }
    }
}
