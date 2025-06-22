"""Centralized logger"""

import logging
import sys
from logging import Formatter, StreamHandler
from typing import Self

from colorama import Fore


class InterceptHandler(logging.Handler):
    """Custom handler for loguru."""

    def emit(self, record: logging.LogRecord) -> None:
        """Intercept log records."""
        CustomLogger().log(record.levelno, record.msg, *record.args, loggerName=record.name)


class CustomLogger:
    """Customized logger"""

    _instance: Self = None

    def __new__(cls) -> Self:
        """
        Singleton constructor for logger.

        Returns:
            Self: Instance of class

        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._logger: logging.Logger = cls._instance.setup()
        return cls._instance

    def setup(self) -> logging.Logger:
        """Create a logger with custom settings."""
        self._name = "time_manager"
        custom_logger = logging.getLogger(self._name)
        log_handler = StreamHandler(sys.stdout)
        log_formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        log_handler.setFormatter(log_formatter)
        custom_logger.addHandler(log_handler)
        custom_logger.setLevel(logging.DEBUG)

        # Intercept log messages from other processes
        for _log in ["uvicorn", "uvicorn.error", "fastapi"]:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]
            _logger.propagate = False

        # Create some formatters for colored logging
        self._color_formatters: dict[int, Formatter] = {
            logging.DEBUG: Formatter(
                f"{Fore.CYAN}%(asctime)s{Fore.RESET} - %(name)s - {Fore.GREEN}%(levelname)s{Fore.RESET} - {Fore.GREEN}%(message)s{Fore.RESET}"
            ),
            logging.INFO: Formatter(
                f"{Fore.CYAN}%(asctime)s{Fore.RESET} - %(name)s - {Fore.BLUE}%(levelname)s{Fore.RESET} - {Fore.BLUE}%(message)s{Fore.RESET}"
            ),
            logging.WARNING: Formatter(
                f"{Fore.CYAN}%(asctime)s{Fore.RESET} - %(name)s - {Fore.YELLOW}%(levelname)s{Fore.RESET} - {Fore.YELLOW}%(message)s{Fore.RESET}"
            ),
            logging.ERROR: Formatter(f"{Fore.CYAN}%(asctime)s{Fore.RESET}- %(name)s - {Fore.RED}%(levelname)s{Fore.RESET} - {Fore.RED}%(message)s{Fore.RESET}"),
            logging.CRITICAL: Formatter(
                f"{Fore.CYAN}%(asctime)s{Fore.RESET} - %(name)s - {Fore.MAGENTA}%(levelname)s{Fore.RESET} - {Fore.MAGENTA}%(message)s{Fore.RESET}"
            ),
        }

        return custom_logger

    def log(self, lev: int, msg: str, *args: object, **extra: dict[str, object]) -> None:  # noqa: C901
        """
        Call the appropriate logger method based on log level.

        Args:
            lev (int): Log level
            msg (str): Message
            args (tuple): Arguments
            extra (dict[str, object]): Extra data

        """
        if "loggerName" in extra:
            self._logger.name = extra.get("loggerName")
        else:
            self._logger.name = self._name

        for handler in self._logger.handlers:
            handler.setFormatter(self._color_formatters[lev])

        extra = {}
        self._logger.log(lev, msg, *args, **extra)
