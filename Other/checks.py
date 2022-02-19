import json
from Other.ErrorMessages import TokenNotFound,InvalidToken
class Checks:
    """
    A class filled with checks that aren't related to discord.py
    """
    @staticmethod
    def token_check() -> str:
        try:
            with open("token.json") as f:
                TOKEN = json.load(f)["TOKEN"]
                if len(TOKEN) != 59:
                    raise InvalidToken


        except FileNotFoundError as e:
            try:
                raise TokenNotFound from e
            except TokenNotFound: pass
            TOKEN = input("Enter your token: ")
            if len(TOKEN) != 59:
                try:
                    raise InvalidToken from e
                except InvalidToken:
                    pass
            with open("token.json", "w") as f:
                json.dump({"TOKEN": TOKEN, "API_TOKEN" : 0}, f,indent=2)
        return TOKEN