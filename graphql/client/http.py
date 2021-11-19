import aiohttp
from typing import Any, Optional, List

import graphql


class HTTPClient:
    __slots__ = ('session', 'url')

    def __init__(self, session: aiohttp.ClientSession, url: str):
        self.session = session
        self.url = url

    async def request(
        self, __document: str, __operation: Optional[str], __variables: dict, **kwargs: Any
    ):
        # region internal

        _data_validate = kwargs.pop('_data_validate', None)

        # endregion

        json = kwargs.pop('json', None) or dict()

        # NOTE: The GraphQL specification is not able to mandate HTTP
        #       parameters, but the following is described as standard
        #       on GraphQL.org
        #
        #       > A standard GraphQL POST request should use the
        #         application/json content type, and include a
        #         JSON-encoded body of the following form:
        #
        #         {
        #           "query": "...",
        #           "operationName": "...",
        #           "variables": { ... }
        #         }
        #
        #         operationName and variables are optional fields.
        #         operationName is only required if multiple operations
        #         are present in the query.

        json['query'] = __document

        if __operation:
            json['operationName'] = __operation

        if __variables:
            json['variables'] = __variables

        # NOTE: The GraphQL specification is not able to mandate HTTP
        #       methods, but GET and POST are the only methods
        #       described as standard on GraphQL.org.
        #
        #       > Your GraphQL HTTP server should handle the HTTP GET
        #         and POST methods.

        try:
            async with self.session.post(self.url, json=json, **kwargs) as resp:
                if not 200 <= resp.status < 300:
                    # NOTE: The GraphQL specification is not able to
                    #       mandate HTTP status, but this block is pretty
                    #       standard AFAIK.

                    try:
                        data = await resp.json()
                        message = data['message']
                    except (aiohttp.ContentTypeError, KeyError):
                        data = None
                        message = resp.reason

                    raise graphql.client.ClientResponseHTTPError(message, resp, data)

                # NOTE: While the GraphQL specification does not mandate a
                #       serialization format, JSON is by far the most
                #       common response serialization for GraphQL servers.

                data = await resp.json()
        except aiohttp.ClientResponseError as e:
            raise graphql.client.ClientResponseError(e.message, resp) from e
        except aiohttp.ClientError as e:
            raise graphql.client.ClientError(str(e)) from e
        else:
            # NOTE: The GraphQL specification mandates that the
            #       "errors" key must (and must only) exist when the
            #       operation encounters an error. The following block
            #       is extra careful about an empty array anyway.
            #
            #       > If the operation encountered any errors, the
            #       response map must contain an entry with key errors.
            #       [...] If the operation completed without
            #       encountering any errors, this entry must not be
            #       present.

            try:
                errors = data['errors']
            except KeyError:
                errors = None

            if errors:
                exceptions = list()

                for error in errors:
                    # NOTE: The GraphQL specification mandates that
                    #       every error must provide a "message" key
                    #       > Every error must contain an entry with
                    #         the key message with a string description
                    #         of the error intended for the developer
                    #         as a guide to understand and correct the
                    #         error.

                    message = error['message']

                    exceptions.append(
                        graphql.client.ClientResponseGraphQLError(message, resp, data)
                    )
                if False:  # len(exceptions) > 1:
                    # TODO: I'm not sure I love this interface
                    raise ClientResponseGraphQLErrorCollection(exceptions)
                else:
                    raise exceptions[0]

            # region internal

            if _data_validate is not None:
                exc_type, message = _data_validate(data['data'])

                if exc_type is None and message is not None:
                    exc_type = graphql.client.ClientResponseGraphQLValidationError
                elif exc_type is not None and message is None:
                    message = 'data validation failed'

                if exc_type is not None and message is not None:
                    raise exc_type(message, resp, data)

            # endregion

            # NOTE: The GraphQL specification mandates that the 'data' key
            #       must be present when no error is encountered.
            #
            #       > If the data entry in the response is not present, the
            #         errors entry in the response must not be empty. It
            #         must contain at least one error. The errors it
            #         contains should indicate why no data was able to be
            #         returned.

            return data['data']


# mypy appeasement
class ClientResponseGraphQLErrorCollection(Exception):
    def __init__(self, exceptions: List[graphql.client.ClientResponseGraphQLError]):
        pass


__all__ = [
    'HTTPClient',
]
