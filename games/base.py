from abc import ABC, abstractmethod


class Base(ABC):
    def __init__(self):
        pass


    @abstractmethod
    def start(self) -> None:
        pass
