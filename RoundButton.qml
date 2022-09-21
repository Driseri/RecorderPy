import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

Item {
    id: root
    property int size: 100
    property color color: "lightgrey"
    property alias text: caption.text

    signal cliked()

    width: size
    height: size


    Rectangle {
        anchors.fill: parent
        radius: size/2
        color: mouseArea.containsPress ? Qt.darker(root.color,1.2) : root.color

        Text {
            id: caption
            anchors.centerIn:  parent
            text: qsTr("Click me")
        }

        MouseArea {
            id: mouseArea
            anchors.fill: parent
            onClicked: {
                root.cliked();
            }
        }
    }
}
