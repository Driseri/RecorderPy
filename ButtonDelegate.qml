import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

Component {
    id: buttondelegate
    Rectangle {
        radius: 10
        height: 60
        width: ListView.view.width
        color: "whitesmoke"
        border.color: " black"
        Text {
            id: buttonText
            anchors.centerIn: parent
            text: display /*model.name*/
            font.pointSize: grid.cellWidth / 17
            font.bold: true
        }
        MouseArea {
                anchors.fill: parent
                onClicked: {
                    videoModel.deleteCameras()
                    appCore.getCams(buttonText.text)
                    videoModel.addCamera()
                    parent.color = "#bea18d"
                    buttonText.color = "white"
                }
            }
    }
}
