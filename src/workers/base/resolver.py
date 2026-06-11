import inspect
from collections.abc import Awaitable, Callable
from logging import Logger
from types import TracebackType
from typing import Annotated, Any, TypeVar, get_args, get_origin

from fastapi.params import Depends as DependsParam

T = TypeVar("T")


class DependencyResolver:
    """
    Dependency resolver for deps if cannot use FastAPI deps

    Notes:
        - Use if you need to resolve dependency, for example: in workers, scripts, etc.
        - Resolves dependencies recursively
        - Saves resolved dependencies in cache
        - Cannot resolve yield dependencies, like 'Depends(get_db)', pass db to overrides instead
    """

    def __init__(self, logger: Logger):
        """
        Initializes the resolver

        :param logger: Logger to use for logging
        """
        self._logger = logger
        self._cache: dict[tuple[Callable, tuple[tuple[str, Any], ...]], Any] = {}

    async def __aenter__(self):
        """
        Enter the async context manager.

        Example:
            async with DependencyResolver(logger) as resolver:
                result = await resolver.resolve(get_service, db=db)

        :returns: DependencyResolver: The resolver instance itself
        """
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        Exit the async context manager.

        Automatically clears the dependency cache when exiting the context.
        """
        self.clear()

    async def resolve(
        self,
        fn: Callable[..., Awaitable[T]],
        **overrides: Any,
    ) -> T:
        """
        Recursively resolves dependencies for a function

        Example:
            result = await self._resolver.resolve(
                get_association_service,
                db=db
            )

        :param fn: Function to resolve dependencies for (Example: 'get_association_service')
        :param overrides: Optional overrides for dependencies (Example: db=db, logger=self.logger)
        :return: Result of the function call
        """

        key = self._make_cache_key(fn, overrides)

        if key in self._cache:
            return self._cache[key]

        self._logger.debug("Resolving dependencies for %s", fn.__name__)

        sig = inspect.signature(fn)
        kwargs = {}

        for name, param in sig.parameters.items():
            # 1. overrides (for example: db, logger)
            if name in overrides:
                kwargs[name] = overrides[name]
                continue

            # 2. trying to extract dependency
            dep_fn = self._extract_dependency(param.annotation)

            if dep_fn is None:
                error = (
                    f"Cannot resolve dependency '{name}' for {fn.__name__} "
                    f"(annotation={param.annotation})"
                )
                raise RuntimeError(error)

            # 3. resolve recursively
            kwargs[name] = await self.resolve(dep_fn, **overrides)

        # 4. calling function
        result = fn(**kwargs)

        if inspect.isawaitable(result):
            result = await result

        self._cache[key] = result
        return result

    @staticmethod
    def _extract_dependency(annotation: Any) -> Callable | None:
        """
        Extracts deps function from Annotated

        :param annotation: Annotation to extract dependency from
            like: Annotated[IAssociationSrv, Depends(get_association_service)]
        :return: Dependency function or None
        """
        empty_deps_error = "Depends without callable is not supported"

        if get_origin(annotation) is Annotated:
            for arg in get_args(annotation):
                if isinstance(arg, DependsParam):
                    if arg.dependency is None:
                        raise RuntimeError(empty_deps_error)
                    return arg.dependency

        return None

    @staticmethod
    def _make_cache_key(
        fn: Callable, overrides: dict[str, Any]
    ) -> tuple[Callable, tuple[tuple[str, Any], ...]]:
        """
        Makes cache key for function and overrides

        :param fn: Function to make cache key for
        :param overrides: Kwargs passed to function
        :return: Cache key from function and overrides
        """

        overrides_key = tuple(sorted((k, id(v)) for k, v in overrides.items()))
        return fn, overrides_key

    def clear(self) -> None:
        """
        Clears the cache (if needed)
        """
        self._cache.clear()
