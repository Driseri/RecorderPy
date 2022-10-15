import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Window {
    id: win
    width: 700
    height: 700
    visible: true
    color: "lightgrey"
    title: qsTr("REcorderGUI1.0")

    //visibility: Window.FullScreen  // НЕ ЗАБЫТЬ ВКЛЮЧИТЬ ПОТОМ!!!!!




    Page {
        id: page
        anchors.fill: parent
        footer: Rectangle {
            width: win.width
            height: win.height * 0.05
            color:  "green"
            Text {
                anchors.centerIn: parent
                text: freeSpace
            }
        }

        Rectangle {
            id: scrol
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            width: parent.width * 0.2
            height: parent.height
            color: "blue"

            ListView {
                id: listview
                anchors.fill: parent
                model: listModel
                spacing: 10
                delegate:
                    Rectangle {
                    radius: 5
                    height: 60
                    width: ListView.view.width
                    color: "grey"
                    border.color: " black"
                    Text {
                        id: buttonText
                        anchors.centerIn: parent
                        text: display
                    }
                    MouseArea {
                            anchors.fill: parent
                            onClicked: {

                                //qwe = appCore.getCams(buttonText.text)
                                videoModel.deleteCameras()
                                appCore.getCams(buttonText.text)
                                videoModel.addCamera()
                                //videoModel.getConnector()
                            }
                        }

                }
            }
        }



        Rectangle {
            height: parent.height
            width: parent.width - scrol.width
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            color: "red"

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
                                    console.log(model.rtsp)
                                }
                            }
                    }
                }

            GridView {
                id: grid
                cellWidth: parent.width/4
                cellHeight: parent.height/4
                width: parent.width
                height: parent.height
                anchors.fill: parent
                model: videoModel
                delegate: contactDelegate
                highlight: Rectangle { color: "lightsteelblue"; radius: 5; Text{} }

            }

        }
}

}
