from abc import ABC, abstractmethod


class BaseEmailParser(ABC):

    @abstractmethod
    def parse(self, text):
        pass

