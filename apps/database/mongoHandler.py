import pymongo

class MongoDBHandler:
    def __init__(self, uri, db_name="user_db",collection_name= "users"):
        try:
            self.client = pymongo.MongoClient(uri)
        except pymongo.errors.ConnectionFailure as e:
            print(f"MongoDB connection error: {e}")
        self.db = self.client[db_name] 
        self.collection = self.db[collection_name]

    def switch_collection(self, collection_name):
        """Switch to a different collection within the same database."""
        self.collection = self.db[collection_name]
 
    def create_document(self, data):
        """Insert a document into the collection."""
        return self.collection.insert_one(data)

    def read_document(self, filter_query):
        """Retrieve a document(s) from the collection."""
        return self.collection.find(filter_query)

    def update_document(self, filter_query, update_data):
        """Update a document in the collection."""
        return self.collection.update_one(filter_query, {"$set": update_data})

    def delete_document(self, filter_query):
        """Delete a document(s) from the collection."""
        return self.collection.delete_many(filter_query)
