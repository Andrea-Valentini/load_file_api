"""
Main file

Provides the command to run the backend
"""
# pylint: disable=import-error
from asyncio import Event, run
from tornado.web import Application
from handlers import LoadHandler
from database import DataBase
from objects import Scanner

class Backend:
    """
    Defines interactions to update Database
    """

    def __init__(self, database: DataBase):
        self.database = database


    def create_api(self):
        """
        Creates api application

        Returns:
            {Application}: Tornado application object
        """
        return  Application(
            [(r"/load",LoadHandler),],
            scanner = Scanner(),
            database = self.database)


    async def main(self):
        """
        Tornado main coroutine
        """
        app = self.create_api()
        app.listen(8888)
        shutdown_event = Event()
        await shutdown_event.wait()


if __name__ == "__main__":

    api = Backend(database = DataBase())
    run(api.main())
