import json

from aio_pika import Message, connect
from aiohttp import web
from api.utils import (
    send_get_value,
    send_set_value,
    validate_get_data,
    validate_set_data,
)


async def index(request):
    return web.Response(text="Placeholder")


async def api_set_value(request):
    if request.headers["Content-type"] != "application/json":
        raise web.HTTPUnsupportedMediaType(
            text="Invalid Content-Type, must be 'application/json'"
        )

    try:
        data = await request.json()

    except ValueError as err:
        raise web.HTTPBadRequest(text="Incorrect input data format, must be JSON")

    if not await validate_set_data(data):
        raise web.HTTPBadRequest(
            text="Acceptable only one pair key:value in JSON format, "
            + "value must be a number"
        )

    result = await send_set_value(json.dumps(data), request.app["broker_connection"])

    return web.json_response({"success": True, "data": result})


async def api_get_value(request):
    data = request.query

    if not await validate_get_data(data):
        raise web.HTTPBadRequest(text="Acceptable one parameter named 'key'")

    result = await send_get_value(
        data["key"], request.app["broker_connection"], request.app["loop"]
    )

    return web.json_response({"success": True, "data": result})
