import cutter

from PySide2.QtCore import QObject, SIGNAL
from PySide2.QtWidgets import QAction, QLabel, QFileDialog


class DiaphoraWidget(cutter.CutterDockWidget):
    def __init__(self, parent, action):
        super().__init__(parent, action)
        self.setObjectName("DiaphoraWidget")
        self.setWindowTitle("Diaphora")

        self._label = QLabel(self)
        self.setWidget(self._label)

        self._file_dialog = QFileDialog(self)
        self.setWidget(self._file_dialog)


class DiaphoraPlugin(cutter.CutterPlugin):
    name = "Diaphora"
    description = "This plugin differs binaries"
    version = "1.0"
    author = "Jon"

    def setupPlugin(self):
        pass

    def setupInterface(self, main):
        action = QAction("My Plugin", main)
        action.setCheckable(True)
        widget = DiaphoraWidget(main, action)
        main.addPluginDockWidget(widget, action)

    def terminate(self):
        pass


# Cutter will call this function first
def create_cutter_plugin():
    return DiaphoraPlugin()
