import asyncio
from aiohttp import web

from api.settings import config
from api.routes import setup_routes
from api.middlewares import setup_middlewares
from api.utils import start_background_tasks, cleanup_background_tasks


def create_app(config_name="development"):
    loop = asyncio.get_event_loop()

    app = web.Application(loop=loop)
    app["loop"] = loop
    app["config"] = config[config_name]
    setup_routes(app)
    setup_middlewares(app)

    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)

    return app
