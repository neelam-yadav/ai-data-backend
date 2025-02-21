import logging

def setup_logger():
    logger = logging.getLogger("enterprise_project")
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler("logs/app.log")
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

logger = setup_logger()
