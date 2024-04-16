"""
Storage Handlers

Protocol interfaces for file, mongodb, sql, and other storage handlers.
"""

import os
from abc import abstractmethod
from dataclasses import dataclass, field
from logging import Logger
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

import pymongo


@runtime_checkable
@dataclass
class StoreWriter(Protocol):
    """
    Represents a storage handler for managing objects.
    Requires authentication information in the form of a dictionary.
        will usually be username and password
    Requires path
        may be a file path, dbname/tablename, or other storage location.
    """

    path: dict[str, str]
    logger: Logger
    auth: dict[str, str]

    @abstractmethod
    def save(self, obj: Any, logger: Logger) -> bool:
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

    def save(self, obj: Any, logger: Logger) -> bool:
        """
        Save the object to a file.
        path: dict[str, str]  # {'uri': 'path/to/file.txt'}
        """
        try:
            with open(Path(self.path.get("uri")), "w", encoding="utf-8") as file:
                result = file.write(obj["text"])
            logger.info(f"Successfully wrote {result} characters to the file with path {self.path}.")
            return result > 0
        except Exception as e:
            logger.error(f"An error occurred while writing to the file: {e} with path {self.path}")
            return False


@dataclass
class MongoWriter(StoreWriter):
    """
    Represents a storage handler for managing objects in MongoDB.
    """

    path: dict[str, str]
    logger: Logger = field(default_factory=lambda: Logger("MongoWriter"))
    auth: dict[str, str] = field(default_factory=lambda: {
        "username": str(os.environ.get("MONGODB_USERNAME")),
        "password": str(os.environ.get("MONGODB_PASSWORD"))})

    def save(self, obj: Any, logger: Logger) -> bool:
        """
        Save the object to MongoDB.
        path: dict[str, str] # {'host': 'mongodb://mongo:27017/', 'dbname': 'mydatabase2', 'collection': 'customers'}
        """
        myclient = pymongo.MongoClient(
            host=self.path["host"], username=self.auth["username"], password=self.auth["password"]
        )
        mydb = myclient[self.path["dbname"]]
        mycol = mydb[self.path["collection"]]
        result = mycol.insert_one(document=obj)
        if result:
            logger.info(f"Inserted document with id: {result.inserted_id} to {self.path}")
            return True
        logger.error(f"failed to write to mongodb with error: {result} to path: {self.path}")
        return False
