import logging

# Just sets up logging, nothing to do with the networking aspect of the server
logger = logging.getLogger("Landscape")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s", "%I:%M:%S")

streamHandler = logging.StreamHandler()

streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)