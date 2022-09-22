import functools
import time
from typing import Any, Dict, List, Optional, Union

from django.db import connection, reset_queries
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    _SerializerType,
    extend_schema,
)

class SwaggerWrapper:
    """Initial swagger wrapper for `extend_schema`"""

    operation_id: Optional[str] = None
    parameters: Optional[List[Union[OpenApiParameter, _SerializerType]]] = None
    request: Any
    responses: Any
    auth: Optional[List[str]] = None
    description: Optional[str] = None
    summary: Optional[str] = None
    deprecated: Optional[bool] = None
    tags: Optional[List[str]] = None
    filters: Optional[bool] = None
    exclude: bool = False
    operation: Optional[Dict[str, Any]] = None
    methods: Optional[List[str]] = None
    versions: Optional[List[str]] = None
    examples: Optional[List[OpenApiExample]] = None
    extensions: Optional[Dict[str, Any]] = None

    @classmethod
    def extend_schema(cls, func):
        """Re-declared function"""

        @extend_schema(
            operation_id=cls.operation_id,
            parameters=cls.parameters,
            request=cls.request,
            responses=cls.responses,
            auth=cls.auth,
            description=cls.description,
            summary=cls.summary,
            deprecated=cls.deprecated,
            tags=cls.tags,
            filters=cls.filters,
            exclude=cls.exclude,
            operation=cls.operation,
            methods=cls.methods,
            versions=cls.versions,
            examples=cls.examples,
            extensions=cls.extensions,
        )
        def decorator(*args, **kwargs):
            """Wrapper function"""
            return func(*args, **kwargs)

        return decorator


def encode_uid(pk: str) -> str:
    """Encode uid"""
    return force_str(urlsafe_base64_encode(force_bytes(pk)))


def decode_uid(pk: str) -> str:
    """Decode uid"""
    return force_str(urlsafe_base64_decode(pk))


def query_debugger(func):
    """Decorator for measuring the time and number of requests performed by functions."""

    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        """
        Measure the time and number of requests performed by functions
        """
        reset_queries()

        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {end_queries - start_queries}")
        print(f"Finished in : {(end - start):.2f}s")
        return result

    return inner_func
