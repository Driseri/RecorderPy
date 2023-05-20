import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

Rectangle {
    id: clearChoi
    width: grid.cellWidth; height: grid.cellHeight * 0.4
    radius: 5
    color: clearChoiClick.containsPress ? "#01004e" : "lightgrey"
    anchors.right: startRec.left
    anchors.bottom: parent.bottom
    anchors.left: parent.left
    anchors.margins: 10
    Image {
        id: img3
        anchors.centerIn: parent
        width: parent.height / 1.2
        height: parent.height / 1.2
        source: "./img/del.png"
    }
    MouseArea {
        id: clearChoiClick
        anchors.fill: parent
        onClicked: {
            appCore.clearSelected()
        }
    }
}
