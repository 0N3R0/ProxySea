from ProxySea.logger import Logger


def test_logger_initialization() -> None:
    logger: Logger = Logger(
        _logger_name = "Test_Logger",
        _debug = True
    )

    assert "Test_Logger" in logger.logger_name
    assert True is logger.debug


def test_logger_log_output_with_debug_enabled(capfd) -> None:
    logger: Logger = Logger(
        _logger_name = "Test_Logger",
        _debug = True
    )

    logger.log("Hi, ProxySea!")

    out, _ = capfd.readouterr()

    assert True is logger.debug
    assert "Hi, ProxySea!" in out
    assert "Test_Logger" in out
    assert "(" in out and ")" in out


def test_logger_log_output_with_debug_disabled(capfd) -> None:
    logger: Logger = Logger(
        _logger_name = "Test_Logger",
        _debug = False
    )

    logger.log("Hi, ProxySea!")

    out, _ = capfd.readouterr()

    assert False is logger.debug
    assert "" == out
