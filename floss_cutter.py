import json
import os
import subprocess

import cutter
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

FLOSS_OUTPUT_JSON_PATH = "floss.json"


class FLOSSWidget(cutter.CutterDockWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("FLOSSWidget")
        self.setWindowTitle("FLOSS")

        content = QWidget()
        self.setWidget(content)

        # Using QTextBrowser
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

        self.static_strings_browser = QTextBrowser(content)
        self.static_strings_browser.setReadOnly(True)
        self.static_strings_browser.setText(
            'Click on "Run FLOSS" to extract static strings'
        )
        vboxtop1.addWidget(QLabel("Static strings"))
        vboxtop1.addWidget(self.static_strings_browser, Qt.AlignCenter)

        self.decoded_strings_browser = QTextBrowser(content)
        self.decoded_strings_browser.setReadOnly(True)
        self.decoded_strings_browser.setText(
            'Click on "Run FLOSS" to extract decoded strings'
        )
        vboxtop2.addWidget(QLabel("Decoded strings"))
        vboxtop2.addWidget(self.decoded_strings_browser, Qt.AlignCenter)

        self.stack_strings_browser = QTextBrowser(content)
        self.stack_strings_browser.setReadOnly(True)
        self.stack_strings_browser.setText(
            'Click on "Run FLOSS" to extract stack strings'
        )
        vboxtop3.addWidget(QLabel("Stack strings"))
        vboxtop3.addWidget(self.stack_strings_browser, Qt.AlignCenter)

        self.run_button = QPushButton(content)
        self.run_button.setText("Run FLOSS")
        self.run_button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.run_button.setMaximumHeight(50)
        self.run_button.setMaximumWidth(200)
        vboxmain.addWidget(self.run_button)
        vboxmain.setAlignment(self.run_button, Qt.AlignHCenter)

        self.run_button.clicked.connect(self.run_floss)

        self.show()

    @staticmethod
    def get_filepath():
        binary_information = cutter.cmdj("ij")
        return binary_information["core"]["file"]

    def run_floss(self):
        self.run_button.setEnabled(False)
        self.static_strings_browser.setText("FLOSS is running...")
        self.decoded_strings_browser.setText("FLOSS is running...")
        self.stack_strings_browser.setText("FLOSS is running...")

        try:
            subprocess.run(
                [
                    "floss",
                    "--output-json",
                    FLOSS_OUTPUT_JSON_PATH,
                    self.get_filepath(),
                ],
                # stdout=subprocess.DEVNULL,
                # stderr=subprocess.DEVNULL,
            )

            with open(FLOSS_OUTPUT_JSON_PATH) as f:
                floss_json = json.load(f)
                floss_strings = floss_json["strings"]
                static_strings = floss_strings["static_strings"]
                decoded_strings = floss_strings["decoded_strings"]
                stack_strings = floss_strings["stack_strings"]

                self.static_strings_browser.clear()
                self.decoded_strings_browser.clear()
                self.stack_strings_browser.clear()

                for s in static_strings:
                    self.static_strings_browser.append(s)

                for s in decoded_strings:
                    self.decoded_strings_browser.append(s)

                for s in stack_strings:
                    self.stack_strings_browser.append(s)
        except subprocess.SubprocessError as e:
            if e.returncode == 1:
                self.static_strings_browser.setText("The FLOSS binary is not in PATH")
                self.decoded_strings_browser.setText("The FLOSS binary is not in PATH")
                self.stack_strings_browser.setText("The FLOSS binary is not in PATH")
            else:
                self.static_strings_browser.setText("FLOSS failed to run")
                self.decoded_strings_browser.setText("FLOSS failed to run")
                self.stack_strings_browser.setText("FLOSS failed to run")
        except Exception as e:
            self.static_strings_browser.setText(f"Unexpected error: {e}")
            self.decoded_strings_browser.setText(f"Unexpected error: {e}")
            self.stack_strings_browser.setText(f"Unexpected error: {e}")
        finally:
            if os.path.exists(FLOSS_OUTPUT_JSON_PATH):
                os.remove(FLOSS_OUTPUT_JSON_PATH)

            self.run_button.setEnabled(True)


class FLOSSPlugin(cutter.CutterPlugin):
    name = "FLOSS"
    description = "Extract static, obfuscated, and stack strings using FLOSS"
    version = "1.0"
    author = "Jonathan"

    def setupPlugin(self):
        pass

    def setupInterface(self, main):
        widget = FLOSSWidget(main)
        main.addPluginDockWidget(widget)

    def terminate(self):
        pass


def create_cutter_plugin():
    return FLOSSPlugin()
