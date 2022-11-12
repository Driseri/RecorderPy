import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

Component {
    id: screendelegate
    Rectangle {
        width: grid.cellWidth * 0.95; height: grid.cellHeight * 0.95
        radius: 5
//        color: "#27328e"
        color: "#01004e"
        border.width: 2
        border.color: "black"
        Text { id: gridText; text: model.name; anchors.centerIn: parent; color: "white";
            font.pointSize: grid.cellWidth / 15; font.bold: true}
        MouseArea {
                anchors.fill: parent
                onClicked: {
                    appCore.buttonReact(model.rtsp, model.name)
                    parent.color = "lightsteelblue"
                }
            }
    }
}
