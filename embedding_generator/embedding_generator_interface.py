from abc import ABC, abstractmethod


class EmbeddingGenerator(ABC):
    @abstractmethod
    def create_embeddings(self, topic) :
        pass
