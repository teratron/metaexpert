from abc import ABC, abstractmethod


class Exchange(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_balance(self):
        pass
