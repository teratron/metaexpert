from metaexpert.exchanges import Exchange


class Stock(Exchange):
    def __init__(self) -> None:
        pass

    def get_balance(self) -> dict | float:
        return 0.0

    def get_account(self) -> dict:
        return {}
