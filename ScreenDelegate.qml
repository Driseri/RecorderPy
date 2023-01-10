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
        color: "#01004e"
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

                    for(var j = 1; j < grid.count + 1; j++)
                        grid.children[0].children[j].color = "#01004e"

                    view.currentIndex = index
                    view.currentItem.color = "#bea18d"
                    page.currCam = gridText.text
                    page.selectRoom = page.currRoom

                }
                onClicked: {
                    if (page.isSelection == 1){
                        var falg = 1;
                        if (rec.color == "#bea18d" & falg) {
                            rec.color = "#01004e";
                            falg = 0;
                        }
                        if (rec.color == "#01004e" & falg) {
                            rec.color = "#bea18d";
                            falg = 0;
                        }

                    }
//                    switch  (rec.color)
//                    {
//                    case "#bea18d":
//                        rec.color = "#01004e";
//                        console.log('todis');
//                        break;
//                    case "#01004e":
//                        rec.color = "#bea18d";
//                        console.log('tosel');
//                        break;
//                    }
                    appCore.buttonReact(model.rtsp, model.name)

//                    for(i = 0; i < grid.count + 1; i++)
//                        grid.children[0].children[i].color = "#01004e"
                    //view.currentIndex = index
                    //view.currentItem.color = "#bea18d"
                }
            }
    }
}
