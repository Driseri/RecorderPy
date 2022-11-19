import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

Component {
    id: buttondelegate
    Rectangle {
        readonly property ListView __listview: ListView.view
        id:rect
        radius: 10
        height: 60
        width: ListView.view.width
        color: __listview.currentIndex == index ? "#bea18d" : "#ffecde"
        Text {
            id: buttonText
            width: parent.width
            height: parent.height
            text: display
            font.pointSize: grid.cellWidth / 13
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            color: __listview.currentIndex == index ? "white" : "#01004e"
            wrapMode: Text.Wrap
        }
        MouseArea {
            id: buttmouse
                anchors.fill: parent
                onClicked: {
                    videoModel.deleteCameras()
                    appCore.getCams(buttonText.text)
                    videoModel.addCamera()
                    __listview.currentIndex = index
                }
            }
    }
}
