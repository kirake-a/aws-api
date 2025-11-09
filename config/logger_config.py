import logging
import sys


def setup_logger(name: str) -> logging.Logger:
    """
    Configures and returns a logger instance.
    Logs are displayed in the terminal only.
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Minimum level to capture all logs

    if logger.hasHandlers():
        return logger

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(console_handler)

    return logger