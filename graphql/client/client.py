from aiohttp import ClientSession
from typing import Any, Optional

from .http import HTTPClient


class Client:
    __slots__ = ('_http',)

    def __init__(self, *, session: ClientSession, url: str):
        self._http = HTTPClient(session, url)

    async def request(self, document: str, operation: Optional[str] = None, **variables: Any):
        return await self._http.request(document, operation, variables)


__all__ = [
    'Client',
]
