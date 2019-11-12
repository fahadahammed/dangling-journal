#  Project dangling-journal is developed by "Fahad Ahammed" on 11/12/19, 5:36 PM.
# 
#  Last modified at 11/12/19, 5:34 PM.
# 
#  Github: fahadahammed
#  Email: obak.krondon@gmail.com
# 
#  Copyright (c) 2019. All rights reserved.

# -----------------------------
#
# Project: DanglingJournal
# Version: 2019-11-12_17-34-11
#
# Date: Tue Nov 12 17:34:27 +06 2019
# Created By: Fahad Ahammed
#
# -----------------------------
from DanglingJournal import app
import pymongo
from bson.objectid import ObjectId


class MDB_Operations:
    def __init__(self, collection_name=None):
        self.client = pymongo.MongoClient(app.config["DanglingJournal_DB_HOST"], app.config["DanglingJournal_DB_PORT"])
        database_name = str(app.config["DanglingJournalL_NAME"]).lower()
        self.db = self.client[database_name]
        if collection_name:
            self.collection = self.db[collection_name]
        else:
            exit()

    def get_collections(self):
        return self.db.collection_names()

    def get_count_of_all_objects(self):
        return self.collection.count()

    def insert_data(self, data_json):
        self.collection.insert(data_json)
        return data_json

    def get_data(self, data_json):
        to_return = []
        for i in self.collection.find(data_json):
            to_return.append(i)
        return to_return

    def get_all_data(self):
        alls = []
        for i in self.collection.find({}).sort("created_at"):
            alls.append(i)
        return alls

    def get_specific_data(self, search_params):
        alls = []
        new_search_params = {}
        for i in search_params.keys():
            if i == "log_id":
                i_new = "_id"
                if search_params[i]:
                    new_search_params[i_new] = search_params[i]
            else:
                if search_params[i]:
                    new_search_params[i] = search_params[i]
        for i in self.collection.find(new_search_params).sort("created_at"):
            alls.append(i)
        return alls

    def update_data(self, old_data_condition, new_data):
        if self.collection.update_one(old_data_condition, {"$set": new_data}):
            return True
        else:
            return False

    def delete_data(self, condition_to_delete):
        if self.collection.delete_one(condition_to_delete):
            return True
        else:
            return False

    def collection_create_index(self, field, name, ascending):
        try:
            if ascending:
                return self.collection.create_index([(field, pymongo.ASCENDING)], name=name)
            else:
                return self.collection.create_index([(field, pymongo.DESCENDING)], name=name)
        except pymongo.errors.OperationFailure:
            return False
