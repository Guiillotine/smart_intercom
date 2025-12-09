from contextvars import ContextVar

session_context: ContextVar[int | None] = ContextVar("session_context", default=None)
