import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

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
    Image {
        id: img
        //                            anchors.fill: parent
        anchors.centerIn: parent
        width: parent.height / 1.2
        height: parent.height / 1.2
        source: "./img/addnew.png"
    }
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
