import functools
import time

from django.db import connection, reset_queries


def openapi_ready(f):
    """
    The openapi generation needs to be able to call some methods on the viewset
    without a user on the request (or AnonymousUser being on it). drf_yasg sets
    the swagger_fake_view attr on the view when running these methods, so we can
    check for that and call the super method if it's present.  This does mean
    that the super method output still has to makes sense for the docs you're trying
    to generate.
    """

    @functools.wraps(f)
    def wrapped(self, *args, **kwargs):
        """
        it's simply getting the super
        class, dynamically getattring the method from it and calling that
        method with the args passed to f
        """
        if getattr(self, "swagger_fake_view", False):

            return getattr(super(self.__class__, self), f.__name__)(*args, **kwargs)
        else:
            return f(self, *args, **kwargs)

    return wrapped


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
