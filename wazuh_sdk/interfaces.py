from abc import ABC, abstractmethod
from typing import Coroutine, Any

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

class AsyncRequestBuilderInterface:
    def __init__(self, client: AsyncClientInterface):
        pass

    async def get(self, endpoint_name: str, query_params: Any) -> Coroutine | None:
       pass


class RequestBuilder:
    def __init__(self, client: ClientInterface):
        pass

    def get(self, endpoint_name: str, query_params: Any) -> Any:
        pass
