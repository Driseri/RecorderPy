import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

Rectangle {
    id: choi
    width: grid.cellWidth; height: grid.cellHeight * 0.8
    radius: 5
    color: choiClick.containsPress ? "#bea18d" : "#01004e"
    border.width: 2
    border.color: "#01004e"
    anchors.right: parent.right
    anchors.bottom: parent.bottom
    anchors.margins: 10
    Image {
        id: img1
        anchors.centerIn: parent
        width: parent.height / 1.2
        height: parent.height / 1.2
        source: "./img/stop.png"
    }
    MouseArea {
        id: choiClick
        anchors.fill: parent
        onClicked: {
            appCore.recStop()
            startRec.color = "#01004e"
        }
    }
}
