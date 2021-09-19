import logging
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


class Color:
    """An enum for the different colors available for printing
    """
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


class Logger:
    def __init__(self, name: str, log_level: str = LOG_LEVEL, use_color: bool = True):
        self.name = name
        self.log_level = logging.getLevelName(LOG_LEVEL)
        logging.basicConfig()
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        self.use_color = use_color

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        warning_message = f"{Color.YELLOW} {str(message)} {Color.END}"
        self.logger.warning(warning_message)

    def debug(self, message):
        self.logger.debug(message)

    def error(self, message):
        error_message = f"{Color.RED} {str(message)} {Color.END}"
        self.logger.error(error_message)
