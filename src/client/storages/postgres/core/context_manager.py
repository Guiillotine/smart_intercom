from src.server.constants import session_context


class PostgresContextManager:

    @staticmethod
    def get_session_context() -> int:
        """
        Retrieve the current PostgreSQL session context ID.
        """
        session_id = session_context.get()

        if not session_id:
            msg = "Currently no session is available"
            raise ValueError(msg)

        return session_id

    @staticmethod
    def set_session_context(session_id: int) -> None:
        """
        Set the PostgreSQL session ID into the current execution context.
        """
        session_context.set(session_id)

    @staticmethod
    def remove_session_context() -> None:
        """
        Remove the PostgreSQL session ID from the current execution context.
        """
        session_context.set(None)
