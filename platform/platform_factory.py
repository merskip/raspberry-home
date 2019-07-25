from abc import ABC, abstractmethod


class PlatformFactory(ABC):

    @abstractmethod
    def get_platform(self):
        pass
