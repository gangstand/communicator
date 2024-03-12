import logging


def get_logger(mod_name: str) -> logging.Logger:
    logger = logging.getLogger(mod_name)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("%(asctime)s: %(name)s: %(levelname)s: %(message)s"))
    logger.addHandler(ch)
    return logger


