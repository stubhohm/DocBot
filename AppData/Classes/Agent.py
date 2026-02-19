from AppData.Classes.Logger import Logger, logging
from AppData.Defaults.imports import chat, ChatResponse, json, unicodedata, ast, os
from AppData.Prompts.SummaryInitial import summary_prompt
from AppData.Defaults.keys import *

class Agent():
    """
    A class representing an AI agent that can engage in conversations,
    process user input, and generate responses using a language model.
    """
    def __init__(self, debugging:bool = False):
        """
        Initializes the Agent object.

        Args:
            debugging (bool, optional): A flag indicating whether debugging
                                         mode is enabled. Defaults to True.
        """
        self.debugging = debugging
        self.logging = False
        self.talking = True
        self.base_prompt = summary_prompt

    def initate_logging(self, logging_name="AgentLogs"):
        """
        Initializes the logging system for the agent.

        Args:
            logging_name (str, optional): The name of the logger.
                                           Defaults to "AgentLogs".
        """
        if self.debugging:
            self.logger = Logger(logging_name, level=logging.DEBUG)
        else:
            self.logger = Logger(logging_name)
        self.logging = True

    def submit_chat(self, user_message:str):
        """
        Submits the user's message to the language model and appends it to a chat log.

        Args:
            user_message (str): The message from the user.

        Returns:
            ChatResponse: The response from the language model.
        """
        self.append_str_to_text_file(f"\nUser: {user_message}", "chatlog.txt")
        total_prompt = self.base_prompt + user_message
        self.debug(f"Total Prompt: {total_prompt}")
        response: ChatResponse = chat(model="gemma3", messages=[{
            role : 'user',
            content : total_prompt
            }   
        ])
        return response.message.content

    def normalize_text(self, response_text:str)-> str:
        """
        Normalizes the response text by replacing various unicode characters
        and strings with their equivalents.

        Args:
            response_text (str): The response text to normalize.

        Returns:
            str: The normalized response text.
        """
        text = unicodedata.normalize("NFKD", response_text.replace("```json","").replace("```","").strip())

        replacements = {
            "\u2018": "'",
            "\u2019": "'",
            "\u201C": '"',
            "\u201D": '"',
            "\u2013": "-",
            "\u2014": "-",
            "\u2026": "...",
            "\U0001f609" : "*wink emoji*",
            "null" : '"null"' 
        }

        for k, v in replacements.items():
            text = text.replace(k, v)

        return text

    def parse_response(self, normalized_text:str)->dict:
        """
        Parses the normalized response text as a JSON object.

        Args:
            normalized_text (str): The normalized response text.

        Returns:
            dict: The parsed JSON response.
        """
        try:
            bot_response_dict = ast.literal_eval(normalized_text)
            self.publish_response_as_json(bot_response_dict, "last_response.json")
            self.info("Response Successfully Parsed")
        except Exception as e:
            error_text_file = "last_response.txt"
            self.exception(f"Unable to parse bot response due to {e}", e)
            self.publish_response_as_txt(normalized_text, error_text_file)
            self.error(f"Response published as text to {error_text_file}")
            bot_response_dict = {}
        return bot_response_dict

    def publish_response_as_txt(self, text:str, file_path):
        """
        Publishes a given text to a file.

        Args:
            text (str): The text to publish.
            file_path (str): The path to the file.
        """
        if not self.debug: return
        if not isinstance(text, str): return False
        with open(file_path, "w") as file:
            file.write(text)
            return True

    def publish_response_as_json(self, response:dict, file_path):
        """
        Publishes a given JSON response to a file.

        Args:
            response (dict): The JSON response.
            file_path (str): The path to the file.
        """
        if not self.debug: return
        if not isinstance(response, dict): return False
        with open(file_path, "w") as file:
            json.dump(response, file, indent=2)
            return True

    def append_str_to_text_file(self, text:str, file_path):
        """
        Appends a given string to a text file.

        Args:
            text (str): The string to append.
            file_path (str): The path to the file.
        """
        if not isinstance(text, str): return False
        with open(file_path, "a") as file:
            file.write(text + "\n")
            return True       

    def begin_conversation(self):
        """
        Starts the conversation loop for the agent.
        """
        self.info("Initiated Conversation")
        user_prompt = "Provide filepath use '/' between dir"
        while self.talking:
            try: 
                path_to_object = input("\n" + user_prompt + "\n\n").strip().split("/")
                file_path = ""
                for object in path_to_object:
                    file_path = os.path.join(file_path, object)
                try:
                    self.info(f"Opening file {file_path}")
                    with open(file_path, "r") as file:
                        message_from_user = file.read()
                except FileNotFoundError as e:
                    self.error(f"File {file_path} not found")
                    continue
                bot_response = self.normalize_text(self.submit_chat(message_from_user))
                self.info(f"Successful Bot Response")
                #bot_response_dict = self.parse_response(bot_response)
                message_to_user = bot_response
                try:
                    self.info(f"Writing bot Response to {file_path}.bot")
                    with open(file_path.replace(".py", "_bot.py"), "w") as file:
                        file.write(bot_response)
                except Exception as e:
                    self.error(f"Unable to write to {file_path.replace(".py", "_bot.py")} due to Error {e}")
                self.append_str_to_text_file(f"Bot Reponse: {message_to_user.splitlines()[0]}....", "chatlog.txt")
                #message_to_user = bot_response_dict.get("message_to_user", "Error, no message")
            except KeyboardInterrupt as e:
                self.talking = False
                self.error("Keyboard Interupt Recieved")
        
        self.info(f"Exiting Conversation with {self.__class__.__name__}")

    def info(self, message):
        """
        Logs an informational message.

        Args:
            message (str): The message to log.
        """
        if not self.logging:return
        self.logger.info(message)

    def debug(self, message):
        """
        Logs a debug message.

        Args:
            message (str): The message to log.
        """
        if not self.debugging: return
        self.logger.debug(message)
    
    def error(self, message):
        """
        Logs an error message.

        Args:
            message (str): The message to log.
        """
        if not self.logging: return
        self.logger.error(message)

    def exception(self, message, exception):
        """
        Logs an exception message along with the exception object.

        Args:
            message (str): The message to log.
            exception (Exception): The exception object.
        """
        if not self.logging:return
        self.logger.exception(message, exception)