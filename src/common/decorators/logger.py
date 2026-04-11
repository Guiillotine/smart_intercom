import inspect
from collections.abc import Callable
from functools import wraps
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import logging


class LoggingFunctionInfo:
    """
    A decorator class for logging the execution of methods of a class instance.

    Requires the class instance to have a `_logger` attribute with `info` and `debug`
    methods.
    """

    def __init__(self, description: str = ""):
        """
        Initialize the decorator with an optional description.

        :param description: An optional description for the function's purpose.
        """

        self.description = description

    def __call__(self, func: Callable) -> Callable:
        """
        Wrap the provided function with logging functionality.

        Logs the function execution before and after calling it.
        Determines if the function is async or sync and handles accordingly.

        :param func: The function to decorate.
        :return: The wrapped function (either async or sync).
        """

        is_coroutine = inspect.iscoroutinefunction(func)

        if is_coroutine:

            @wraps(func)
            async def async_wrapper(instance: Any, *args: Any, **kwargs: Any) -> Any:
                """
                Asynchronous wrapper to log function execution.

                Logs the start and end of an asynchronous function call.

                :param instance: The instance of the class calling the function.
                :param args: Positional arguments for the function.
                :param kwargs: Keyword arguments for the function.
                :return: The result of the function execution.
                """

                logger: logging.Logger = getattr(instance, "_logger", None)
                if logger:
                    logger.debug("→ %s() called. %s", func.__name__, self.description)
                result = await func(instance, *args, **kwargs)
                if logger:
                    logger.debug("← %s() finished.", func.__name__)
                return result

            return async_wrapper

        @wraps(func)
        def sync_wrapper(instance: Any, *args: Any, **kwargs: Any) -> Any:
            """
            Synchronous wrapper to log function execution.

            Logs the start and end of a synchronous function call.

            :param instance: The instance of the class calling the function.
            :param args: Positional arguments for the function.
            :param kwargs: Keyword arguments for the function.
            :return: The result of the function execution.
            """

            logger: logging.Logger = getattr(instance, "_logger", None)
            if logger:
                logger.debug("→ %s() called. %s", func.__name__, self.description)
            result = func(instance, *args, **kwargs)
            if logger:
                logger.debug("← %s() finished.", func.__name__)
            return result

        return sync_wrapper
