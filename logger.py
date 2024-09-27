import logging

def get_logger(logger_name: str) -> logging.Logger:
    """Logger factory to generate logging objects.

    Returns
        logger: logging.Logger
    """
    logging.basicConfig(
        format="%(levelname)s | %(asctime)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )
    return logging.getLogger(logger_name)