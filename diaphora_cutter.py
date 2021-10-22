import cutter

class diaphora(cutter.CutterPlugin):
    name = "Diaphora"
    description = "This plugin differs binaries"
    version = "1.0"
    author = "1337 h4x0r"

    def setupPlugin(self):
        pass

    def setupInterface(self, main):
        pass

    def terminate(self):
        pass


#Cutter will call this function first
def create_cutter_plugin():
    return diaphora()
