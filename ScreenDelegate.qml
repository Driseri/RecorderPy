import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

Component {
    id: screendelegate
    Rectangle {
        readonly property GridView view: GridView.view
        property int i: 0
        id: rec
        width: grid.cellWidth * 0.95
        height: grid.cellHeight * 0.95
        radius: 20
        color: "#d3d3d3"
        Component.onCompleted : {
//            if (rec.color == "#d3d3d3" & flag) {
//                    rec.color = "#01004e";
//                    flag = 0;
//                }
//            if (rec.color == "#01004e" & flag) {
//                rec.color = "#d3d3d3";
//                flag = 0;
//            }
              if (model.type == 1) {
                    rec.color = "#01004e";
              }
        }
        Text {
            id: gridText;
            text: model.name;
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            color: "white";
            width: parent.width
            height: parent.height
            font.bold: true
            wrapMode: Text.Wrap
            fontSizeMode: Text.Fit
            minimumPixelSize: 10
            font.pixelSize: grid.cellWidth / 10
        }

        Rectangle{
             id: circle
             width: grid.cellWidth / 20
             anchors.right: parent.right
             anchors.top: parent.top
             anchors.margins: 10
             radius: width / 2
             height: width
             visible: rec.color == "#01004e" ? true: false
             color: startRec.color == "#01004e" ? "red" : "grey"
        }
        MouseArea {
                anchors.fill: parent
                onPressAndHold: {
                    appCore.goToView(model.rtsp)

//                    var flag = 1;
//                    if (rec.color == "#d3d3d3" & flag) {
//                        rec.color = "#01004e";
//                        flag = 0;
//                    }
//                    if (rec.color == "#01004e" & flag) {
//                        rec.color = "#d3d3d3";
//                        flag = 0;
//                    }
                }
                onClicked: {
                    appCore.buttonReact(model.rtsp, model.name)

                    var flag = 1;
                    if (rec.color == "#d3d3d3" & flag) {
                        rec.color = "#01004e";
                        flag = 0;
                    }
                    if (rec.color == "#01004e" & flag) {
                        rec.color = "#d3d3d3";
                        flag = 0;
                    }
                }
            }
    }
}
