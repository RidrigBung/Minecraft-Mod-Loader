from PySide2 import QtWidgets, QtCore
import os

# minecraft mods folder: os.path.join(os.getenv('APPDATA'), '.minecraft\\mods')
minecraft_mods_folder = os.path.join(os.getenv('APPDATA'), '.minecraft\\mods')
# modpacks folder: '.\\modpacks'
modpacks_folder = '.\\modpacks'

class ModpackWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.status_label = QtWidgets.QLabel("Status: Unknown")

        # create a widget with a vertical layout and add the list of labels
        # the style sheet of self.subsWidget will cascade down to the individual labels.
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setStyleSheet('QLabel{color: black; font-size:20px}')
        self.modpacks_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        modpacks_list = os.listdir(modpacks_folder)
        self.buttonGroup = QtWidgets.QButtonGroup(self)
        self.buttonGroup.buttonClicked[QtWidgets.QAbstractButton].connect(self.change_modpack)
        for modpack_name in modpacks_list:
            self.btn = QtWidgets.QPushButton(modpack_name)
            self.buttonGroup.addButton(self.btn)
            self.modpacks_layout.addWidget(self.btn)

        # create a scroll area and add widget with labels to this area
        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidget(self.centralwidget)

        # set layout of main widget and add scroll area to this layout
        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.addWidget(self.status_label)
        mainLayout.addWidget(self.scroll_area)

    def disable_all_buttons(self):
        for btn in self.buttonGroup.buttons():
            if btn.text()[-11:] == ' [selected]':
                btn.setText(btn.text()[:-11])

    def change_btn_text(self, btn):
        self.disable_all_buttons()
        if btn.text()[-11:] == ' [selected]':
            btn.setText(btn.text()[:-11])
        else:
            btn.setText(f'{btn.text()} [selected]')
    
    def change_modpack(self, btn):
        self.change_btn_text(btn)
        self.status_label.setText("Status: Processing")
        for mod in os.listdir(minecraft_mods_folder):
            os.remove(os.path.join(minecraft_mods_folder, mod))
        modpack_name = btn.text()[:-11]
        modpack_folder = os.path.join(modpacks_folder, modpack_name)
        for mod in os.listdir(modpack_folder):
            os.popen(f'copy {os.path.join(modpack_folder, mod)} {os.path.join(minecraft_mods_folder, mod)}')
        self.status_label.setText(f"Status: installed {modpack_name}")


if __name__=="__main__":
    app = QtWidgets.QApplication([])
    window = ModpackWindow()
    window.resize(500,500)
    window.show()
    app.exec_()