import logging
from traceback import extract_stack
from datetime import datetime

class LoggingHandler:

    def __init__(self, name :str = "default", level=logging.DEBUG):
        if name == "default":
            name = datetime.now().strftime("%Y-%b-%d")
        self.name = name
        self.level = level
        
        if name in logging.Logger.manager.loggerDict:
            self.logger = logging.getLogger(name)
        else:
            self._init_logger()
        
    def _init_logger(self):
        self.log_file = f"logs/{self.name}.log"
        # Create a logger
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self.level)
        
        # Create a file handler for outputting log messages to a file
        fh = logging.FileHandler(self.log_file)
        fh.setLevel(self.level)
        
        # Create a console handler for outputting log messages to console
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARN)
        
        # Create a formatter
        formatter = logging.Formatter('<< %(asctime)s ||| %(name)s ||| %(levelname)s ||| %(message)s')
        
        # Attach the formatter to the handlers
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        # Add handlers to the logger
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)


    def warning(self, msg : str):
        self.logger.warning(msg)

    def info(self, msg : str):
        self.logger.info(msg)
    
    def debug(self, msg : str):
        self.logger.debug(msg)
    
    def error(self, msg : str):
        self.logger.error(msg)
        self.logger.debug(extract_stack())