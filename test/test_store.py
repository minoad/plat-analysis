from logging import Logger

import pytest

from documentanalysis.secure import MONGODB_AUTHENTICATION
from documentanalysis.store import FileWriter, MongoWriter


def test_mongo_actual_writer():
    """
    Test the MongoWriter class.
    """
    n = MongoWriter(
        auth=MONGODB_AUTHENTICATION,
        path={"host": "mongodb://mongo:27017/", "dbname": "mydatabase", "collection": "customers"},
    ).save(obj={"name": "John", "address": "Highway 37"}, logger=Logger("test"))
    print(n)


def test_mongo_lambda_actual_writer():
    """
    Test the MongoWriter class.
    """
    n = MongoWriter(
        path={"host": "mongodb://mongo:27017/", "dbname": "mydatabase", "collection": "customers"},
    )
    
    #.save(obj={"name": "John", "address": "Highway 37"}, logger=Logger("test"))
    print(n)

# def test_mongo_writer():
#     """
#     Test the MongoWriter class.
#     """
#     n = MongoWriter(
#         auth=MONGODB_AUTHENTICATION,
#         path={"host": "mongodb://mongo:27017/", "dbname": "mydatabase", "collection": "customers"},
#     ).save(obj={"name": "John", "address": "Highway 37"}, logger=Logger("test"))
#     print(n)


def test_file_write():
    """
    Test the FileWrite class.
    """
    n = FileWriter(auth={}, path={"uri": "test/test.txt"}).save(obj="Hello, World!", logger=Logger("test"))
    print(n)
