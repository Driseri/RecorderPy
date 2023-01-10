import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

Rectangle {
    property int i: 0
    id: select
    width: grid.cellWidth; height: grid.cellHeight * 0.4
    radius: 5
    color: i % 2 == 0 ? "#01004e": "#bea18d"
    border.width: 2
    border.color: "#01004e"
    anchors.right: clearChoi.left
    anchors.bottom: parent.bottom
    anchors.left: parent.left
    anchors.margins: 10
    Image {
        id: img
        anchors.centerIn: parent
        width: parent.height / 1.2
        height: parent.height / 1.2
        source: "./img/addnew.png"
    }
    MouseArea {
        anchors.fill: parent
        onClicked: {
            appCore.setRecord()
            // #todo сделать выделение выбранных для записи
            console.log("____________________")
            if (i % 2 == 0) {
                for(var j = 1; j < grid.count + 1; j++){
                    grid.children[0].children[j].color = "#bea18d";
                    console.log(grid.children[0].children[j].children[0].text);
                }
//                if (page.currRoom != page.selectRoom){
//                    console.log('poapsdoapsdopasd');
//                }
                page.isSelection = 1
            }
            if (i % 2 == 1) {
                for(var j = 1; j < grid.count + 1; j++){
                    grid.children[0].children[j].color = "#01004e";
                }
                for(var j = 1; j < grid.count + 1; j++){
                    if (grid.children[0].children[j].children[0].text == page.currCam){
                        grid.children[0].children[j].color = "#bea18d";
                    }

                }
                page.isSelection = 0
            }
            i += 1
            console.log(page.isSelection)
        }
    }
}
