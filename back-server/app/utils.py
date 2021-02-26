import json
import asyncio
from functools import partial
from aio_pika import connect, Message

import app
from app.db import get_message_value, save_message


async def on_set_value_message(message):
    data = json.loads(message.body.decode())
    message_key = list(data.keys())[0]
    message_value = list(data.values())[0]

    print(f" [x] Saving message in database: {data}")
    await save_message(app.new_app.db_connection, message_key, message_value)


async def on_get_value_message(exchange, message):
    with message.process():
        message_key = message.body.decode()
        message_value = await get_message_value(app.new_app.db_connection, message_key)

        print(
            f" [x] Publish callback for message key: {message_key}, value: {message_value}"
        )
        await exchange.publish(
            Message(
                body=str(message_value).encode(), correlation_id=message.correlation_id
            ),
            routing_key=message.reply_to,
        )


async def handle_set_value():
    channel = await app.new_app.broker_connection.channel()
    queue = await channel.declare_queue("set_value")
    await queue.consume(on_set_value_message, no_ack=True)


async def handle_get_value():
    channel = await app.new_app.broker_connection.channel()
    queue = await channel.declare_queue("get_value")
    await queue.consume(partial(on_get_value_message, channel.default_exchange))
