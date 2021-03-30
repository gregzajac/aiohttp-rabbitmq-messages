import asyncio

import aio_pika
import aiosqlite

from app.settings import config
from app.utils import handle_get_value, handle_set_value
from init_db import DSN, create_db


class App:
    """
    Class App handle main functions of app including handling connections
    with broker message and database

    Parameters:
        tasks_list - list of app async tasks to manage
        broker_url - broker message URL
        db_url - database URL

    Attributes:
        loop - main asyncio event loop
        tasks_list - list of async tasks to manage in the app
        broker_url - broker message url for making connection
        broker_connection - connection object to message broker (rabbitmq)
        db_url - database URL
        db_connection - connection object to the database

    Methods:
        start_app - starting app with establishing connections and appending tasks
        close_app - closing app (closing all tasks and event loop)
    """

    def __init__(self, tasks_list, broker_url, db_url):
        self.loop = asyncio.get_event_loop()
        self.tasks_list = tasks_list
        self.broker_url = broker_url
        self.broker_connection = None
        self.db_url = db_url
        self.db_connection = None

    async def _start_app(self):
        self.broker_connection = await aio_pika.connect(
            url=self.broker_url, loop=self.loop
        )

        self.db_connection = await aiosqlite.connect(
            database=self.db_url, loop=self.loop
        )

        if self.tasks_list:
            for task in self.tasks_list:
                await task

    def start_app(self):
        try:
            print("\nApplication started. To exit press CTRL+C")

            asyncio.ensure_future(self._start_app(), loop=self.loop)
            self.loop.run_forever()

        except Exception as exc:
            print(f"Error during starting app: {exc}")

    async def _exit(self):
        await self.db_connection.close()
        self.loop.stop()

    def close_app(self):
        try:
            for task in asyncio.Task.all_tasks(loop=self.loop):
                task.cancel()
            self.loop.run_until_complete(self._exit())

            print("\nApplication closed")

        except Exception as exc:
            print(f"Error during closing app: {exc}")


create_db()

app = App(
    tasks_list=[handle_set_value(), handle_get_value()],
    broker_url=config["broker_url"],
    db_url=DSN,
)
