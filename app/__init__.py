from collections import namedtuple
import logging

Metrics = namedtuple('Metrics', 'dist_avg clustering')

logger = logging.getLogger('main_logger')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)