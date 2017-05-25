from abc import ABC, abstractmethod


class BaseFeatureExtractor(ABC):

    def extract(self, emails):
        pass
