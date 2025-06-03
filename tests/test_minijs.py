from unittest.mock import MagicMock
from ProxySea.util import MiniJS

class TestMiniJS:
    def setup_method(self):
        self.js = MiniJS()
        self.js.mini_racer = MagicMock()
    
    def test_set_temp_script_and_print_temp_script(self, capfd):
        script = "var a = 10;"

        self.js.set_temp_script(script)

        assert self.js.temp_script == script

        self.js.print_temp_script()

        out, _ = capfd.readouterr()

        assert script in out

    def test_add_script_to_temp_script(self):
        self.js.set_temp_script("var a = 1;")
        self.js.add_script_to_temp_script("var b = 2;")

        assert self.js.temp_script == "var a = 1;var b = 2;"

    def test_deobfuscate_script_calls_eval_with_cleaned_script(self):
        raw_script = "eval('2 + 2')"
        cleaned_script = raw_script.replace("eval", "")

        self.js.mini_racer.eval.return_value = 4

        result = self.js.deobfuscate_script(raw_script)        
        self.js.mini_racer.eval.assert_called_once_with(cleaned_script)

        assert result == 4

    def test_get_value_from_temp_script_calls_eval_with_combined_script(self):
        self.js.temp_script = "var result = 3 * 7"
        expression = "result"

        combined = f"{self.js.temp_script};{expression};"

        self.js.mini_racer.eval.return_value = 21

        result = self.js.get_value_from_temp_script(expression)

        self.js.mini_racer.eval.assert_called_once_with(combined)

        assert result == 21
