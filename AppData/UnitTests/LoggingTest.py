from AppData.Classes.Logger import Logger

class LoggingTest():
    def __init__(self):
        self.primary_logger = Logger("LoggingUnitTest")
        self.initial_test()

    def initial_test(self):
        self.primary_logger.info("Making Info Log")
        self.primary_logger.critical("Making Crital Log")
        self.primary_logger.error("Making Error Log")
        self.primary_logger.debug("Making Debug Log")
        try:
            array = []
            array[10]
        except Exception as e:
            self.primary_logger.exception("Making Exception Log", e)
        self.primary_logger.critical("Crital Log")