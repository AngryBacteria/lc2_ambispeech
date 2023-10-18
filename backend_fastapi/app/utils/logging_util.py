# logger_config.py
import logging

# Create a logger object
logger = logging.getLogger("global_logger")
logger.setLevel(logging.DEBUG)  # Set logging level

# Create a console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Create a formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(ch)
