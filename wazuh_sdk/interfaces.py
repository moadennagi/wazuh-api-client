from abc import ABC, abstractmethod
from typing import Coroutine, Any, Optional

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
    def build_endpoint(self, key: str, params: Optional[dict[str, str | int]] = None) -> str:
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

class AsyncRequestBuilderInterface(ABC):
    def __init__(self, client: AsyncClientInterface):
        pass

    @abstractmethod
    async def get(self, endpoint_name: str, query_params: Any, path_params: dict[str, str | int]) -> Any:
       pass
    
    @abstractmethod
    async def delete(self, endpoint_name: str, query_params: Any, path_params: dict[str, str | int]) -> Any:
       pass

    @abstractmethod
    async def post(self, endpoint_name: str, query_params: Any, body: dict[str, Any], path_params: dict[str, str | int]) -> Any:
       pass


class RequestBuilderInterface(ABC):
    def __init__(self, client: ClientInterface):
        pass

    @abstractmethod
    def get(self, endpoint_name: str, query_params: Any) -> Any:
        pass

    @abstractmethod
    def delete(self, endpoint_name: str, query_params: Any) -> Coroutine | None:
       pass