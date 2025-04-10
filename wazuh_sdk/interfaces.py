from abc import ABC, abstractmethod

class ClientInterface(ABC):

    @abstractmethod
    def build_endpoint(self, key: str) -> str:
        """
        Construct the full API endpoint URL using the mapping and provided parameters.
        """
        pass

    @abstractmethod
    def request(self, method: str, endpoint: str, **kwargs):
        """
        Helper method to make an HTTP request.
        """
        pass


class AsyncClientInterface(ABC):

    @abstractmethod
    def build_endpoint(self, key: str) -> str:
        """
        Construct the full API endpoint URL using the mapping and provided parameters.
        """
        pass

    @abstractmethod
    async def request(self, method: str, endpoint: str, **kwargs):
        """
        Helper method to make an HTTP request.
        """
        pass
