from AppData.Classes.Logger import Logger
from AppData.Classes.Agent import Agent

class PrimaryConstructor():
    """
    PrimaryConstructor class.

    This class initializes a Logger and an Agent, and then executes a 
    conversation through the Agent.
    """
    def __init__(self):
        """
        Initializes the PrimaryConstructor with a Logger and an Agent.

        The Logger is instantiated with the name "PrimaryLogger". 
        The Agent is instantiated and its logging is initiated.
        A log message indicating completion of instantiation is logged.
        """
        self.logger = Logger("PrimaryLogger")
        self.agent = Agent()
        self.agent.initate_logging()

        self.logger.info(f"Completed Intancing of {self.__class__.__name__}")

    def execute(self):
        """
        Executes the primary functionality of the PrimaryConstructor.

        This method logs a message indicating that the class is running, 
        initiates a conversation through the Agent, and logs a message 
        indicating that the conversation is completed.
        """
        self.logger.info(f"running {self.__class__.__name__}")
        self.agent.begin_conversation()
        self.logger.info(f"Conversation Completed")