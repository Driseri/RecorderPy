import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

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
    Image {
        id: img2
        anchors.centerIn: parent
        width: parent.height / 1.2
        height: parent.height / 1.2
        source: "img/record.png"
    }
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
