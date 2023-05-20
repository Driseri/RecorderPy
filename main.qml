import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

Window {
    id: win
    width: 700
    height: 700
    visible: true
    color: "lightgrey"
    title: qsTr("REcorderGUI1.0")

    signal testTrigger()

    Loader {
        id: loader
        source: "settingsWin.qml"
        active: false
    }


    function onTestTrigger() {
        console.log('qweqwe!');
    }
//    Component.onCompleted: {
//        var component = Qt.createComponent("stream.qml")
//        var window    = component.createObject(win)
//        window.show()
//    }
    //flags: Qt.Window | Qt.FramelessWindowHint //Включить в финале
    //visibility: Window.FullScreen  // НЕ ЗАБЫТЬ ВКЛЮЧИТЬ ПОТОМ!!!!!


    Page {
        id: page
        property int isRecording: 0
        anchors.fill: parent
        footer: Rectangle {
            id: footer
            width: win.width
            height: win.height * 0.05
            color: "#01004e"
            border.color: "#01004e"
            border.width: 2
            Text {
                anchors.centerIn: parent
                text: freeSpace
                color: "white"
                font.bold: true
            }
        }


        Rectangle {
            id: scrol
            width: parent.width * 0.2
            height: parent.height
            color: "white"
            ListView {
                id: listview
                anchors.fill: parent
                anchors.margins: 15
                spacing: 25
                model: listModel
                delegate: ButtonDelegate{}
            }
        }

        Rectangle {
            id: screen
            height: parent.height * 0.6
            width: parent.width - scrol.width
            anchors.right: parent.right
            color: "white"

            GridView {
                id: grid
                cellWidth: parent.width / 3 - 12
                cellHeight: parent.height / 2 - 12
                anchors.fill: parent
                anchors.margins: 15
                model: videoModel
                delegate: ScreenDelegate {}
            }
        }

        Rectangle{
            id: settings
            width: parent.width * 0.05
            height: parent.height * 0.6
            anchors.right: parent.right
            anchors.top: parent.top
            color: "white"
            ComboBox {
                id: comBox
                width: parent.width
                height: parent.height * 0.1
                model:
                    ListModel {
                    ListElement { text: "⚙" }
                    ListElement { text: "Setting 1" }
                    ListElement { text: "Setting 2" }
                    ListElement { text: "Setting 3" }
                }
                onActivated: {
                    var index = comBox.currentIndex

                    // выполняем соответствующие действия на основе индекса
                    switch (index) {
                        case 0:
                            // выполнить действие для первого элемента
                            loader.active = true;
                            loader.item.show();
                            console.log(settingModel);
                            console.log(videoModel);
                            break;
                        case 1:
                            // выполнить действие для второго элемента
                            console.log("Выбрана опция 2")
                            break;
                        case 2:
                            // выполнить действие для третьего элемента
                            console.log("Выбрана опция 3")
                            break;
                    }
                }
            }
        }

        Rectangle{
            id: buttons
            height: parent.height * 0.4
            width: parent.width - scrol.width
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            color: "white"
            StopRecordingButton {id: stopRec}
            StartRecordingButton {id: startRec}
            ClearChoiceButton {id: clearChoi}
        }
        NotRecordPopup {
            id: recordpopup
        }
        AFewMemoryPopup {
            id: memorypopup
        }
        BreakCoderPopup {
            id: breakcoderpopup
        }
        BreakCamsPopup {
            id: breakcamspopup
        }
    }
}
