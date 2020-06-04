import logging
import configparser
def instance_logger():
    try:
        config = configparser.ConfigParser()
        config.read('config.env')
        LOG_FILE = config['CONFIG']['LOG_FILE']
        LOG_LEVEL = config['CONFIG']['LOG_LEVEL']

        if LOG_LEVEL == 'debug':
            log_level = logging.DEBUG
        if LOG_LEVEL == 'info':
            log_level = logging.INFO

        logging.basicConfig(
            level=log_level,
            format='%(asctime)s [%(levelname)s] : %(message)s',
            datefmt='%Y-%m-%d %H:%M',
            handlers=[logging.FileHandler(LOG_FILE, 'a', 'utf-8'), ]
        )

        return logging
    except Exception as e:
        print(e)
        return False


def log(level, s):
    logger = instance_logger()
    if not logger:
        return False

    if level == 'debug':
        logger.debug(s)
    if level == 'info':
        logger.info(s)
    if level == 'error':
        logger.error(s)