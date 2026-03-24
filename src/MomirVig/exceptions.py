class CardNotFoundException(Exception):
    def __init__(self):
        super().__init__("No card could be found with the used search terms")

class UnhandledStatusCodeException(Exception):
    def __init__(self, error, code) -> None:
        self.status_code = code
        self.error = error
        super().__init__(f"Server responded with unhandled status code: {code}. Error: {error}")

class CardNotCreatureException(Exception):
    def __init__(self, name, oracle_id) -> None:
        self.name = name
        self.oracle_id = oracle_id
        super().__init__(f"The {name} card does not have a creature on its front face")