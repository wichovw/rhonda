import logging

logger = logging.getLogger('rhonda')
logger.setLevel(logging.INFO)

#Create file handler

handler = logging.FileHandler('rhonda.log')
handler.setLevel(logging.INFO)

#Set up logging format
formatter = logging.Formatter('%(asctime)s - %(name)s/%(threadName)-10s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)