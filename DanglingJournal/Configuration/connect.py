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
import MySQLdb
from DanglingJournal import app
import sys
from DanglingJournal import app
import pymongo
from DanglingJournal.Library.DynamicName import DynamicName
from DanglingJournal import ncache
import datetime
from functools import lru_cache


# DB CLASS
class ConnectDB:
    def __init__(self):
        self.db = MySQLdb.connect(host=app.config.get("DanglingJournal_DB_HOST"),  # your host
                             user=app.config.get("DanglingJournal_DB_USER"),       # username
                             passwd=app.config.get("DanglingJournal_DB_PASSWORD"),     # password
                             db=app.config.get("DanglingJournal_DB_NAME"),   # name of the database
                             port=app.config.get("DanglingJournal_DB_PORT"),
                             use_unicode=True,
                             charset="utf8mb4"
        )
        self.db.commit()


# Operation Class
class AnyQuery:
    def __init__(self):
        # Create Cursor for Account
        self.db = ConnectDB().db
        self.cursor = self.db.cursor()
        self.results = None

    # Limiting Memory Usage by Chunking the data
    def resultIter(self, cursor, arraysize=1000):
        """An iterator that uses fetchmany to keep memory usage down"""
        while True:
            results = cursor.fetchmany(arraysize)
            if not results:
                break
            for result in results:
                yield result

    def execute(self, query, parameters=None):
        method = "SELECT"
        if query.split()[0].lower() == "insert":
            method = "INSERT"
        if query.split()[0].lower() == "select":
            method = "SELECT"
        if query.split()[0].lower() == "update":
            method = "UPDATE"
        if query.split()[0].lower() == "delete":
            method = "DELETE"

        if method == "INSERT":
            if parameters:
                self.cursor.execute(query, parameters)
            else:
                self.cursor.execute(query)

            self.results = True

        if method == "SELECT":
            if parameters:
                self.cursor.execute(query, parameters)
            else:
                self.cursor.execute(query)
            self.results = []
            for i in self.resultIter(self.cursor):
                self.results.append(i)
            self.results = tuple(self.results)

        if method == "UPDATE":
            if parameters:
                self.cursor.execute(query, parameters)
            else:
                self.cursor.execute(query)
            self.results = True

        if method == "DELETE":
            if parameters:
                self.cursor.execute(query, parameters)
            else:
                self.cursor.execute(query)
            self.results = True

        # Transaction Commits and close connection.
        self.db.commit()
        self.cursor.close()
        self.db.close()

        # Return Data
        return self.results



class MDB_Operations:
    """Mongo DB Operations"""
    def __init__(self, collection_name=None):
        self.client = pymongo.MongoClient(app.config["DanglingJournal_MDB_HOST"], app.config["DanglingJournal_MDB_PORT"])
        database_name = str(app.config["DanglingJournal_MDB_NAME"]).lower()
        self.db = self.client[database_name]
        if collection_name:
            self.collection = self.db[collection_name]
        else:
            dynamic_collection_name = DynamicName().get_collection_name()
            self.collection = self.db[dynamic_collection_name]
        self.columns = {"entity": 1, "entity_id": 1, "change_section": 1, "change_reason": 1, "change_time": 1,
                                           "previous_value": 1, "current_value": 1,
                                           "responsible_account": 1, "application": 1, "created_at": 1,
                                           "updated_at": 1, "_id": 1}

    def get_collections(self):
        """Get all collections but it is confined to 10 only"""
        print("All collections ***")
        collections = []
        for i in self.db.collection_names():
            collections.append(i)
        collections.sort()
        to_return = collections[::-1][0:10][::-1]
        print("Colls:        ", to_return)
        return to_return

    @ncache.cached(timeout=600, key_prefix=str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")))
    def get_count_of_all_objects(self):
        """Count of all objects of all collections, but depends on the confined list"""
        blank = []
        for i in self.get_collections():
            blank.append(int(self.db[i].count()))
        return sum(blank)

    def get_list_of_datakey(self, section):
        @ncache.cached(timeout=21600, key_prefix=str(section + "_" + str(datetime.datetime.now().strftime("%Y-%m-%d"))))
        def toReturn(section=section):
            to_return = []
            for i in self.get_collections():
                to_return = to_return + self.db[i].distinct(section)
            return to_return
        return toReturn(section=section)

    def insert_data(self, data_json):
        self.collection.insert(data_json)
        return data_json

    def get_all_data(self):
        alls = []
        for i in self.collection.find({}, self.columns):
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
        for i in self.collection.find(new_search_params, self.columns).sort("created_at", pymongo.ASCENDING):
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
