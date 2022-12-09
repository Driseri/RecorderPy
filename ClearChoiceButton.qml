import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

Rectangle {
    id: clearChoi
    width: grid.cellWidth; height: grid.cellHeight * 0.8
    radius: 5
    color: clearChoiClick.containsPress ? "#bea18d" : "#01004e"
    border.width: 2
    border.color: "#01004e"
    anchors.right: startRec.left
    anchors.bottom: parent.bottom
    anchors.margins: 10
    Image {
        id: img3
        anchors.centerIn: parent
        width: parent.height / 1.2
        height: parent.height / 1.2
        source: "./img/unselect.png"
    }
    MouseArea {
        id: clearChoiClick
        anchors.fill: parent
        onClicked: {
            appCore.clearSelected()
        }
    }
}
