import pymongo
import logging
# from config.config_settings import get_settings
# from config.config_settings import get_settings
# from database.mongoHandler import MongoDBHandler

# settings = get_settings()
# mongo = MongoDBHandler(settings.mongodb_uri,"user_db","use") 


logger = logging.getLogger()


class InvalidInputError(Exception):
    """Custom exception for invalid input."""
class CollectionNotFoundError(Exception):
    """Custom exception for when the specified collection is not found."""
class InsertionError(Exception):
    """Custom exception for insertion errors - insert did not occur."""


class MongoDBHandler:
    def __init__(self, uri, db_name="user_db", collection_name="users"):
        try:
            self.client = pymongo.MongoClient(uri)
            self.db = self.client[db_name]
            self.collection = self.switch_collection(collection_name)
        except pymongo.errors.ConnectionFailure as e:
            raise ConnectionError(f"MongoDB connection error: {e}")
        except pymongo.errors.ServerSelectionTimeoutError as e:
            raise ConnectionError(f"MongoDB server selection error: {e}")

    def switch_collection(self, collection_name):
        """Switch to a different collection within the same database."""
        if collection_name not in self.db.list_collection_names():
            raise CollectionNotFoundError(f"Collection '{collection_name}' not found in the database.")
        
        return self.db[collection_name]
 
    def insert_one_document(self, data):
        """Insert a document into the collection."""
        if not isinstance(data, dict):
            raise InvalidInputError("Input must be a dictionary")
        return self.collection.insert_one(data)

    def insert_many_documents(self, data_list):
        """Insert multiple documents into the collection."""
        if not isinstance(data_list, list) or not all(isinstance(item, dict) for item in data_list):
            raise InvalidInputError("Input must be a list of dictionaries.")
        try:
            result = self.collection.insert_many(data_list)
            return result.inserted_ids
        except Exception as e:
            raise InsertionError(e)
    
    def read_one_document(self, filter_query):
        """Retrieve a document(s) from the collection."""
        if not isinstance(filter_query, dict):
            raise InvalidInputError("Input must be a dictionary")
        return self.collection.find_one(filter_query)

    def read_many_document(self, filter_query):
        """Retrieve a document(s) from the collection."""
        if not isinstance(filter_query, dict):
            raise InvalidInputError("Input must be a dictionary")
        return list(self.collection.find(filter_query))
    
    def update_many_document(self, filter_query, update_data):
        """Update a document in the collection."""
        if not isinstance(filter_query, dict) or not isinstance(update_data,dict):
            raise InvalidInputError("Input must be a dictionary")
        return list(self.collection.update_one(filter_query, {"$set": update_data}))

    def delete_many_document(self, filter_query):
        """Delete a document(s) from the collection."""
        if not isinstance(filter_query, dict):
            raise InvalidInputError("Input must be a dictionary")
        return self.collection.delete_many(filter_query)
    
    def close_connection(self):
        self.client.close()