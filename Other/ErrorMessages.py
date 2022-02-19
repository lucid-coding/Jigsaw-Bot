
from inspect import currentframe
class Error(Exception):
    """Base class for exceptions in this module."""
    
    @classmethod
    def get_linenumber():
        """Returns the line number of the caller."""
        return currentframe().f_back.f_lineno

class TokenNotFound(Error):
    """Exception raised for errors in the input.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self):
        self.message = 'TokenNotFound: Token not found in token.json'

        super().__init__(self.message)


class InvalidToken(Error):
    """Exception raised for errors in the input.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self):
        self.message = 'InvalidToken: the token you passed is not valid, for more info check -> https://www.writebots.com/discord-bot-token/  \n check the token.json file and edit the value of the TOKEN variable'

        super().__init__(self.message)
