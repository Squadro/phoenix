from abc import ABC, abstractmethod


class MessageConsumer(ABC):
    @abstractmethod
    def process_message(self, payload):
        pass
