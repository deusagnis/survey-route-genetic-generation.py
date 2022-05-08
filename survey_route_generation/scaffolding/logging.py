import time
import logging


def tune_logging(console_log=True, file_log=False, log_dir=None):
    """
    Настроить логирование.
    """
    handlers = []
    if console_log:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
    if file_log:
        filename = log_dir + "\\log_" + str(time.time()) + ".log"
        file_handler = logging.FileHandler(filename, mode="w", encoding="utf-8")
        file_handler.setLevel(logging.INFO)

    logging.basicConfig(
        level=logging.INFO,
        handlers=handlers
    )
