from aiohttp import ClientResponse
from typing import Optional


class ClientError(Exception):
    """The base exception class for the GraphQL client."""

    __slots__ = ('message',)

    def __init__(self, message: str):
        self.message = message

        super().__init__(message)


class ClientResponseError(ClientError):
    """Represents an error in a response."""

    __slots__ = ('response',)

    def __init__(self, message: str, response: ClientResponse):
        self.response = response

        super().__init__(f'{response.status}: {message}')


class ClientResponseHTTPError(ClientResponseError):
    """Represents an error in an HTTP response."""

    __slots__ = ('data',)

    def __init__(self, message: str, response: ClientResponse, data: Optional[dict]):
        self.data = data

        super().__init__(message, response)


class ClientResponseGraphQLError(ClientResponseError):
    """Represents an error in a GraphQL response."""

    __slots__ = ('data',)

    def __init__(self, message: str, response: ClientResponse, data: dict):
        self.data = data

        super().__init__(message, response)


class ClientResponseGraphQLValidationError(ClientResponseGraphQLError):
    """Represents a GraphQL response that failed internal data validation."""

    __slots__ = ()


__all__ = [
    'ClientError',
    'ClientResponseError',
    'ClientResponseHTTPError',
    'ClientResponseGraphQLError',
    'ClientResponseGraphQLValidationError',
]
