import unittest
from unittest.mock import MagicMock

from documentanalysis.store import MongoStorage


class TestMongoStorage(unittest.TestCase):
    def setUp(self):
        self.storage = MongoStorage({ "name": "John", "address": "Highway 37" })

    def test_save(self):
        # Mock the pymongo.MongoClient and pymongo.MongoClient().__getitem__ methods
        pymongo = MagicMock()
        pymongo.MongoClient.return_value.__getitem__.return_value = MagicMock()

        # Set the mocked pymongo.MongoClient as the MongoClient used in the test
        MongoStorage.pymongo = pymongo

        # Call the save method
        self.storage.save()

        # Assert that the pymongo.MongoClient and pymongo.MongoClient().__getitem__ methods were called
        pymongo.MongoClient.assert_called_once_with("mongodb://mongo:27017/")
        pymongo.MongoClient.return_value.__getitem__.assert_called_once_with("mydatabase")

if __name__ == '__main__':
    unittest.main()