import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

Component {
    id: screendelegate
    Rectangle {
        readonly property GridView __gridview: GridView.view
        id: rec
        width: grid.cellWidth * 0.95
        height: grid.cellHeight * 0.95
        radius: 20
        color: __gridview.currentIndex == index ? "#bea18d" : "#01004e"
        border.width: 2
        border.color: "#01004e"
        Text {
            id: gridText;
            text: model.name;
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            color: "white";
            width: parent.width
            height: parent.height
            font.pointSize: grid.cellWidth / 13
            font.bold: true
            wrapMode: Text.Wrap
        }
        MouseArea {
                anchors.fill: parent
                onPressAndHold: {
                    appCore.goToView(model.rtsp)
                    __gridview.currentIndex = index
                }
                onClicked: {
                    appCore.buttonReact(model.rtsp, model.name)
                    __gridview.currentIndex = index
                }
            }
    }
}
