import logging

logger = logging.getLogger('rhonda')
logger.setLevel(logging.DEBUG)

#Create file handler

handler = logging.FileHandler('rhonda.log')
handler.setLevel(logging.DEBUG)

#Set up logging format
formatter = logging.Formatter('%(asctime)s - %(name)s/%(threadName)-10s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)