import cutter
import json
import os
import subprocess

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QVBoxLayout, QLabel, QWidget, QSizePolicy, QPushButton, QTextBrowser, QHBoxLayout

FLOSS_OUTPUT_JSON_PATH = "floss.json"

class FortuneWidget(cutter.CutterDockWidget):
    def __init__(self, parent):
        super(FortuneWidget, self).__init__(parent)
        self.static_strings = []
        self.decoded_strings = []
        self.stack_strings = []

        self.setObjectName("FLOSS Plugin")
        self.setWindowTitle("FLOSS")

        content = QWidget()
        self.setWidget(content)

        #Using QTextBrowser
        vboxmain = QVBoxLayout(content)
        content.setLayout(vboxmain)

        hboxtop = QHBoxLayout()
        vboxmain.addLayout(hboxtop)

        vboxtop1 = QVBoxLayout()
        vboxtop2 = QVBoxLayout()
        vboxtop3 = QVBoxLayout()

        hboxtop.addLayout(vboxtop1)
        hboxtop.addLayout(vboxtop2)
        hboxtop.addLayout(vboxtop3)

        self.textBrowser1 = QTextBrowser(content)
        self.textBrowser1.setReadOnly(True)
        self.textBrowser1.setText("This program will run FLOSS for the current code.")
        vboxtop1.addWidget(QLabel("Static strings"))
        vboxtop1.addWidget(self.textBrowser1, Qt.AlignCenter)

        self.textBrowser2 = QTextBrowser(content)
        self.textBrowser2.setReadOnly(True)
        self.textBrowser2.setText("This program will run FLOSS for the current code.")
        vboxtop2.addWidget(QLabel("Decoded strings"))
        vboxtop2.addWidget(self.textBrowser2, Qt.AlignCenter)

        self.textBrowser3 = QTextBrowser(content)
        self.textBrowser3.setReadOnly(True)
        self.textBrowser3.setText("This program will run FLOSS for the current code.")
        vboxtop3.addWidget(QLabel("Stack strings"))
        vboxtop3.addWidget(self.textBrowser3, Qt.AlignCenter)


        #create button
        button = QPushButton(content)
        button.setText("Run FLOSS")
        button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        button.setMaximumHeight(50)
        button.setMaximumWidth(200)
        vboxmain.addWidget(button)
        vboxmain.setAlignment(button, Qt.AlignHCenter)

        button.clicked.connect(self.update_strings)

        self.show()

    def update_strings(self):
        #Clear Boxes
        #self.textBrowser1.clear()
        #self.textBrowser2.clear()
        #self.textBrowser3.clear()
        self.run_floss()

        for i in self.static_strings:
            self.textBrowser1.append(i)
            self.textBrowser2.append("RUN")
        self.textBrowser2.append(self.get_filepath())

    @staticmethod
    def get_filepath():
        binary_information = cutter.cmdj("ij")
        return binary_information["core"]["file"]

    def run_floss(self):
        self.textBrowser1.append("Code is running")
        try:
            subprocess.run(
                [
                    "floss",
                    "--output-json",
                    FLOSS_OUTPUT_JSON_PATH,
                    self.get_filepath(),
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            with open(FLOSS_OUTPUT_JSON_PATH) as f:
                floss_json = json.load(f)
                floss_strings = floss_json["strings"]
                self.static_strings = floss_strings["static_strings"]
                self.decoded_strings = floss_strings["decoded_strings"]
                self.stack_strings = floss_strings["stack_strings"]

        except subprocess.SubprocessError as e:

            if e.returncode == 1:
                raise Exception("The FLOSS binary is not in PATH")
            else:
                raise Exception("FLOSS failed to run")
        except Exception as e:
            self.textBrowser1.append(e)

        finally:
            if os.path.exists(FLOSS_OUTPUT_JSON_PATH):
                os.remove(FLOSS_OUTPUT_JSON_PATH)
        self.textBrowser1.append("Code is DONE")



class FlossPlugin(cutter.CutterPlugin):
    name = "FLOSS Plugin"
    description = "Integrating FLOSS into Cutter"
    version = "1.1"
    author = "Cutter developers"

    # Override CutterPlugin methods

    def __init__(self):
        super(FlossPlugin, self).__init__()
        self.disassembly_actions = []
        self.addressable_item_actions = []
        self.disas_action = None
        self.addr_submenu = None
        self.main = None

    def setupPlugin(self):
        #Get FLOSS and binary location
        pass

    def setupInterface(self, main):
        # Dock widget
        widget = FortuneWidget(main)
        main.addPluginDockWidget(widget)

        # Dissassembly context menu
        menu = main.getContextMenuExtensions(cutter.MainWindow.ContextMenuType.Disassembly)
        self.disas_action = menu.addAction("CutterSamplePlugin dissassembly action")
        self.disas_action.triggered.connect(self.handle_disassembler_action)
        self.main = main

        # Context menu for tables with addressable items like Flags,Functions,Strings,Search results,...
        addressable_item_menu = main.getContextMenuExtensions(cutter.MainWindow.ContextMenuType.Addressable)
        self.addr_submenu = addressable_item_menu.addMenu("CutterSamplePlugin") # create submenu
        adrr_action = self.addr_submenu.addAction("Action 1")
        self.addr_submenu.addSeparator() # can use separator and other qt functionality
        adrr_action2 = self.addr_submenu.addAction("Action 2")
        adrr_action.triggered.connect(self.handle_addressable_item_action)
        adrr_action2.triggered.connect(self.handle_addressable_item_action)

    def terminate(self): # optional
        print("FLOSS Plugin shutting down")
        if self.main:
            menu = self.main.getContextMenuExtensions(cutter.MainWindow.ContextMenuType.Disassembly)
            menu.removeAction(self.disas_action)
            addressable_item_menu = self.main.getContextMenuExtensions(cutter.MainWindow.ContextMenuType.Addressable)
            submenu_action = self.addr_submenu.menuAction()
            addressable_item_menu.removeAction(submenu_action)
        print("FLOSS Plugin finished clean up")


# This function will be called by Cutter and should return an instance of the plugin.
def create_cutter_plugin():
    return FlossPlugin()
