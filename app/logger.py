"""Centralized logger"""

import logging
import sys
from logging import Formatter, StreamHandler
from typing import Self


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
        custom_logger = logging.getLogger("time_manager")
        log_handler = StreamHandler(sys.stdout)
        log_formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        log_handler.setFormatter(log_formatter)
        custom_logger.addHandler(log_handler)
        custom_logger.setLevel(logging.DEBUG)

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
        self._logger.log(lev, msg, *args, **extra)
