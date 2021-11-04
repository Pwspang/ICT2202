import json
import os
import subprocess

import cutter

FLOSS_OUTPUT_JSON_PATH = "floss.json"


class FLOSSWidget(cutter.CutterDockWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("FLOSSWidget")
        self.setWindowTitle("FLOSS")
        self.static_strings = []
        self.decoded_strings = []
        self.stack_strings = []

    @staticmethod
    def get_filepath():
        binary_information = cutter.cmdj("ij")
        return binary_information["core"]["file"]

    def run_floss(self):
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
        finally:
            if os.path.exists(FLOSS_OUTPUT_JSON_PATH):
                os.remove(FLOSS_OUTPUT_JSON_PATH)


class FLOSSPlugin(cutter.CutterPlugin):
    name = "FLOSS"
    description = "Extracts static, obfuscated, and stack strings with FLOSS"
    version = "1.0"
    author = "Jon"

    def setupPlugin(self):
        pass

    def setupInterface(self, main):
        widget = FLOSSWidget(main)
        main.addPluginDockWidget(widget)

    def terminate(self):
        pass


def create_cutter_plugin():
    return FLOSSPlugin()
