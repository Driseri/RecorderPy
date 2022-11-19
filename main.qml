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

            Rectangle {
                        id: choi
                        width: grid.cellWidth; height: grid.cellHeight * 0.3
                        radius: 5
                        color: "#01004e"
                        border.width: 2
                        border.color: "#01004e"
                        anchors.right: parent.right
                        anchors.bottom: parent.bottom
                        anchors.margins: 10
                        Text { id: choitext; text: "exit"; anchors.centerIn: parent;
                            font.pointSize: grid.cellWidth / 15; font.bold: true; color: "white"}
                        MouseArea {
                                anchors.fill: parent
                                onClicked: {
                                    appCore.recStop()
                                    parent.color = "#bea18d"
                                    choitext.color = "white"
                                    clearChoi.color = startRec.color = select.color = "#01004e"
                                }
                            }
                    }
            Rectangle {
                        id: startRec
                        width: grid.cellWidth; height: grid.cellHeight * 0.3
                        radius: 5
                        color: "#01004e"
                        border.width: 2
                        border.color: "#01004e"
                        anchors.right: choi.left
                        anchors.bottom: parent.bottom
                        anchors.margins: 10
                        Text { id: startRectext; text: "start recording"; anchors.centerIn: parent;
                            font.pointSize: grid.cellWidth / 15; font.bold: true; color: "white"}
                        MouseArea {
                                anchors.fill: parent
                                onClicked: {
                                    appCore.StartRecording()
                                    parent.color = "#bea18d"
                                    startRectext.color = "white"
                                    clearChoi.color = choi.color = select.color = "#01004e"
                                }
                            }
                    }
            Rectangle {
                        id: clearChoi
                        width: grid.cellWidth; height: grid.cellHeight * 0.3
                        radius: 5
                        color: "#01004e"
                        border.width: 2
                        border.color: "#01004e"
                        anchors.right: startRec.left
                        anchors.bottom: parent.bottom
                        anchors.margins: 10
                        Text { id: clearChoitext; text: "clear camera selection"; anchors.centerIn: parent;
                            font.pointSize: grid.cellWidth / 15; font.bold: true; color: "white"}
                        MouseArea {
                                anchors.fill: parent
                                onClicked: {
                                    appCore.clearSelected()
                                    parent.color = "#bea18d"
                                    clearChoitext.color = "white"
                                    choi.color = startRec.color = select.color = "#01004e"
                                }
                            }
                    }

            Rectangle {
                        id: select
                        width: grid.cellWidth; height: grid.cellHeight * 0.3
                        radius: 5
                        color: "#01004e"
                        border.width: 2
                        border.color: "#01004e"
                        anchors.right: clearChoi.left
                        anchors.bottom: parent.bottom
                        anchors.left: screen.left;
                        anchors.margins: 10
                        Text {id: selecttext; text: "camera selection"; anchors.centerIn: parent;
                            font.pointSize: grid.cellWidth / 15; font.bold: true; color: "white"}
                        MouseArea {
                                anchors.fill: parent
                                onClicked: {
                                    appCore.setRecord()
                                    parent.color = "#bea18d"
                                    selecttext.color = "white"
                                    clearChoi.color = startRec.color = choi.color = "#01004e"
                                }
                            }
                    }
        }
}

}
