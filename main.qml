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
            color: "#bea18d"
            border.color: "black"
            border.width: 2
            Text {
                anchors.centerIn: parent
                text: freeSpace
                color: "#01004e"
                font.bold: true
            }
        }


        Rectangle {
            id: scrol
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.bottom: parent.bottom
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
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            color: "grey"

            Component {
                    id: contactDelegate
                    Rectangle {
                        width: grid.cellWidth*0.95; height: grid.cellHeight*0.9
                        radius: 5
                        color: "grey"
                        border.width: 2
                        border.color: "black"

                        Column {
                            anchors.fill: parent
                            Text { text: model.name; anchors.horizontalCenter: parent.horizontalCenter }
                        }
                        MouseArea {
                                anchors.fill: parent
                                onClicked: {
                                    //appCore.addSelect(model.rtsp, model.name)
                                    appCore.buttonReact(model.rtsp, model.name)
                                    //appCore.recStart()
                                    //parent.color = "yellow"
                                }
                            }
                    }
                }

            GridView {
                id: grid
                cellWidth: parent.width / 3 - 10
                cellHeight: parent.height / 3 - 10
                width: parent.width
                height: parent.height
                anchors.fill: parent
                anchors.right:screen.right
                anchors.left:screen.left
                anchors.margins: 15
                model: videoModel
                delegate: ScreenDelegate {}
                highlight: Rectangle { color: "lightsteelblue"; radius: 5; Text{} }
            }

            Rectangle {
                        id: choi
                        width: grid.cellWidth * 0.75; height: grid.cellHeight * 0.3
                        radius: 5
                        color: "whitesmoke"
                        border.width: 2
                        border.color: "black"
                        anchors.right: parent.right
                        anchors.bottom: parent.bottom
                        anchors.margins: 10
                        Text { id: choitext; text: "exit"; anchors.centerIn: parent;
                            font.pointSize: grid.cellWidth / 20; font.bold: true}
                        MouseArea {
                                anchors.fill: parent
                                onClicked: {
                                    appCore.recStop()
                                    parent.color = "#01004e"
                                    selecttext.color = "white"
                                }
                            }
                    }
            Rectangle {
                        id: startRec
                        width: grid.cellWidth * 0.75; height: grid.cellHeight * 0.3
                        radius: 5
                        color: "white"
                        border.width: 2
                        border.color: "black"
                        anchors.right: choi.left
                        anchors.bottom: parent.bottom
                        anchors.margins: 10
                        Text { id: startRectext; text: "start recording"; anchors.centerIn: parent;
                            font.pointSize: grid.cellWidth / 20; font.bold: true}
                        MouseArea {
                                anchors.fill: parent
                                onClicked: {
                                    appCore.StartRecording()
                                    parent.color = "#01004e"
                                    selecttext.color = "white"
                                }
                            }
                    }
            Rectangle {
                        id: clearChoi
                        width: grid.cellWidth * 0.75; height: grid.cellHeight * 0.3
                        radius: 5
                        color: "white"
                        border.width: 2
                        border.color: "black"
                        anchors.right: startRec.left
                        anchors.bottom: parent.bottom
                        anchors.margins: 10
                        Text { id: clearChoitext; text: "clear camera selection"; anchors.centerIn: parent;
                            font.pointSize: grid.cellWidth / 20; font.bold: true}
                        MouseArea {
                                anchors.fill: parent
                                onClicked: {
                                    appCore.clearSelected()
                                    parent.color = "#01004e"
                                    selecttext.color = "white"
                                }
                            }
                    }

            Rectangle {
                        id: select
                        width: grid.cellWidth * 0.75; height: grid.cellHeight * 0.3
                        radius: 5
                        color: "white"
                        border.width: 2
                        border.color: "black"
                        anchors.right: clearChoi.left
                        anchors.bottom: parent.bottom
                        anchors.left: screen.left;
                        anchors.margins: 10
                        Text {id: selecttext; text: "camera selection"; anchors.centerIn: parent;
                            font.pointSize: grid.cellWidth / 20; font.bold: true}
                        MouseArea {
                                anchors.fill: parent
                                onClicked: {
                                    appCore.setRecord()
                                    parent.color = "#01004e"
                                    selecttext.color = "white"
                                }
                            }
                    }
        }
}

}
