from ..imports import py_mini_racer

class MiniJS:
    """
    Lightweight wrapper around py_mini_racer for evaluating JavaScript code within Python.

    This class provides a simplified interface for working with obfuscated or dynamically generated
    JavaScript code using the `py_mini_racer` engine (which embeds V8). It supports deobfuscation,
    temporary script assembly, and value extraction from evaluated scripts.

    Note:
        - This class is synchronous and not thread-safe.
        - It is designed for basic JS execution, not for simulating full browser environments.

    Attributes:
        mini_racer (MiniRacer): JavaScript execution engine instance (based on py_mini_racer).
        temp_script (str): Temporary, mutable JavaScript code buffer used for evaluation.

    Methods:
        deobfuscate_script(_script):
            Removes `eval` from a given string and executes the cleaned-up script.

        print_temp_script():
            Prints the current temporary script to stdout. Useful for debugging.

        set_temp_script(_new_script):
            Replaces the current temporary script with the given string.

        add_script_to_temp_script(_new_script):
            Appends additional JavaScript code to the existing temporary script.

        get_value_from_temp_script(_value):
            Evaluates the current temporary script and extracts the value of a specific variable or expression.
    """

    def __init__(self) -> None:
        """
        Initializes a new MiniJS instance with an empty script buffer and embedded JS engine.

        Examples:
        ```
            >>> js = MiniJS()
        ```
        """

        self.mini_racer = py_mini_racer.py_mini_racer.MiniRacer()
        self.temp_script: str = ""

    def print_temp_script(self) -> None:
        """
        Outputs the current temporary script content to the console.

        Returns:
            None

        Examples:
        ```
            >>> js = MiniJS()

            >>> js.set_temp_script("var a = 5;")
            >>> js.print_temp_script()
            >>> var a = 5; # Result of the print_temp_script method
        ```
        """

        print(self.temp_script)

    def deobfuscate_script(self, _script: str) -> str:
        """
        Attempts to deobfuscate JavaScript code by removing 'eval' calls and executing the result.

        Args:
            _script (str): Raw JavaScript code that may contain eval-based obfuscation.

        Returns:
            str:
                Result of evaluating the cleaned script using the MiniRacer engine.

        Examples:
        ```
            >>> js = MiniJS()

            >>> res = js.deobfuscate_script("eval('2 + 2')")
            >>> print(res)
            >>> '4' # Result of the print
        ```
        """

        script = str(_script).replace("eval", "")
        return self.mini_racer.eval(script)

    def set_temp_script(self, _new_script: str) -> None:
        """
        Replaces the temporary script with a new script string.

        Args:
            _new_script (str): New JavaScript code to store in the buffer.
        
        Returns:
            None

        Examples:
        ```
            >>> js = MiniJS()

            >>> js.set_temp_script("var x = 10;")
        ```
        """

        self.temp_script = _new_script
    
    def add_script_to_temp_script(self, _new_script: str) -> None:
        """
        Appends a script fragment to the existing temporary script buffer.

        Args:
            _new_script (str): JavaScript code to be appended.
        
        Returns:
            None

        Examples:
        ```
            >>> js = MiniJS()

            >>> js.set_temp_script("var a = 1;")
            >>> js.add_script_to_temp_script("var b = 2;")
        ```
        """

        self.temp_script += _new_script

    def get_value_from_temp_script(self, _value: str) -> str:
        """
        Evaluates the temporary script, then returns the result of evaluating the provided value expression.

        Args:
            _value (str): JavaScript expression or variable name to evaluate after script execution.

        Returns:
            str: Result of evaluating the requested expression using the current script context.

        Examples:
        ```
            >>> js = MiniJS()
            >>> js.set_temp_script("var result = 3 * 7;")
            >>> res = js.get_value_from_temp_script("result")
            >>> print(res)
            >>> 21 # Result of the print
        ```
        """

        return self.mini_racer.eval(f"{self.temp_script};{_value};")
    
