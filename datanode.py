# core/data/data_node.py

from taipy.core.exceptions import DataNodeIsBeingEdited

class DataNode:
    def __init__(self, name):
        self.name = name
        self._data = None
        self._is_locked = False
        self._editor_id = None

    def lock_edit(self, editor_id=None):
        self._is_locked = True
        self._editor_id = editor_id

    def unlock_edit(self):
        self._is_locked = False
        self._editor_id = None

    def write(self, data, editor_id=None):
        if self._is_locked and (self._editor_id is not None and self._editor_id != editor_id):
            raise DataNodeIsBeingEdited(f"DataNode is being edited by {self._editor_id}.")
        self._data = data
        self._save()

    def append(self, data, editor_id=None):
        if self._is_locked and (self._editor_id is not None and self._editor_id != editor_id):
            raise DataNodeIsBeingEdited(f"DataNode is being edited by {self._editor_id}.")
        if not isinstance(self._data, list):
            raise TypeError("DataNode data must be a list to append.")
        self._data.append(data)
        self._save()

    def _save(self):
        # This method handles saving data to the backend (e.g., file, database).
        pass

class FileDataNode(DataNode):
    def _upload(self, data, editor_id=None):
        if self._is_locked and (self._editor_id is not None and self._editor_id != editor_id):
            raise DataNodeIsBeingEdited(f"DataNode is being edited by {self._editor_id}.")
        self._save_to_file(data)

    def _save_to_file(self, data):
        # Save the file data
        pass


# tests/core/data/test_data_node.py

import pytest
from core.data.data_node import DataNode, DataNodeIsBeingEdited

def test_write_locked_data_node():
    dn = DataNode("test_node")
    dn.lock_edit("editor_1")

    # Attempt to write data with a different editor_id
    with pytest.raises(DataNodeIsBeingEdited):
        dn.write(42, editor_id="editor_2")

    # Should pass when the same editor tries to write
    dn.write(42, editor_id="editor_1")

def test_append_locked_data_node():
    dn = DataNode("test_node")
    dn._data = []
    dn.lock_edit("editor_1")

    # Attempt to append data with a different editor_id
    with pytest.raises(DataNodeIsBeingEdited):
        dn.append(100, editor_id="editor_2")

    # Should pass when the same editor tries to append
    dn.append(100, editor_id="editor_1")

def test_append_non_list_data():
    dn = DataNode("test_node")
    dn._data = 100  # Non-list data

    with pytest.raises(TypeError):
        dn.append(200)


# tests/core/data/test_file_data_node.py

import pytest
from core.data.data_node import FileDataNode, DataNodeIsBeingEdited

def test_file_data_node_upload_locked():
    file_dn = FileDataNode("test_file_node")
    file_dn.lock_edit("editor_1")

    # Attempt to upload data with a different editor_id
    with pytest.raises(DataNodeIsBeingEdited):
        file_dn._upload("new_file_data", editor_id="editor_2")

    # Should pass when the same editor tries to upload
    file_dn._upload("new_file_data", editor_id="editor_1")
