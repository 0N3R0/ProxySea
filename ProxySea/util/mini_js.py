from ..imports import py_mini_racer

class MiniJS:
    def __init__(self) -> None:
        self.mini_racer = py_mini_racer.py_mini_racer.MiniRacer()
        self.temp_script: str = ""

    def deobfuscate_script(self, _script: str) -> str:
        script = str(_script).replace("eval", "")
        return self.mini_racer.eval(script)

    def print_temp_script(self) -> None:
        print(self.temp_script)

    def set_temp_script(self, _new_script: str) -> None:
        self.temp_script = _new_script
    
    def add_script_to_temp_script(self, _new_script: str) -> None:
        self.temp_script += _new_script

    def get_value_from_temp_script(self, _value: str) -> str:
        return self.mini_racer.eval(f"{self.temp_script};{_value};")
