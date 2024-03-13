from abc import ABC, abstractmethod


class MessageProducer(ABC):
    @abstractmethod
    def produce_message(self, topic, message):
        pass

    @abstractmethod
    def get_config(self):
        pass
