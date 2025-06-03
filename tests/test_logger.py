from ProxySea.logger import Logger

class TestLogger:
    def setup_method(self):
        self.logger = Logger(
            _logger_name = "Test_Logger",
            _debug = True
        )

    def test_logger_initialization(self) -> None:
        assert "Test_Logger" in self.logger.logger_name
        assert True is self.logger.debug

    def test_logger_log_output_with_debug_enabled(self, capfd) -> None:
        self.logger.log("Hi, ProxySea!")

        out, _ = capfd.readouterr()

        assert True is self.logger.debug
        assert "Hi, ProxySea!" in out
        assert "Test_Logger" in out
        assert "(" in out and ")" in out

    def test_logger_log_output_with_debug_disabled(self, capfd) -> None:
        logger: Logger = Logger(
            _logger_name = "Test_Logger",
            _debug = False
        )

        logger.log("Hi, ProxySea!")

        out, _ = capfd.readouterr()

        assert False is logger.debug
        assert "" == out
