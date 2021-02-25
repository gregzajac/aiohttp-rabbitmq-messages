import asyncio
import uuid
from multidict import MultiDictProxy
from aio_pika import connect, Message
from aiohttp.web_exceptions import HTTPNotFound


class GetValueRpcClient:
    '''
    Class GetValueRpcClient manages remote procedure call in other server
    for obtaining value for given key

    parameters:
        loop - an event loop for future response from other server

    methods:
        connect - connecting to message broker
            parameters:
                connection - connection object to message broker
        on_response - setting future message obtaining from message broker
        call - sending message to message broker
    '''

    def __init__(self, loop):
        self.connection = None
        self.channel = None
        self.callback_queue = None
        self.futures = {}
        self.loop = loop

    async def connect(self, connection):
        self.connection = connection
        self.channel = await self.connection.channel()
        self.callback_queue = await self.channel.declare_queue(exclusive=True)
        await self.callback_queue.consume(self.on_response)
        return self

    def on_response(self, message):
        _future = self.futures.pop(message.correlation_id)
        _future.set_result(message.body)

    async def call(self, key):
        _corr_id = str(uuid.uuid4())
        _future = self.loop.create_future()

        self.futures[_corr_id] = _future

        await self.channel.default_exchange.publish(
            Message(
                str(key).encode(),
                content_type='text/plain',
                correlation_id=_corr_id,
                reply_to=self.callback_queue.name,
            ),
            routing_key='get_value',
        )
        return await _future


async def send_get_value(key, broker_connection, loop):
    get_value_rpc = await GetValueRpcClient(loop).connect(broker_connection)

    print(f' [.] Get value message with key: {key} prepared for sending')
    response = await get_value_rpc.call(key)
    response = response.decode()
    print(f' [x] Obtained value: {response}')

    if response == '':
        raise HTTPNotFound(text=f'Value for key \'{key}\' not found')

    return float(response)


async def send_set_value(message, broker_connection):
    channel = await broker_connection.channel()

    await channel.default_exchange.publish(
        Message(message.encode()),
        routing_key="set_value",
    )
    
    print(f' [x] Sent set_value message: {message}')
    return f'Message with key and value {message} sent to save'


async def validate_set_data(data):
    result = True

    if not isinstance(data, dict):
        result = False
    if len(data) != 1:
        result = False
    if not isinstance(list(data.keys())[0], str):
        result = False 
    if not (isinstance(list(data.values())[0], float)
            or isinstance(list(data.values())[0], int)):
        result = False 
    
    return result


async def validate_get_data(data):
    result = True
    
    if not isinstance(data, MultiDictProxy):
        result = False
    if len(data) != 1:
        result = False
    if list(data.keys())[0] != 'key':
        result = False
    
    return result


async def start_background_tasks(app):
    try:
        app['broker_connection'] = await connect(
            url=app['config']['broker_url'], loop=app['loop']
        )

    except Exception as exc:
        print('Error during starting background tasks: ', exc)


async def cleanup_background_tasks(app):
    try:
        await app['broker_connection'].close()

    except Exception as exc:
        print('Error during cleaning up background tasks: ', exc)
