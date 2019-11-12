#  Project dangling-journal is developed by "Fahad Ahammed" on 11/12/19, 9:58 PM.
#
#  Last modified at 11/12/19, 9:58 PM.
#
#  Github: fahadahammed
#  Email: obak.krondon@gmail.com
#
#  Copyright (c) 2019. All rights reserved.

import os
import json
import sys
import datetime
import time
import glob
import pytz
from DanglingJournal import app


class Note:
    def __init__(self):
        self.dt_now = datetime.datetime.now(tz=pytz.timezone('Asia/Dhaka'))
        self.djddfn = app.config["DANGLINGJOURNAL_DATA_D"] + "/notes"

    def list_of_notes(self):
        notes = glob.glob(self.djddfn + "/*")
        if notes:
            return notes
        else:
            return False

    def get_all_notes(self):
        to_return = []
        list_of_notes = self.list_of_notes()
        if list_of_notes:
            for note_file in list_of_notes:
                with open(note_file, "r") as note:
                    to_return.append(json.load(note))
            if to_return:
                return to_return[::-1]
            else:
                return False
        else:
            return False

    def get_single_note(self, note_id):
        to_return = []
        all_notes = self.get_all_notes()
        for note in all_notes:
            if note["id"] == note_id:
                to_return.append(note)
        if to_return:
            return to_return[0]
        else:
            return False

    def store_note(self, data_json):
        if self.list_of_notes():
            new_note_id = len(self.list_of_notes()) + 1
        else:
            new_note_id = 1
        note_file_name = "note-" + str(new_note_id) + ".json"
        note_file = self.djddfn + "/" + note_file_name
        to_store = data_json.copy()
        to_store["revision"] = 1
        to_store["id"] = new_note_id
        to_store["created_at"] = str(self.dt_now)
        to_store["updated_at"] = str(self.dt_now)
        if to_store:
            with open(note_file, 'w', encoding='utf-8') as f:
                json.dump(to_store, f, ensure_ascii=False, indent=4)
            return {
                "message": "Successfully Stored data !",
                "data": to_store
            }
        else:
            return False

    def update_note(self, note_id, data_json):
        old_data = self.get_single_note(note_id=note_id)
        if old_data:
            new_revision = old_data["revision"] + 1
            to_update = old_data.copy()
            for key, value in data_json.items():
                to_update[key] = value
            to_update["revision"] = new_revision
            to_update["updated_at"] = str(self.dt_now)
            if to_update:
                note_file_name = "note-" + str(note_id) + ".json"
                note_file = self.djddfn + "/" + note_file_name
                with open(note_file, 'w', encoding='utf-8') as f:
                    json.dump(to_update, f, ensure_ascii=False, indent=4)
            if to_update:
                return {
                    "message": "Successfully updated data !",
                    "old_data": old_data,
                    "new_data": to_update
                }
            else:
                return False
        else:
            return False

    def delete_single_note(self, note_id):
        note_file_name = "note-" + str(note_id) + ".json"
        note_file = self.djddfn + "/" + note_file_name
        if os.path.exists(note_file):
            os.remove(note_file)
            return True
        else:
            return False