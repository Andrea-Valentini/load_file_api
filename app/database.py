"""
DataBase definition

"""
# pylint: disable=import-error, no-name-in-module
import logging
from os import environ
from objects import Metadata
from psycopg2 import connect
from psycopg2.errors import DuplicateTable


class DataBase:
    """
    DataBase class

    Initialize a PostGreSQL database connection and create a "filemetadata" table.
    """
    def __init__(self):
        self.connection = connect(database=environ["DB_NAME"],
                                    user=environ["DB_USER"],
                                    password=environ["DB_PASSWORD"],
                                    host=environ["DB_HOST_NAME"],
                                    port=environ["DATABASE_PORT"])

        self.cursor = self.connection.cursor()
        try:
            logging.info("Creating filemetadata table ...")
            self.cursor.execute(
            """ CREATE TABLE filemetadata (
                id SERIAL NOT NULL PRIMARY KEY,
                filename VARCHAR(255),
                upload_date DATE NOT NULL
                );
            """
            )
        except DuplicateTable:
            pass

    def update_db(self, new_metadata: Metadata):
        """
        Stores metadata into the DataBase

        Args:
            new_metadata {Metadata}: files metadata to store in the db
        """
        insert_command = "INSERT INTO filemetadata (filename, upload_date) VALUES (%s, %s)"
        try:
            logging.info("Updating database ...")
            self.cursor.execute(insert_command, (new_metadata.filename, new_metadata.upload_date))
            self.connection.commit()
        except Exception as error:
            logging.error(f"The following error has occurred during the database updating: {error}")
            self.connection.rollback()
