from abc import ABC, abstractmethod


class BaseTextTokenizer(ABC):

    @abstractmethod
    def tokenize(self, text):
        pass

