import QtQuick 6.0
import QtQuick.Controls 6.0
import QtQuick.Layouts 6.0

ApplicationWindow {
    visible: true
    width: 400
    height: 250
    title: "Display Off"

    ColumnLayout {
        anchors.centerIn: parent
        spacing: 20

        Label {
            text: "Delay: " + delaySlider.value + " seconds"
            font.pixelSize: 16
            Layout.alignment: Qt.AlignCenter
        }

        Slider {
            id: delaySlider
            from: 0
            to: 60
            value: 5
            Layout.fillWidth: true
        }

        ComboBox {
            id: sessionTypeCombo
            model: ["Wayland", "X11"]
            Layout.fillWidth: true
        }

        CheckBox {
            id: blockSleepCheckbox
            text: "Block Sleep and Screen Locking"
            Layout.fillWidth: true
        }

        Button {
            text: "Turn Off Display"
            Layout.alignment: Qt.AlignCenter
            onClicked: {
                displayOffApp.turn_off_display(delaySlider.value, sessionTypeCombo.currentText, blockSleepCheckbox.checked)
            }
        }
    }
}
