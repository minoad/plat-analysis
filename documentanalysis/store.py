"""
Storage Handlers

Protocol interfaces for file, mongodb, sql, and other storage handlers.
"""
import importlib
from dataclasses import dataclass, field
from logging import Logger
from pathlib import Path
from typing import Any, Protocol

import pymongo

from documentanalysis.secure import MONGODB_AUTHENTICATION


@dataclass
class StoreWriter(Protocol):
    """
    Represents a storage handler for managing objects.
    Requires authentication information in the form of a dictionary.
        will usually be username and password
    Requires path
        may be a file path, dbname/tablename, or other storage location.
    """
    auth: dict[str, str]
    path: dict[str, str]
    logger: Logger = field(init=False)

    def save(self,  obj: Any, logger: Logger) -> bool:
        """
        Save the object to storage.
        """
        return False


@dataclass
class FileWriter(StoreWriter):
    """
    Represents a storage handler for managing objects in files.
    """
    auth: dict[str, str]
    path: dict[str, str]
    logger: Logger = field(init=False)

    def save(self,  obj: Any, logger: Logger) -> bool:
        """
        Save the object to a file.
        path: dict[str, str]  # {'uri': 'path/to/file.txt'}
        """
        try:
            with open(Path(self.path.get('uri')), "w", encoding="utf-8") as file:
                result = file.write(obj['text'])
            logger.info(f"Successfully wrote {result} characters to the file with path {self.path}.")
            return result > 0
        except Exception as e:
            logger.error(f"An error occurred while writing to the file: {e} with path {self.path}")
            return False


def test_file_write():
    """
    Test the FileWrite class.
    """
    n = FileWriter(
        auth={},
        path={"uri": "test/test.txt"}).save(obj="Hello, World!", logger=Logger("test"))
    print(n)


@dataclass
class MongoWriter(StoreWriter):
    """
    Represents a storage handler for managing objects in MongoDB.
    """
    auth: dict[str, str]
    path: dict[str, str]
    logger: Logger = field(init=False)

    def save(self,  obj: Any, logger: Logger) -> bool:
        """
        Save the object to MongoDB.
        path: dict[str, str] # {'host': 'mongodb://mongo:27017/', 'dbname': 'mydatabase2', 'collection': 'customers'}
        """
        myclient = pymongo.MongoClient(
            host=self.path['host'],
            username=self.auth['username'],
            password=self.auth['password']
        )
        mydb = myclient[self.path['dbname']]
        mycol = mydb[self.path['collection']]
        result = mycol.insert_one(document=obj)
        if result:
            logger.info(f"Inserted document with id: {result.inserted_id} to {self.path}")
            return True
        logger.error(f"failed to write to mongodb with error: {result} to path: {self.path}")
        return False


def test_mongo_writer():
    """
    Test the MongoWriter class.
    """
    n = MongoWriter(
        auth=MONGODB_AUTHENTICATION,
        path={'host': 'mongodb://mongo:27017/', 'dbname': 'mydatabase', 'collection': 'customers'}).save(
            obj={"name": "John", "address": "Highway 37"},
            logger=Logger("test")
    )
    print(n)


def main():
    test_mongo_writer()
    # x = test_file_write()
    # storage = MongoStorage({ "name": "John", "address": "Highway 37" })
    # storage.save()


if __name__ == "__main__":
    main()
