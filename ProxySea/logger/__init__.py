from ..imports import datetime, colorama


class CLR:
    RESET = colorama.Style.RESET_ALL

    # Standardowe kolory tekstu
    CYAN = colorama.Fore.CYAN
    RED = colorama.Fore.RED
    GREEN = colorama.Fore.GREEN
    YELLOW = colorama.Fore.YELLOW
    MAGENTA = colorama.Fore.MAGENTA
    BLUE = colorama.Fore.BLUE
    WHITE = colorama.Fore.WHITE

    # "Pogrubione" kolory – jasne wersje
    CYAN_BOLD = colorama.Fore.LIGHTCYAN_EX
    RED_BOLD = colorama.Fore.LIGHTRED_EX
    GREEN_BOLD = colorama.Fore.LIGHTGREEN_EX
    YELLOW_BOLD = colorama.Fore.LIGHTYELLOW_EX
    MAGENTA_BOLD = colorama.Fore.LIGHTMAGENTA_EX
    BLUE_BOLD = colorama.Fore.LIGHTBLUE_EX
    WHITE_BOLD = colorama.Fore.LIGHTWHITE_EX

    # Style
    BOLD = colorama.Style.BRIGHT
    DIM = colorama.Style.DIM
    NORMAL = colorama.Style.NORMAL


class Logger:
    def __init__(self, _logger_name: str = "Logger", _debug: bool = False) -> None:
        self.debug: bool = _debug

        # ID Information
        self.logger_name: str = f"[{_logger_name}]"

        self.CLR = CLR
    
    def log(self, message: str) -> None:
        if not self.debug:
            return

        now: datetime.datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"({CLR.YELLOW}{now}{CLR.RESET}) {CLR.GREEN}{self.logger_name}{CLR.RESET} {CLR.NORMAL}{message}{CLR.RESET}")
