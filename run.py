import uvicorn

from src.config.settings.deps import get_settings


def run():
    settings = get_settings()
    uvicorn.run(
        "src.server.core.app:app",
        host=settings.PROJECT.HOST,
        port=settings.PROJECT.PORT,
        reload=True,
        use_colors=True,
    )


if __name__ == '__main__':
    run()
