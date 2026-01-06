import logging

def setup_logger(name: str) -> object:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(f"{name}.log")
    file_handler.setLevel(logging.DEBUG)

    #console_handler = logging.StreamHandler()
    #console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    #console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    #logger.addHandler(console_handler)

    return logger