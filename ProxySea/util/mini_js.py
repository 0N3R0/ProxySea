from ..imports import py_mini_racer

class MiniJS:
    def __init__(self) -> None:
        self.JS = py_mini_racer.py_mini_racer.MiniRacer()
        self.TEMP_SCRIPT: str = ""

    def deobfuscate_script(self, script: str) -> str:
        script = str(script).replace("eval", "")
        return self.JS.eval(script)

    def print_temp_script(self) -> None:
        print(self.TEMP_SCRIPT)

    def set_temp_script(self, new_script: str) -> None:
        self.TEMP_SCRIPT = new_script
    
    def add_script_to_temp_script(self, new_script: str) -> None:
        self.TEMP_SCRIPT += new_script

    def get_value_from_temp_script(self, value: str) -> str:
        return self.JS.eval(f"{self.TEMP_SCRIPT};{value};")
