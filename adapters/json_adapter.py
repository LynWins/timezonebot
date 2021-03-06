from adapters.adapter import Adapter
from pathlib import Path
import os

import json

class JSONAdapter(Adapter):
    """
    Adapter used for storing JSON
    """
    DB_PATH = "tzdata.json"

    # allow specifying custom db path for tests so that we don't override prod
    def __init__(self, db_path = DB_PATH):
        self.db_path = db_path

    def load(self):
        # check if file exists
        if self.storage_exists() and self.storage_not_empty():
            # this will safely open the file and then close if after it exits the block
            with open(self.db_path, 'r') as f:
                self.data = json.load(f)

        else:
            # if we don't have storage initialize it and create the file
            self.data = {}
            self.store()

    def __setitem__(self, key, item):
        self.data[key] = item

    def __getitem__(self, key):
        return self.data[key]

    def items(self):
        return self.data.items()

    def store(self):
        # yet again we safely open the file and make sure it's closed
        # when we close it data is flished to the disk
        with open(self.db_path, 'w') as f:
            json.dump(self.data, f)

    # check if the file exists
    def storage_exists(self):
        return Path(self.db_path).is_file()

    def storage_not_empty(self):
        return (os.path.getsize(self.db_path) > 0)
