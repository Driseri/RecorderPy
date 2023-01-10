import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

Component {
    id: buttondelegate
    Rectangle {
        readonly property ListView view: ListView.view
        property int i: 0
        id:rect
        radius: 10
        height: 60
        width: ListView.view.width
        color: view.currentIndex == index ? "#bea18d" : "#ffecde"
        Text {
            id: buttonText
            width: parent.width
            height: parent.height
            text: display
            font.pointSize: grid.cellWidth / 13
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            color: view.currentIndex == index ? "white" : "#01004e"
            wrapMode: Text.Wrap
        }
        MouseArea {
            id: buttmouse
                anchors.fill: parent
                onClicked: {
                    videoModel.deleteCameras()
                    appCore.getCams(buttonText.text)
                    videoModel.addCamera()
                    view.currentIndex = index
//                    for(i = 0; i < grid.count + 1; i++)
//                        grid.children[0].children[i].color = "#bea18d"
                    page.currRoom = buttonText.text
                }
            }
    }
}
