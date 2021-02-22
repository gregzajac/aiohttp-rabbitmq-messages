from aiohttp import web


async def handle_400(request, ex):
    return create_error_response(ex.text, ex.status)

async def handle_404(request, ex):
    return create_error_response(ex.text, ex.status)

async def handle_415(request, ex):
    return create_error_response(ex.text, ex.status)

async def handle_500(request, ex):
    return create_error_response(str(ex), 500)


def create_error_response(message, http_status):
    response = web.json_response({
        'success': False,
        'message': message
    }, status=http_status)
    return response 


def create_error_middleware(overrides):
    @web.middleware
    async def error_middleware(request, handler):
        try:
            return await handler(request)
        except web.HTTPException as ex:
            override = overrides.get(ex.status)
            if override:
                return await override(request, ex)
            raise
        except Exception as ex:
            return await overrides[500](request, ex)
    return error_middleware


def setup_middlewares(app):
    error_middleware = create_error_middleware({
        400: handle_400,
        404: handle_404,
        415: handle_415,
        500: handle_500,
    })
    app.middlewares.append(error_middleware)