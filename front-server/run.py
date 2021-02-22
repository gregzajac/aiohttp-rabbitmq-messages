from aiohttp import web
from api import app


if __name__ == '__main__':
    try:
        web.run_app(app=app, 
                    host=app['config']['host'],
                    port=app['config']['port'])
    except Exception as exc:
        print(f'Error during starting app: {exc}')
