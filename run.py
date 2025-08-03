import uvicorn

from app.config import settings


def run():
    uvicorn.run(
        "app.main:app",
        host=settings.PROJECT.HOST,
        port=settings.PROJECT.PORT,
        reload=True
    )


if __name__ == '__main__':
    print('PyCharm', settings.PROJECT.PORT)
    run()
