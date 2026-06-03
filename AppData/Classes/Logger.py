from AppData.Defaults.imports import logging, datetime, os

class Logger():
    """
    A flexible logger class that allows configuration of logging level, 
    format, and output destination.
    """
    def __init__(
            self,
            name,
            level:int= logging.INFO,
            log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            file_path:str = None
            ):
        """
        Initializes the logger.

        Args:
            name (str): The name of the logger.
            level (int, optional): The logging level (e.g., logging.DEBUG, logging.INFO). Defaults to logging.INFO.
            format (str, optional): The format of the log messages. Defaults to a predefined format.
            file_path (str, optional): The path to the log file. If None, logs will be printed to the console. 
        """
        self._name = name
        self._level = level
        self._format = log_format

        self._define_path(file_path)
        self._define_handler()

        #self.info(f"Logging FilePath {self._file_path}")

    def _define_handler(self):
        self.logger = logging.getLogger(self._name)
        self.logger.setLevel(self._level)

        if self._file_path:
            handler = logging.FileHandler(self._file_path)
        else:
            handler = logging.StreamHandler()

        formatter = logging.Formatter(self._format)

        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def _define_path(self, file_path):
        if file_path:
            self._file_path = file_path
            return
        log_dir = os.path.join("logs", self._name)
        try:
            os.makedirs(log_dir, exist_ok=True)  # Create the directory if it doesn't exist
        except OSError as e:
            print(f"Error creating directory {log_dir}: {e}")
            raise  # Re-raise the exception if directory creation fails
        log_file = os.path.join(log_dir, f"{datetime.date.today().strftime("%m_%d_%Y")}.log")
        self._file_path = log_file

    def debug(self, message):
        """
        Logs a debug message.

        Args:
            message (str): The debug message to log.
        """
        self.logger.debug(message)

    def info(self, message):
        """
        Logs an info message.

        Args:
            message (str): The info message to log.
        """
        self.logger.info(message)

    def warning(self, message):
        """
        Logs a warning message.

        Args:
            message (str): The warning message to log.
        """
        self.logger.warning(message)

    def error(self, message):
        """
        Logs an error message.

        Args:
            message (str): The error message to log.
        """
        self.logger.error(message)

    def exception(self, message, exception:Exception):
        """
        Logs an exception message along with the exception object.

        Args:
            message (str): The exception message.
            exception (Exception): The exception object.
        """
        self.logger.exception(message, exc_info=exception)

    def critical(self, message):
        """
        Logs a critical message.

        Args:
            message (str): The critical message to log.
        """
        self.logger.critical(message)
